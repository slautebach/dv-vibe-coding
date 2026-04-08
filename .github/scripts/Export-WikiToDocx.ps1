<#
.SYNOPSIS
    Converts a wiki section to a Word (.docx) document, respecting .order files.

.DESCRIPTION
    Recursively walks the specified wiki folder in the reading order defined by .order
    files, pre-processes ADO-specific markdown syntax (TOC tokens, mermaid fences, wiki
    links), concatenates all pages into a single markdown buffer, and converts to Word
    using pandoc.

    Requirements:
      - pandoc must be on PATH (https://pandoc.org/installing.html)
      - .order files must exist in each folder to control page sequence

.PARAMETER WikiSection
    Absolute or relative path to the wiki folder to export.
    Default: wiki\Welcome\Platform-Delivery-Playbook\GitHub-Copilot-for-VSCode

.PARAMETER OutputFile
    Path for the output Word document.
    Default: <repo root>\GitHub-Copilot-for-VSCode.docx

.PARAMETER ReferenceDoc
    Optional path to a .docx file to use as a style reference for pandoc.
    When omitted, pandoc uses its built-in Word styles.

.PARAMETER OpenAfter
    Open the generated document in Word after export. Default: $false

.PARAMETER NoToc
    Suppress the auto-generated table of contents. By default a TOC is included.

.PARAMETER TocDepth
    Heading depth to include in the table of contents. Default: 3 (H1–H3).

.EXAMPLE
    # Export the Copilot section with defaults
    .\BuildScripts\Export-WikiToDocx.ps1

.EXAMPLE
    # Export with a custom style reference and open afterwards
    .\BuildScripts\Export-WikiToDocx.ps1 `
        -ReferenceDoc ".\docs\mnp-template.docx" `
        -OutputFile ".\GitHub-Copilot-Guide.docx" `
        -OpenAfter
#>
[CmdletBinding()]
param(
    [string]$WikiSection = (Join-Path $PSScriptRoot "..\wiki\Welcome\Platform-Delivery-Playbook\GitHub-Copilot-for-VSCode"),
    [string]$OutputFile  = (Join-Path $PSScriptRoot "..\GitHub-Copilot-for-VSCode.docx"),
    [string]$ReferenceDoc = "",
    [switch]$OpenAfter,
    [switch]$NoToc,
    [int]$TocDepth = 3
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

function Get-OrderedFiles {
    <#
    .SYNOPSIS Returns .md file paths for a folder in .order-defined sequence.
    #>
    param([string]$FolderPath)

    $results = [System.Collections.Generic.List[string]]::new()
    $orderFile = Join-Path $FolderPath ".order"

    if (Test-Path $orderFile) {
        $entries = Get-Content $orderFile | Where-Object { $_.Trim() -ne "" }
        foreach ($entry in $entries) {
            $entry = $entry.Trim()
            $mdFile   = Join-Path $FolderPath "$entry.md"
            $subFolder = Join-Path $FolderPath $entry

            # Section landing page (e.g. Setup.md alongside Setup/)
            if (Test-Path $mdFile) {
                $results.Add((Resolve-Path $mdFile).Path)
            }

            # Recurse into child folder
            if (Test-Path $subFolder -PathType Container) {
                foreach ($child in (Get-OrderedFiles -FolderPath $subFolder)) {
                    $results.Add($child)
                }
            }
        }
    } else {
        Write-Warning "No .order file in '$FolderPath' — sorting by name."
        Get-ChildItem -Path $FolderPath -Filter "*.md" | Sort-Object Name |
            ForEach-Object { $results.Add($_.FullName) }
    }

    return $results
}

function Convert-AdoMarkdown {
    <#
    .SYNOPSIS Strips / transforms ADO-specific wiki syntax before pandoc conversion.
    #>
    param([string]$Content, [string]$FilePath)

    # --- Remove ADO control tokens ---
    $content = $content -replace '\[\[_TOC_\]\]', ''
    $content = $content -replace '\[\[_TOSP_\]\]', ''

    # --- Mermaid: ::: mermaid / ::: → fenced code block ---
    # ADO uses ::: mermaid delimiters; pandoc will pass through ```mermaid blocks.
    $content = [regex]::Replace(
        $content,
        '(?ms):::\s*mermaid\s*\r?\n(.*?):::',
        { param($m) "``````mermaid`n" + $m.Groups[1].Value.TrimEnd() + "`n``````" }
    )

    # --- Collapse ADO-style internal wiki links: [[Page Name]] → Page Name ---
    $content = $content -replace '\[\[([^\]]+)\]\]', '$1'

    # --- Trim excess blank lines left by removed tokens ---
    $content = [regex]::Replace($content, '(\r?\n){3,}', "`n`n")

    return $content.Trim()
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

# Validate dependencies
if (-not (Get-Command pandoc -ErrorAction SilentlyContinue)) {
    Write-Error "pandoc not found on PATH. Install from https://pandoc.org/installing.html"
    exit 1
}

$wikiRoot = Resolve-Path $WikiSection
Write-Host "Wiki section : $wikiRoot" -ForegroundColor Cyan
Write-Host "Output file  : $OutputFile" -ForegroundColor Cyan

# Build ordered file list
Write-Host "`nResolving page order..." -ForegroundColor DarkGray
$files = Get-OrderedFiles -FolderPath $wikiRoot

if ($files.Count -eq 0) {
    Write-Error "No .md files found under '$wikiRoot'."
    exit 1
}

Write-Host "Found $($files.Count) pages:" -ForegroundColor DarkGray
$files | ForEach-Object { Write-Host "  $_" -ForegroundColor DarkGray }

# Read, pre-process, and concatenate all pages
Write-Host "`nPre-processing markdown..." -ForegroundColor DarkGray
$sb = [System.Text.StringBuilder]::new()

foreach ($file in $files) {
    $raw = Get-Content -Path $file -Raw -Encoding UTF8
    $processed = Convert-AdoMarkdown -Content $raw -FilePath $file
    if ($processed) {
        [void]$sb.AppendLine($processed)
        [void]$sb.AppendLine()           # blank line between pages
        [void]$sb.AppendLine("---")      # horizontal rule as visual separator
        [void]$sb.AppendLine()
    }
}

# Write combined markdown to a temp file
$tempMd = [System.IO.Path]::GetTempFileName() + ".md"
$sb.ToString() | Set-Content -Path $tempMd -Encoding UTF8

# Build pandoc arguments
$pandocArgs = @(
    $tempMd,
    "-o", $OutputFile,
    "--from", "markdown+smart",
    "--to", "docx",
    "--standalone",
    "--wrap", "none"
)

if ($ReferenceDoc -and (Test-Path $ReferenceDoc)) {
    $pandocArgs += "--reference-doc=$ReferenceDoc"
    Write-Host "Using style reference: $ReferenceDoc" -ForegroundColor DarkGray
}

if (-not $NoToc) {
    $pandocArgs += "--toc"
    $pandocArgs += "--toc-depth=$TocDepth"
    Write-Host "Table of contents: enabled (depth $TocDepth)" -ForegroundColor DarkGray
}

# Run pandoc
Write-Host "`nRunning pandoc..." -ForegroundColor DarkGray
try {
    & pandoc @pandocArgs
    if ($LASTEXITCODE -ne 0) { throw "pandoc exited with code $LASTEXITCODE" }
} finally {
    Remove-Item $tempMd -ErrorAction SilentlyContinue
}

Write-Host "`n✅ Document created: $OutputFile" -ForegroundColor Green

if ($OpenAfter) {
    Write-Host "Opening document..." -ForegroundColor DarkGray
    Start-Process $OutputFile
}
