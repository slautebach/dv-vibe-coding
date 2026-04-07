#Requires -Version 7
<#
.SYNOPSIS
    Recursively builds a Word document from an Azure DevOps wiki folder.

.DESCRIPTION
    Traverses the wiki folder following .order files to determine page sequence,
    concatenates all markdown files with heading levels adjusted for nesting depth,
    inserts page breaks between top-level sections, then passes the result to
    pandoc to produce a Word document.

    Pages and their sub-pages are discovered by matching each .order entry to:
      - <entry>.md  — the page content file
      - <entry>/    — a subfolder containing child pages (with its own .order)

    When no .order file is present, pages are sorted alphabetically.

    Links are rewritten so they work inside the merged Word document:
      - /wiki/path/to/Page.md links  → #page-anchor (cross-reference within doc)
      - Relative .md links           → #page-anchor (resolved against current file)
      - https:// links               → kept as-is
      - #same-page anchors           → kept as-is
      - [[_TOC_]] directives         → removed (pandoc generates its own TOC)

.PARAMETER WikiFolder
    Path to the wiki folder to process.
    Defaults to the parent folder of this script (i.e. the wiki root when the
    script lives in wiki/_tools/).

.PARAMETER OutputFile
    Name of the generated Word document. Resolved relative to this script's
    folder unless an absolute path is given. Defaults to 'Documentation.docx'.

.PARAMETER TocDepth
    Depth of the table of contents. Defaults to 3.

.EXAMPLE
    # Full wiki → Documentation.docx
    pwsh -NoProfile -ExecutionPolicy Bypass -File build-word-doc.ps1

    # Single section only
    pwsh -NoProfile -ExecutionPolicy Bypass -File build-word-doc.ps1 `
        -WikiFolder "C:\dev\sask\MSS\wiki\Detailed-Application-Design" `
        -OutputFile "Design.docx"
#>
param(
    [string]$WikiFolder = (Split-Path $PSScriptRoot -Parent),
    [string]$OutputFile = "Documentation.docx",
    [int]$TocDepth = 3
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Resolve WikiFolder to an absolute path (caller may pass "." or a relative path)
$WikiFolder = (Resolve-Path $WikiFolder).Path

# The wiki root is the parent of the _tools folder. Used to resolve /wiki/ absolute links.
$wikiRoot = Split-Path $PSScriptRoot -Parent

# Resolve output path relative to the script folder when not absolute
if ([System.IO.Path]::IsPathRooted($OutputFile)) {
    $outputPath = $OutputFile
} else {
    $outputPath = Join-Path $PSScriptRoot $OutputFile
}

# Raw OpenXML page break understood by pandoc's docx writer
$pageBreak = @(
    "",
    '```{=openxml}',
    '<w:p><w:r><w:br w:type="page"/></w:r></w:p>',
    '```',
    ""
)

# ---------------------------------------------------------------------------
# Page ID helpers
# Derives a stable, unique heading anchor from a file's path relative to the
# wiki root (e.g. "Design-Decisions/Architecture/Why-D365.md" → "design-decisions-architecture-why-d365").
# This anchor is injected as {#id} on the page's first heading so that
# cross-page links can reference it reliably.
# ---------------------------------------------------------------------------
function Get-PageId {
    param([string]$RelPath)   # path relative to wiki root, forward-slash separated
    $id = $RelPath -replace '\.md$', ''
    $id = $id -replace '[/\\]', '-'
    $id = $id.ToLower()
    $id = [regex]::Replace($id, '[^a-z0-9\-]', '-')
    $id = [regex]::Replace($id, '-+', '-')
    return $id.Trim('-')
}

# Builds a hashtable of  relPath → pageId  for every .md file under $WikiRoot.
# Called once before traversal so all links can be resolved even for pages
# that appear later in the document.
function Build-PageMap {
    param([string]$WikiRoot)
    $map = @{}
    Get-ChildItem -Path $WikiRoot -Filter '*.md' -Recurse -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -notlike '_*' } |
        ForEach-Object {
            $relPath = $_.FullName.Substring($WikiRoot.Length).TrimStart('\', '/') -replace '\\', '/'
            $map[$relPath] = Get-PageId $relPath
        }
    return $map
}

# ---------------------------------------------------------------------------
# Helper: returns ordered page names for a folder, using .order when present
# ---------------------------------------------------------------------------
function Get-OrderedPages {
    param([string]$FolderPath)
    $orderFile = Join-Path $FolderPath '.order'
    if (Test-Path $orderFile) {
        return @(Get-Content $orderFile -Encoding UTF8 |
            Where-Object { $_.Trim() -ne '' })
    }
    # Fallback: alphabetical, skip underscore-prefixed files
    return @(Get-ChildItem -Path $FolderPath -Filter '*.md' |
        Where-Object { $_.Name -notlike '_*' } |
        Sort-Object Name |
        ForEach-Object { [System.IO.Path]::GetFileNameWithoutExtension($_.Name) })
}

# ---------------------------------------------------------------------------
# Helper: bumps every markdown heading by $Offset levels
# ---------------------------------------------------------------------------
function Add-HeadingOffset {
    param([string[]]$Lines, [int]$Offset)
    if ($Offset -le 0) { return $Lines }
    $extra = '#' * $Offset
    return $Lines | ForEach-Object {
        if ($_ -match '^(#{1,6})(\s.+)$') { "$extra$_" } else { $_ }
    }
}

# ---------------------------------------------------------------------------
# Helper: injects {#page-id} onto the first heading in $Lines
# ---------------------------------------------------------------------------
function Add-PageAnchor {
    param([string[]]$Lines, [string]$PageId)
    $injected = $false
    return $Lines | ForEach-Object {
        if (-not $injected -and $_ -match '^#{1,6}\s') {
            $injected = $true
            # Avoid double-injecting if the heading already has an explicit ID
            if ($_ -notmatch '\{#[^}]+\}') {
                return "$_ {#$PageId}"
            }
        }
        return $_
    }
}

# ---------------------------------------------------------------------------
# Helper: rewrites markdown links in a single line so they work inside the
# merged Word document.
#
#   /wiki/path/to/Page.md   →  #page-id  (cross-doc anchor)
#   relative/path.md        →  #page-id  (resolved against $CurrentFileDir)
#   https://...             →  unchanged
#   #anchor                 →  unchanged
#   [[_TOC_]]               →  empty string (ADO-only directive)
# ---------------------------------------------------------------------------
function Rewrite-Links {
    param(
        [string]  $Line,
        [string]  $CurrentFileDir,  # absolute path to the folder containing the current .md
        [string]  $WikiRoot,
        [hashtable]$PageMap
    )

    # Remove ADO table-of-contents directive
    if ($Line -match '^\s*\[\[_TOC_\]\]\s*$') { return '' }

    # Rewrite [text](url) links — but NOT image links ![text](url)
    $Line = [regex]::Replace($Line, '(?<!!)\[([^\]]+)\]\(([^)"\s]+)(?:\s+"[^"]*")?\)', {
        param($m)
        $text = $m.Groups[1].Value
        $url  = $m.Groups[2].Value

        # Keep external links and same-page anchors untouched
        if ($url -match '^https?://' -or $url -match '^#') { return $m.Value }

        # Resolve the target to a wiki-root-relative path
        $relPath = $null

        if ($url -match '^/wiki/(.+)') {
            # Absolute ADO wiki path: /wiki/Section/Page.md
            $relPath = $Matches[1] -replace '\\', '/'
        } elseif ($url -match '^[^/]') {
            # Relative path: resolve against the current file's directory
            try {
                $abs = [System.IO.Path]::GetFullPath((Join-Path $CurrentFileDir ($url -replace '/', [System.IO.Path]::DirectorySeparatorChar)))
                if ($abs.StartsWith($WikiRoot)) {
                    $relPath = $abs.Substring($WikiRoot.Length).TrimStart('\', '/') -replace '\\', '/'
                }
            } catch { <# unresolvable — fall through #> }
        }

        if ($relPath) {
            # Strip any fragment from the path before lookup
            $fragment = ''
            if ($relPath -match '^([^#]+)(#.+)$') {
                $relPath  = $Matches[1]
                $fragment = $Matches[2]
            }

            if ($PageMap.ContainsKey($relPath)) {
                return "[$text](#$($PageMap[$relPath])$fragment)"
            }
            # Target not in the document — render as plain text so the reader
            # can still see the label without a broken link
            return $text
        }

        return $m.Value
    })

    return $Line
}

# ---------------------------------------------------------------------------
# Recursive: collect combined content lines for one wiki folder
#   $HeadingOffset  — extra '#' levels to prepend to headings at this depth
#   $IsFirstRef     — [ref] bool; prevents a page break before the very first page
# ---------------------------------------------------------------------------
function Get-WikiContent {
    param(
        [string]   $FolderPath,
        [string]   $WikiRoot,
        [hashtable]$PageMap,
        [int]      $HeadingOffset,
        [ref]      $IsFirstRef
    )

    $result = [System.Collections.Generic.List[string]]::new()

    foreach ($pageName in (Get-OrderedPages -FolderPath $FolderPath)) {
        $mdFile = Join-Path $FolderPath "$pageName.md"
        $subDir = Join-Path $FolderPath $pageName
        $hasMd  = Test-Path $mdFile  -PathType Leaf
        $hasSub = Test-Path $subDir  -PathType Container

        if (-not $hasMd -and -not $hasSub) {
            Write-Warning "  Skipping '$pageName' — no .md or subfolder found in $FolderPath"
            continue
        }

        # Separator before every page except the very first
        if (-not $IsFirstRef.Value) {
            if ($HeadingOffset -eq 0) {
                $result.AddRange([string[]]$pageBreak)
            } else {
                $result.Add("")
            }
        }
        $IsFirstRef.Value = $false

        # Include this page's own content
        if ($hasMd) {
            $relPath = $mdFile.Substring($WikiRoot.Length).TrimStart('\', '/') -replace '\\', '/'
            $pageId  = $PageMap[$relPath]

            $lines = [string[]](Get-Content $mdFile -Encoding UTF8)

            # 1. Add page anchor to first heading (before offset so {#id} is preserved through bump)
            if ($pageId) { $lines = [string[]](Add-PageAnchor -Lines $lines -PageId $pageId) }

            # 2. Bump heading levels for nesting depth
            $lines = [string[]](Add-HeadingOffset -Lines $lines -Offset $HeadingOffset)

            # 3. Rewrite wiki links to in-document anchors
            $fileDir = Split-Path $mdFile -Parent
            $lines = [string[]]($lines | ForEach-Object {
                Rewrite-Links -Line $_ -CurrentFileDir $fileDir -WikiRoot $WikiRoot -PageMap $PageMap
            })

            $result.AddRange($lines)
            Write-Host "  $('  ' * $HeadingOffset)$pageName.md  [#$pageId]"
        }

        # Recurse into the matching subfolder for child pages
        if ($hasSub) {
            $subFirst = [ref]$true
            $subLines = Get-WikiContent `
                -FolderPath    $subDir `
                -WikiRoot      $WikiRoot `
                -PageMap       $PageMap `
                -HeadingOffset ($HeadingOffset + 1) `
                -IsFirstRef    $subFirst
            if ($subLines.Count -gt 0) {
                $result.Add("")
                $result.AddRange([string[]]$subLines)
            }
        }
    }

    return $result
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if (-not (Test-Path $WikiFolder -PathType Container)) {
    Write-Error "Wiki folder not found: $WikiFolder"
    exit 1
}

Write-Host "Building wiki document from: $WikiFolder"
Write-Host "Wiki root (for link resolution): $wikiRoot"
Write-Host ""

Write-Host "Scanning wiki for page map..."
$pageMap = Build-PageMap -WikiRoot $wikiRoot
Write-Host "  Indexed $($pageMap.Count) pages"
Write-Host ""

$isFirst = [ref]$true
$combined = Get-WikiContent `
    -FolderPath    $WikiFolder `
    -WikiRoot      $wikiRoot `
    -PageMap       $pageMap `
    -HeadingOffset 0 `
    -IsFirstRef    $isFirst

if ($combined.Count -eq 0) {
    Write-Error "No content found in $WikiFolder"
    exit 1
}

$tempFile = Join-Path $env:TEMP "wiki-combined.md"
$combined | Set-Content $tempFile -Encoding UTF8
Write-Host "`nCombined markdown: $tempFile ($($combined.Count) lines)"

# ---------------------------------------------------------------------------
# Run pandoc
# ---------------------------------------------------------------------------
if (-not (Get-Command pandoc -ErrorAction SilentlyContinue)) {
    Write-Error "pandoc is not installed or not on PATH. Install from https://pandoc.org/installing.html"
    exit 1
}

Write-Host "Running pandoc → $outputPath"
pandoc $tempFile `
    --from markdown `
    --to docx `
    --output $outputPath `
    --table-of-contents `
    --toc-depth=$TocDepth

if ($LASTEXITCODE -ne 0) {
    Write-Error "pandoc exited with code $LASTEXITCODE"
    exit $LASTEXITCODE
}

# ---------------------------------------------------------------------------
# Cleanup & report
# ---------------------------------------------------------------------------
Remove-Item $tempFile -Force
$size = (Get-Item $outputPath).Length / 1KB
Write-Host "`n✅  Document generated: $outputPath ($([math]::Round($size, 1)) KB)"
