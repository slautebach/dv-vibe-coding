#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Sets up Azure CLI authentication and configures az devops defaults from the current git repo URL.

.DESCRIPTION
    Reads the git remote origin URL, extracts the Azure DevOps organization URL and project name,
    logs in to Azure CLI if not already authenticated, installs the azure-devops extension,
    and sets az devops defaults so --org and --project flags are not needed on subsequent commands.

.EXAMPLE
    ./setup-auth.ps1
    ./setup-auth.ps1 -Remote upstream
    ./setup-auth.ps1 -Remote origin -Verbose
#>
param(
    [string]$Remote = "origin"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Parse-AzureDevOpsUrl {
    param([string]$Url)

    # HTTPS: https://dev.azure.com/{org}/{project}/_git/{repo}
    if ($Url -match 'https://dev\.azure\.com/([^/]+)/([^/]+)') {
        return @{
            OrgUrl  = "https://dev.azure.com/$($Matches[1])"
            Project = [System.Uri]::UnescapeDataString($Matches[2])
        }
    }

    # Legacy HTTPS: https://{org}.visualstudio.com/{project}/_git/{repo}
    if ($Url -match 'https://([^.]+)\.visualstudio\.com/([^/]+)') {
        return @{
            OrgUrl  = "https://dev.azure.com/$($Matches[1])"
            Project = [System.Uri]::UnescapeDataString($Matches[2])
        }
    }

    # SSH: git@ssh.dev.azure.com:v3/{org}/{project}/{repo}
    if ($Url -match 'git@ssh\.dev\.azure\.com:v3/([^/]+)/([^/]+)') {
        return @{
            OrgUrl  = "https://dev.azure.com/$($Matches[1])"
            Project = [System.Uri]::UnescapeDataString($Matches[2])
        }
    }

    return $null
}

# --- Step 1: Get git remote URL ---
Write-Host "Reading git remote '$Remote'..." -ForegroundColor Cyan
try {
    $remoteUrl = git remote get-url $Remote 2>&1
    if ($LASTEXITCODE -ne 0) { throw "git remote '$Remote' not found." }
} catch {
    Write-Error "Could not read git remote '$Remote'. Are you in a git repository? Error: $_"
    exit 1
}

Write-Verbose "Remote URL: $remoteUrl"

# --- Step 2: Parse org URL and project ---
$parsed = Parse-AzureDevOpsUrl -Url $remoteUrl
if (-not $parsed) {
    Write-Error @"
Could not parse an Azure DevOps URL from remote '$Remote':
  $remoteUrl

Expected formats:
  https://dev.azure.com/{org}/{project}/_git/{repo}
  https://{org}.visualstudio.com/{project}/_git/{repo}
  git@ssh.dev.azure.com:v3/{org}/{project}/{repo}
"@
    exit 1
}

$orgUrl = $parsed.OrgUrl
$project = $parsed.Project

Write-Host "Detected:" -ForegroundColor Cyan
Write-Host "  Organization : $orgUrl"
Write-Host "  Project      : $project"
Write-Host ""

# --- Step 3: Ensure Azure CLI is installed ---
if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    Write-Error "Azure CLI (az) is not installed. Install from https://aka.ms/installazurecliwindows"
    exit 1
}

# --- Step 4: Check login status, login if needed ---
Write-Host "Checking Azure CLI login status..." -ForegroundColor Cyan
$accountJson = az account show --output json 2>$null
if ($LASTEXITCODE -ne 0 -or -not $accountJson) {
    Write-Host "Not logged in. Running 'az login'..." -ForegroundColor Yellow
    az login
    if ($LASTEXITCODE -ne 0) {
        Write-Error "az login failed."
        exit 1
    }
} else {
    $account = $accountJson | ConvertFrom-Json
    Write-Host "  Already logged in as: $($account.user.name)" -ForegroundColor Green
}

# --- Step 5: Install azure-devops extension if missing ---
Write-Host "Checking azure-devops extension..." -ForegroundColor Cyan
$extList = az extension list --output json 2>$null | ConvertFrom-Json
$hasExt = $extList | Where-Object { $_.name -eq "azure-devops" }
if (-not $hasExt) {
    Write-Host "  Installing azure-devops extension..." -ForegroundColor Yellow
    az extension add --name azure-devops --only-show-errors
} else {
    Write-Host "  azure-devops extension already installed." -ForegroundColor Green
}

# --- Step 6: Configure az devops defaults ---
Write-Host "Configuring az devops defaults..." -ForegroundColor Cyan
az devops configure -d organization=$orgUrl project=$project

Write-Host ""
Write-Host "Setup complete." -ForegroundColor Green
Write-Host "You can now run az boards commands without --org or --project flags."
Write-Host ""
Write-Host "Examples:" -ForegroundColor Cyan
Write-Host "  az boards work-item show --id 1234"
Write-Host "  az boards work-item update --id 1234 --state Active"
Write-Host "  az boards query --wiql `"SELECT [System.Id],[System.Title] FROM workitems WHERE [System.AssignedTo] = @me`""
