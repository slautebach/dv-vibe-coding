<#
.SYNOPSIS
    Export and unpack a Dynamics 365 solution to the workspace.

.DESCRIPTION
    Exports an unmanaged solution from Dynamics 365 using the pac CLI tool, unpacks it to the
    <Solutions>/{SolutionName} directory, and updates the version based on the current timestamp.
    Includes built-in delay to prevent file lock issues during unpacking.

.PARAMETER SolutionName
    The unique name of the solution to export.

.PARAMETER EnvironmentUrl
    Optional. The URL of the Dynamics 365 environment to connect to.
    If not specified, uses the currently authenticated environment in pac CLI.

.PARAMETER SolutionPath
    Optional. The base path for solutions. Defaults to "src/D365Solution".

.EXAMPLE
    .\export-solution.ps1 -SolutionName "IncomeAssistance"

.EXAMPLE
    .\export-solution.ps1 -SolutionName "IncomeAssistanceCore" -EnvironmentUrl "https://org.crm.dynamics.com"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SolutionName,

    [Parameter(Mandatory = $false)]
    [string]$EnvironmentUrl = "",

    [Parameter(Mandatory = $false)]
    [string]$SolutionPath = "src\D365Solution"
)

$ErrorActionPreference = "Stop"

# Save current directory
$originalLocation = Get-Location

try {
    # Find workspace root (where src folder exists)
    $workspaceRoot = $PWD
    if (-not (Test-Path (Join-Path $workspaceRoot $SolutionPath))) {
        # Try going up one level
        $workspaceRoot = Split-Path $PWD -Parent
        if (-not (Test-Path (Join-Path $workspaceRoot $SolutionPath))) {
            throw "Cannot find $SolutionPath directory. Please run from workspace root or src directory."
        }
    }
    Set-Location $workspaceRoot

    # Set up paths - export directly to solution folder
    $solutionFolder = Join-Path $SolutionPath $SolutionName
    $extractPath = $solutionFolder
    $zipFile = Join-Path $solutionFolder "$($SolutionName).zip"
    $packageType = "Unmanaged"

    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "Exporting Solution: $SolutionName" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Export Path:     $zipFile"
    Write-Host "Extract Path:    $extractPath"
    if ($EnvironmentUrl) {
        Write-Host "Environment:     $EnvironmentUrl"
    }
    Write-Host ""

    # Create solution folder if it doesn't exist
    if (-not (Test-Path $solutionFolder)) {
        New-Item -Path $solutionFolder -ItemType Directory -Force | Out-Null
    }

    # Clean up previous files
    if (Test-Path $extractPath) {
        Write-Host "Cleaning previous extraction folder..." -ForegroundColor Yellow
        Remove-Item $extractPath -Recurse -Force
    }
    if (Test-Path $zipFile) {
        Write-Host "Removing previous zip file..." -ForegroundColor Yellow
        Remove-Item $zipFile -Force
    }

    # Build pac solution export command (always unmanaged)
    $exportArgs = @(
        "solution", "export",
        "--path", $solutionFolder,
        "--name", $SolutionName,
        "--overwrite"
    )

    if ($EnvironmentUrl) {
        $exportArgs += @("--environment-url", $EnvironmentUrl)
    }

    # Export the solution
    Write-Host "`nExporting solution from Dynamics 365..." -ForegroundColor Green
    & pac @exportArgs
    
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to export solution '$SolutionName'. Error code: $LASTEXITCODE"
    }

    if (-not (Test-Path $zipFile)) {
        throw "Solution zip file not found at: $zipFile"
    }

    Write-Host "✓ Solution exported successfully" -ForegroundColor Green

    # Wait briefly to ensure file handles are released
    Write-Host "`nWaiting for file locks to release..." -ForegroundColor Gray
    Start-Sleep -Seconds 3

    # Unpack the solution
    Write-Host "Unpacking solution..." -ForegroundColor Green
    
    $unpackArgs = @(
        "solution", "unpack",
        "--zipfile", $zipFile,
        "--folder", $extractPath,
        "--packagetype", $packageType,
        "--allowDelete",
        "--allowWrite",
        "--clobber"
    )

    # Add mapping file if it exists
    $mappingFile = Join-Path $SolutionPath "mapping.xml"
    if (Test-Path $mappingFile) {
        Write-Host "Using mapping file: $mappingFile" -ForegroundColor Gray
        $unpackArgs += @("--map", $mappingFile)
    }

    & pac @unpackArgs
    
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to unpack solution. Error code: $LASTEXITCODE"
    }

    Write-Host "✓ Solution unpacked successfully" -ForegroundColor Green

    # Update solution version
    Write-Host "`nUpdating solution version..." -ForegroundColor Green
    
    $otherPath = Join-Path $extractPath "Other"
    if (Test-Path $otherPath) {
        Set-Location $otherPath

        $buildVersion = Get-Date -Format "yyyyMM"
        $revisionVersion = Get-Date -Format "ddHHmm"

        pac solution version -bv $buildVersion | Out-Null
        pac solution version -rv $revisionVersion | Out-Null

        Write-Host "✓ Version updated to x.x.$buildVersion.$revisionVersion" -ForegroundColor Green
    }
    else {
        Write-Host "! Could not find Other folder to update version" -ForegroundColor Yellow
    }

    # Clean up zip file
    Set-Location $workspaceRoot
    Write-Host "`nCleaning up zip file..." -ForegroundColor Green
    Remove-Item $zipFile -Force -ErrorAction SilentlyContinue

    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "✓ Solution export completed successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Location: $extractPath`n"

}
catch {
    Write-Host "`n========================================" -ForegroundColor Red
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "========================================`n" -ForegroundColor Red
    exit 1
}
finally {
    # Return to original directory
    Set-Location $originalLocation
}
