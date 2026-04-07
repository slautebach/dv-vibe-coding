<#
Installs plantuml.jar to the per-user AppData Local folder:
  %LOCALAPPDATA%\plantuml\plantuml.jar

Usage:
  powershell -NoProfile -ExecutionPolicy Bypass -File .github\tools\install-plantuml.ps1

#>

param(
    [string]$Url = 'https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ($IsLinux -or $IsMacOS) {
    Write-Error "This installer is intended for Windows (AppData Local). Use the project's .github/tools location or place plantuml.jar on PATH for non-Windows systems."
    exit 1
}

$installDir = Join-Path $env:LOCALAPPDATA 'plantuml'
if (-not (Test-Path $installDir)) { New-Item -ItemType Directory -Path $installDir -Force | Out-Null }

$target = Join-Path $installDir 'plantuml.jar'

Write-Host "Downloading plantuml.jar to: $target"
try {
    Invoke-WebRequest -Uri $Url -OutFile $target -UseBasicParsing -ErrorAction Stop
} catch {
    Write-Error "Failed to download plantuml.jar from $Url : $_"
    exit 1
}

if (-not (Test-Path $target)) {
    Write-Error "Download completed but target file not found: $target"
    exit 1
}

Write-Host "plantuml.jar downloaded successfully."
Write-Host "You can run it with: java -jar `"$target`""
Write-Host "(Optionally add a wrapper script to PATH to simplify usage.)"
