# Power Platform Build Tools Reference

Complete reference for Microsoft Power Platform Build Tools for Azure DevOps - Azure Pipelines tasks for automating Dynamics 365/Dataverse solution deployments, environment management, and quality checks.

**Official Documentation:** [Microsoft Power Platform Build Tools tasks](https://learn.microsoft.com/en-us/power-platform/alm/devops-build-tool-tasks)

## Overview

Power Platform Build Tools is an Azure DevOps extension that provides tasks for:
- **Solution management** - Export, import, pack, unpack solutions
- **Quality assurance** - Static analysis with Power Platform Checker
- **Environment lifecycle** - Create, delete, backup, restore environments
- **Data operations** - Export and import Dataverse data
- **Power Pages** - Download and upload portal content

**Installation:** Install from [Azure DevOps Marketplace](https://marketplace.visualstudio.com/items?itemName=microsoft-IsvExpTools.PowerPlatform-BuildTools)

## Quick Start

### Basic Pipeline Structure

```yaml
trigger:
  branches:
    include:
    - main

pool:
  vmImage: 'windows-latest'

steps:
# Required: Install Power Platform Build Tools first
- task: PowerPlatformToolInstaller@2
  displayName: 'Install Power Platform Build Tools'

# Verify connection
- task: PowerPlatformWhoAmi@2
  displayName: 'Verify connection'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Dataverse Service Connection'

# Export solution from dev environment
- task: PowerPlatformExportSolution@2
  displayName: 'Export solution'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Dev Environment'
    SolutionName: 'MySolution'
    SolutionOutputFile: '$(Build.ArtifactStagingDirectory)/MySolution.zip'
```

### Service Connection Setup

**Two authentication types supported:**

1. **Service Principal (SPN)** - Recommended for production (supports MFA)
2. **Username/Password** - Legacy option (no MFA support)

**Creating Service Principal connection:**
1. Navigate to **Project Settings** > **Service connections** > **New service connection**
2. Select **Power Platform**
3. Choose **Service Principal**
4. Provide:
   - **Tenant ID** - Azure AD tenant ID
   - **Application (client) ID** - App registration ID
   - **Client Secret** - Application secret
   - **Service Connection Name** - Friendly name for pipeline reference

**For username/password:** Select **Username/password** authentication type and provide credentials.

**See:** [Configure service connections for Power Platform](https://learn.microsoft.com/en-us/power-platform/alm/devops-build-tool-tasks#service-connections)

---

## Helper Tasks

### Power Platform Tool Installer

**Required first step** in all pipelines using Power Platform Build Tools. Installs pac CLI and related tools.

```yaml
- task: PowerPlatformToolInstaller@2
  displayName: 'Install Power Platform Tools'
  inputs:
    DefaultVersion: true  # Use latest versions
    AddToolsToPath: true  # Add pac CLI to PATH for script tasks
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `DefaultVersion` | boolean | Use default versions (true) or specify custom versions (false) |
| `AddToolsToPath` | boolean | Add pac CLI to PATH environment variable for use in script tasks |
| `XrmToolingPackageDeploymentVersion` | string | Specific version of deployment tool (when DefaultVersion=false) |
| `PowerAppsAdminVersion` | string | Specific version of admin module (when DefaultVersion=false) |

**Custom version example:**

```yaml
- task: PowerPlatformToolInstaller@2
  inputs:
    DefaultVersion: false
    XrmToolingPackageDeploymentVersion: '3.3.0.928'
    AddToolsToPath: true
```

### Power Platform WhoAmI

Verifies environment connection by calling WhoAmI. Useful for validating service connections early in pipeline.

```yaml
# Service Principal authentication
- task: PowerPlatformWhoAmi@2
  displayName: 'Verify environment connection'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Dataverse Service Connection'
```

```yaml
# Username/password authentication
- task: PowerPlatformWhoAmi@2
  displayName: 'Verify environment connection'
  inputs:
    authenticationType: PowerPlatformEnvironment
    PowerPlatformEnvironment: 'My Service Connection'
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `authenticationType` | string | `PowerPlatformSPN` (Service Principal) or `PowerPlatformEnvironment` (username/password) |
| `PowerPlatformSPN` | string | Service connection name (for SPN auth) |
| `PowerPlatformEnvironment` | string | Service connection name (for username/password auth) |

---

## Solution Tasks

### Power Platform Export Solution

Exports a solution from source environment to a .zip file.

```yaml
- task: PowerPlatformExportSolution@2
  displayName: 'Export solution from Dev'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Dev Environment'
    SolutionName: 'ContosoSample'
    SolutionOutputFile: '$(Build.ArtifactStagingDirectory)/ContosoSample_$(Build.BuildId).zip'
    AsyncOperation: true
    MaxAsyncWaitTime: 120
    Managed: false
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationType` | string | For SPN | `PowerPlatformSPN` or `PowerPlatformEnvironment` |
| `PowerPlatformSPN` | string | Yes* | Service connection name (SPN auth) |
| `PowerPlatformEnvironment` | string | Yes* | Service connection name (username/password auth) |
| `SolutionName` | string | **Yes** | Solution unique name (not display name) |
| `SolutionOutputFile` | string | **Yes** | Output path and filename for .zip file |
| `AsyncOperation` | boolean | No | Export asynchronously (true/false) - recommended for large solutions |
| `MaxAsyncWaitTime` | integer | No | Max wait time in minutes (default: 60) |
| `Managed` | boolean | No | Export as managed (true) or unmanaged (false) |
| `ExportAutoNumberingSettings` | boolean | No | Include auto-numbering settings |
| `ExportCalendarSettings` | boolean | No | Include calendar settings |
| `ExportCustomizationSettings` | boolean | No | Include customization settings |
| `ExportEmailTrackingSettings` | boolean | No | Include email tracking settings |

**Best practices:**
- Always use `AsyncOperation: true` for solutions over 50 MB
- Use build variables like `$(Build.BuildId)` for unique filenames
- Export unmanaged solutions from dev, then pack as managed for deployment

### Power Platform Import Solution

Imports a solution into target environment.

```yaml
- task: PowerPlatformImportSolution@2
  displayName: 'Import solution to QA'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'QA Environment'
    SolutionInputFile: '$(Pipeline.Workspace)/drop/ContosoSample_managed.zip'
    AsyncOperation: true
    MaxAsyncWaitTime: 60
    PublishWorkflows: true
    UseDeploymentSettingsFile: true
    DeploymentSettingsFile: '$(Pipeline.Workspace)/drop/deployment-settings.json'
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationType` | string | For SPN | `PowerPlatformSPN` or `PowerPlatformEnvironment` |
| `PowerPlatformSPN` | string | Yes* | Service connection name (SPN auth) |
| `PowerPlatformEnvironment` | string | Yes* | Service connection name (username/password auth) |
| `SolutionInputFile` | string | **Yes** | Path to solution .zip file |
| `AsyncOperation` | boolean | No | Import asynchronously (recommended) |
| `MaxAsyncWaitTime` | integer | No | Max wait time in minutes (default: 60) |
| `PublishWorkflows` | boolean | No | Activate workflows after import |
| `OverwriteUnmanagedCustomizations` | boolean | No | Overwrite unmanaged customizations |
| `SkipProductUpdateDependencies` | boolean | No | Skip dependency checks |
| `HoldingSolution` | boolean | No | Import as holding solution for upgrade |
| `UseDeploymentSettingsFile` | boolean | No | Use deployment settings file |
| `DeploymentSettingsFile` | string | When UseDeploymentSettingsFile=true | Path to JSON deployment settings file |

**⚠️ Import Performance Recommendations** ([source](https://learn.microsoft.com/en-us/power-platform/alm/performance-recommendations)):

| Option | Recommendation | Reason |
|--------|---------------|--------|
| `OverwriteUnmanagedCustomizations` | ❌ **Avoid** — keep `false` (default) | Significantly slows down import. Prevent unmanaged customizations in non-dev environments instead. |
| `HoldingSolution: true` + `ApplySolutionUpgrade` | ⚠️ **Slower** — prefer single-stage upgrade | Two-stage holding solution upgrade is slower than the default single-stage import. |
| Publish all customizations | ❌ **Never use** for managed solutions | Only needed for unmanaged solutions. Publishes *all pending changes* environment-wide and slows deployment. Use `PublishWorkflows: true` to activate flows/plugins instead. |
| `ConvertToManaged` / "Import as managed" | ❌ **Deprecated** — do not use | This option is deprecated and should not be used. |

**Deployment settings file** - Pre-populate connection references and environment variables:

```json
{
  "EnvironmentVariables": [
    {
      "SchemaName": "prefix_APIEndpoint",
      "Value": "https://api.production.com"
    }
  ],
  "ConnectionReferences": [
    {
      "LogicalName": "prefix_SharedDataverse",
      "ConnectionId": "connection-guid-here",
      "ConnectorId": "/providers/Microsoft.PowerApps/apis/shared_commondataserviceforapps"
    }
  ]
}
```

**See:** [Deployment settings file format](https://learn.microsoft.com/en-us/power-platform/alm/conn-ref-env-variables-build-tools)

### Power Platform Add Solution Component

Adds a solution component to an unmanaged solution.

```yaml
- task: PowerPlatformAddSolutionComponent@2
  displayName: 'Add solution component'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Dev Environment'
    SolutionName: 'ContosoSample'
    Component: 'contact'
    ComponentType: 1
    AddRequiredComponents: false
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationType` | string | For SPN | `PowerPlatformSPN` or `PowerPlatformEnvironment` |
| `PowerPlatformSPN` | string | Yes* | Service connection name (SPN auth) |
| `PowerPlatformEnvironment` | string | Yes* | Service connection name (username/password auth) |
| `SolutionName` | string | **Yes** | Solution unique name (not display name) |
| `Component` | string | **Yes** | Schema name or ID of the component to add |
| `ComponentType` | integer | **Yes** | Component type value (see Microsoft docs for component type values) |
| `AddRequiredComponents` | boolean | No | Add required components from other solutions |
| `Environment` | string | No | Environment URL or ID |

**Use cases:**
- Dynamically add components to solutions in pipelines
- Automate solution composition
- Build modular solutions

**See:** [Component type values](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/reference/entities/solutioncomponent#componenttype-choicesoptions)

### Power Platform Apply Solution Upgrade

Upgrades a solution that has been imported as a holding solution.

```yaml
- task: PowerPlatformApplySolutionUpgrade@2
  displayName: 'Apply solution upgrade'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Production Environment'
    SolutionName: 'ContosoSample'
    AsyncOperation: true
    MaxAsyncWaitTime: 60
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationType` | string | For SPN | `PowerPlatformSPN` or `PowerPlatformEnvironment` |
| `PowerPlatformSPN` | string | Yes* | Service connection name (SPN auth) |
| `PowerPlatformEnvironment` | string | Yes* | Service connection name (username/password auth) |
| `SolutionName` | string | **Yes** | Solution unique name (not display name) |
| `AsyncOperation` | boolean | No | Perform upgrade asynchronously (recommended) |
| `MaxAsyncWaitTime` | integer | No | Max wait time in minutes (default: 60) |

**Use case:** Used in conjunction with Import Solution when `HoldingSolution: true` to complete a staged solution upgrade.

> **⚠️ Performance:** The two-phase holding solution upgrade is slower than the default single-stage import. Use only when you specifically need to stage the upgrade (e.g., to run pre-upgrade steps between phases). For most deployments, omit `HoldingSolution` and let the import perform a single-stage upgrade directly.

**Two-phase upgrade workflow (slower — use only when staging is required):**
```yaml
# Phase 1: Import as holding solution
- task: PowerPlatformImportSolution@2
  inputs:
    SolutionInputFile: 'solution_managed.zip'
    HoldingSolution: true

# Phase 2: Apply the upgrade
- task: PowerPlatformApplySolutionUpgrade@2
  inputs:
    SolutionName: 'MySolution'
```

### Power Platform Pack Solution

Packs unpacked solution source into a .zip file for deployment.

```yaml
- task: PowerPlatformPackSolution@2
  displayName: 'Pack solution as managed'
  inputs:
    SolutionSourceFolder: '$(Build.SourcesDirectory)/Solutions/ContosoSample'
    SolutionOutputFile: '$(Build.ArtifactStagingDirectory)/ContosoSample_managed.zip'
    SolutionType: Managed
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `SolutionSourceFolder` | string | **Yes** | Path to unpacked solution folder |
| `SolutionOutputFile` | string | **Yes** | Output path and filename for .zip |
| `SolutionType` | string | **Yes** | `Managed`, `Unmanaged`, or `Both` |

**Best practices:**
- Pack as `Managed` for production deployments
- Pack as `Unmanaged` only for development environment restores
- Use `Both` to generate both managed and unmanaged versions

### Power Platform Unpack Solution

Unpacks a solution .zip file into source-controlled folder structure.

```yaml
- task: PowerPlatformUnpackSolution@2
  displayName: 'Unpack solution'
  inputs:
    SolutionInputFile: '$(Pipeline.Workspace)/drop/ContosoSample.zip'
    SolutionTargetFolder: '$(Build.SourcesDirectory)/Solutions/ContosoSample'
    SolutionType: Both
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `SolutionInputFile` | string | **Yes** | Path to solution .zip file |
| `SolutionTargetFolder` | string | **Yes** | Target folder for unpacked files |
| `SolutionType` | string | **Yes** | `Unmanaged` (recommended), `Managed`, or `Both` |

**Best practices:**
- Always unpack `Unmanaged` solutions for source control
- Unpacking managed solutions is rarely needed
- Commit unpacked files to Git for version tracking

### Power Platform Publish Customizations

Publishes all unpublished customizations in an environment.

```yaml
- task: PowerPlatformPublishCustomizations@2
  displayName: 'Publish customizations'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Dev Environment'
```

**Use cases:**
- After multiple solution imports
- After data imports that modify metadata
- Before exporting solution to ensure all changes included

### Power Platform Set Solution Version

Updates solution version number in the environment before export.

```yaml
- task: PowerPlatformSetSolutionVersion@2
  displayName: 'Set solution version'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Dev Environment'
    SolutionName: 'ContosoSample'
    SolutionVersionNumber: '$(Build.BuildNumber)'
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationType` | string | For SPN | `PowerPlatformSPN` or `PowerPlatformEnvironment` |
| `PowerPlatformSPN` | string | Yes* | Service connection name (SPN auth) |
| `SolutionName` | string | **Yes** | Solution unique name |
| `SolutionVersionNumber` | string | **Yes** | Version in format `major.minor.build.revision` |

**Version strategies:**

```yaml
# Use Azure DevOps build number
variables:
  solutionVersion: '1.0.$(Build.BuildId).0'

# Use date-based versioning
variables:
  solutionVersion: '$(Date:yyyy.MM.dd).$(Rev:r)'

# PowerShell dynamic version
- powershell: |
    $version = Get-Date -Format "yyyy.MM.dd.HHmm"
    Write-Host "##vso[task.setvariable variable=solutionVersion]$version"
  displayName: 'Generate version number'
```

### Power Platform Set Connection Variables

Sets pipeline variables from a service connection for use in custom script tasks.

```yaml
- task: PowerPlatformSetConnectionVariables@2
  displayName: 'Set connection variables'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Production Environment'
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationType` | string | For SPN | `PowerPlatformSPN` or `PowerPlatformEnvironment` |
| `PowerPlatformSPN` | string | Yes* | Service connection name (SPN auth) |
| `PowerPlatformEnvironment` | string | Yes* | Service connection name (username/password auth) |
| `ApplicationId` | string | For username/password | Application ID for OAuth login |
| `RedirectUri` | string | For username/password | Redirect URI of the application |

**Output variables set:**
- `PowerPlatformSetConnectionVariables.BuildTools.TenantId`
- `PowerPlatformSetConnectionVariables.BuildTools.ApplicationId`
- `PowerPlatformSetConnectionVariables.BuildTools.ClientSecret`
- `PowerPlatformSetConnectionVariables.BuildTools.DataverseConnectionString`

**Use case:** Access service connectiondetails in PowerShell or other script tasks without hardcoding credentials.

**Example usage:**
```yaml
- task: PowerPlatformSetConnectionVariables@2
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'My Connection'

- powershell: |
    $tenantId = $env:POWERPLATFORMSETCONNECTIONVARIABLES_BUILDTOOLS_TENANTID
    $connectionString = $env:POWERPLATFORMSETCONNECTIONVARIABLES_BUILDTOOLS_DATAVERSECONNECTIONSTRING
    Write-Host "Tenant: $tenantId"
  displayName: 'Use connection variables'
```

### Power Platform Delete Solution

Deletes a solution from target environment.

```yaml
- task: PowerPlatformDeleteSolution@2
  displayName: 'Delete solution'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Test Environment'
    SolutionName: 'ContosoSample'
```

**Warning:** Deletes solution and all its components. Use carefully in production environments.

### Power Platform Deploy Package

Deploys a package (.dll assembly) created with Package Deployer tool.

```yaml
- task: PowerPlatformDeployPackage@2
  displayName: 'Deploy package'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Production Environment'
    PackageFile: '$(Pipeline.Workspace)/drop/DeploymentPackage.dll'
    MaxAsyncWaitTime: 120
```

**Use case:** Deploy multiple solutions with data and custom logic in single deployment.

**See:** [Create packages for Package Deployer](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/package-deployer/create-packages-package-deployer)

---

## Quality Check Tasks

### Power Platform Checker

Runs static analysis on solution files using Power Platform Checker (Solution Checker).

```yaml
- task: PowerPlatformChecker@2
  displayName: 'Run Solution Checker'
  inputs:
    PowerPlatformSPN: 'Dataverse Service Connection'
    FilesToAnalyze: '$(Build.ArtifactStagingDirectory)/**/*.zip'
    RuleSet: '0ad12346-e108-40b8-a956-9a8f95ea18c9'
    ErrorLevel: 'HighIssueCount'
    ErrorThreshold: 5
    FailOnPowerAppsCheckerAnalysisError: true
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `PowerPlatformSPN` | string | **Yes** | Service connection (requires licensed environment) |
| `UseDefaultPACheckerEndpoint` | boolean | No | Use default checker endpoint (default: true) |
| `CustomPACheckerEndpoint` | string | If UseDefaultPACheckerEndpoint=false | Custom endpoint (e.g., https://japan.api.advisor.powerapps.com/) |
| `FileLocation` | string | No | `localFiles` (default) or `sasUriFile` |
| `FilesToAnalyze` | string | For localFiles | Wildcard path to .zip files (e.g., `**/*.zip`) |
| `FilesToExclude` | string | No | Files to exclude (comma or semicolon separated) |
| `FilesToAnalyzeSasUri` | string | For sasUriFile | SAS URI to analyze |
| `RuleSet` | string | **Yes** | Rule set GUID or name |
| `RulesToOverride` | string | No | JSON array of rule overrides |
| `ErrorLevel` | string | No | Severity level: `CriticalIssueCount`, `HighIssueCount`, `MediumIssueCount`, etc. |
| `ErrorThreshold` | integer | No | Max allowed issues at ErrorLevel (default: 0) |
| `FailOnPowerAppsCheckerAnalysisError` | boolean | No | Fail pipeline on analysis error |

**Rule sets:**
- **Solution Checker** (GUID: `0ad12346-e108-40b8-a956-9a8f95ea18c9`) - Standard best practices
- **AppSource Certification** - Extended rules for marketplace submission

**Rule override example:**

```yaml
inputs:
  RulesToOverride: |
    [
      {"Id":"meta-remove-dup-reg","OverrideLevel":"Medium"},
      {"Id":"il-avoid-specialized-update-ops","OverrideLevel":"Low"}
    ]
```

**Results:** Analysis generates SARIF file published as pipeline artifact.

---

## Environment Management Tasks

### Power Platform Create Environment

Creates a new Power Platform environment.

```yaml
- task: PowerPlatformCreateEnvironment@2
  displayName: 'Create test environment'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Admin Service Connection'
    DisplayName: 'Contoso Test $(Build.BuildId)'
    LocationName: 'unitedstates'
    EnvironmentSku: 'Sandbox'
    CurrencyName: 'USD'
    LanguageName: '1033'
    DomainName: 'contoso-test-$(Build.BuildId)'
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `DisplayName` | string | **Yes** | Environment display name |
| `LocationName` | string | **Yes** | Region (e.g., unitedstates, europe, asia) |
| `EnvironmentSku` | string | **Yes** | `Sandbox`, `Production`, `Trial`, `SubscriptionBasedTrial` |
| `DomainName` | string | **Yes** | URL prefix (e.g., 'contoso' for contoso.crm.dynamics.com) |
| `CurrencyName` | string | **Yes** | Base currency (e.g., USD, EUR, CAD) |
| `LanguageName` | integer | **Yes** | LCID code (e.g., 1033 for English) |
| `AppsTemplate` | string | No | Apps to include (e.g., `D365_Sales`, `D365_CustomerService`) |

**Output:** Sets `BuildTools.EnvironmentUrl` variable for use in subsequent tasks.

**Capacity note:** Requires available capacity/license to create environments.

### Power Platform Delete Environment

Deletes an environment.

```yaml
- task: PowerPlatformDeleteEnvironment@2
  displayName: 'Delete test environment'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Admin Service Connection'
```

**Warning:** Permanently deletes environment and all data. Cannot be undone.

### Power Platform Assign User

Assigns a user to an environment with a specified security role.

```yaml
- task: PowerPlatformAssignUser@2
  displayName: 'Assign user to environment'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Production Environment'
    User: 'user@contoso.com'
    Role: 'System Administrator'
    ApplicationUser: false
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationType` | string | For SPN | `PowerPlatformSPN` or `PowerPlatformEnvironment` |
| `PowerPlatformSPN` | string | Yes* | Service connection name (SPN auth) |
| `PowerPlatformEnvironment` | string | Yes* | Service connection name (username/password auth) |
| `User` | string | **Yes** | Azure AD object ID or user principal name (UPN) |
| `Role` | string | **Yes** | Security role name or ID |
| `ApplicationUser` | boolean | No | Whether user is an application user (default: false) |

**Use cases:**
- Automatically provision users in new environments
- Assign pipeline service principals appropriate roles
- Set up test users in sandbox environments

### Power Platform Reset Environment

Resets an environment to a clean state.

```yaml
- task: PowerPlatformResetEnvironment@2
  displayName: 'Reset test environment'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Test Environment'
    CurrencyName: 'USD'
    Purpose: 'Reset to clean state'
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationType` | string | For SPN | `PowerPlatformSPN` or `PowerPlatformEnvironment` |
| `PowerPlatformSPN` | string | Yes* | Service connection name (SPN auth) |
| `PowerPlatformEnvironment` | string | Yes* | Service connection name (username/password auth) |
| `CurrencyName` | string | No | Base currency after reset |
| `Purpose` | string | No | Purpose description for the reset |
| `AppsTemplate` | string | No | Apps to include after reset |

**Warning:** Resets environment to factory defaults, deleting all data and customizations.

**Use cases:**
- Reset test environments between test runs
- Clean up temporary environments
- Restore environment to known state

### Power Platform Backup Environment

Creates backup of environment.

```yaml
- task: PowerPlatformBackupEnvironment@2
  displayName: 'Backup production'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Production Environment'
    BackupLabel: 'Pre-deployment backup $(Build.BuildNumber)'
```

### Power Platform Copy Environment

Copies environment to target environment.

```yaml
- task: PowerPlatformCopyEnvironment@2
  displayName: 'Copy production to test'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Production Environment'
    TargetEnvironmentUrl: 'https://contoso-test.crm.dynamics.com'
    CopyType: 'MinimalCopy'
    OverrideFriendlyName: true
    FriendlyName: 'Test Environment Copy'
```

**Copy types:**
- **FullCopy** - All data and metadata
- **MinimalCopy** - Metadata only (no data)

### Power Platform Restore Environment

Restores an environment from a backup.

```yaml
- task: PowerPlatformRestoreEnvironment@2
  displayName: 'Restore production from backup'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Production Environment'
    TargetEnvironmentUrl: 'https://contoso-prod.crm.dynamics.com'
    RestoreLatestBackup: true
    FriendlyName: 'Contoso Production Restored'
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------||
| `authenticationType` | string | For SPN | `PowerPlatformSPN` or `PowerPlatformEnvironment` |
| `PowerPlatformSPN` | string | Yes* | Service connection name (SPN auth) |
| `PowerPlatformEnvironment` | string | Yes* | Service connection name (username/password auth) |
| `TargetEnvironmentUrl` | string | **Yes** | Target environment URL to restore to |
| `RestoreLatestBackup` | boolean | No | Restore latest backup (true) or specify timestamp (false) |
| `RestoreTimeStamp` | string | When RestoreLatestBackup=false | DateTime in 'mm/dd/yyyy hh:mm' format or 'latest' |
| `FriendlyName` | string | No | Friendly name for restored environment |
| `DisableAdminMode` | boolean | No | Disable administration mode after restore |

**Use cases:**
- Disaster recovery
- Roll back after failed deployment
- Create point-in-time copies for testing

**Restore strategies:**
```yaml
# Restore latest backup
- task: PowerPlatformRestoreEnvironment@2
  inputs:
    RestoreLatestBackup: true

# Restore specific backup
- task: PowerPlatformRestoreEnvironment@2
  inputs:
    RestoreLatestBackup: false
    RestoreTimeStamp: '02/15/2024 14:30'
```

---

## Data Tasks

### Power Platform Export Data

Exports Dataverse data using Configuration Migration schema.

```yaml
- task: PowerPlatformExportData@2
  displayName: 'Export reference data'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Dev Environment'
    SchemaFile: '$(Build.SourcesDirectory)/Data/schema.xml'
    DataFile: '$(Build.ArtifactStagingDirectory)/data.zip'
    Overwrite: true
```

### Power Platform Import Data

Imports Dataverse data from Configuration Migration export.

```yaml
- task: PowerPlatformImportData@2
  displayName: 'Import reference data'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'QA Environment'
    DataFile: '$(Pipeline.Workspace)/drop/data.zip'
```

**Use cases:** Import reference data, test data, or migrate data between environments.

---

## Power Pages Tasks

### Power Platform Download PAPortal

Downloads Power Pages website content from a Dataverse environment.

```yaml
- task: PowerPlatformDownloadPAPortal@2
  displayName: 'Download Power Pages content'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Dev Environment'
    DownloadPath: '$(Build.SourcesDirectory)/portals/website1'
    WebsiteId: 'f88b70cc-580b-4f1a-87c3-41debefeb902'
    Overwrite: true
    ModelVersion: '2'
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationType` | string | For SPN | `PowerPlatformSPN` or `PowerPlatformEnvironment` |
| `PowerPlatformSPN` | string | Yes* | Service connection name (SPN auth) |
| `PowerPlatformEnvironment` | string | Yes* | Service connection name (username/password auth) |
| `DownloadPath` | string | **Yes** | Local path to download portal content to |
| `WebsiteId` | string | **Yes** | Power Pages website ID (GUID) |
| `Overwrite` | boolean | No | Overwrite existing files (default: false) |
| `ModelVersion` | string | No | Data model version: '1' (standard) or '2' (enhanced) |

**Use cases:**
- Version control Power Pages website content
- Export portal configurations
- Create backups of portal content

### Power Platform Upload PAPortal

Uploads Power Pages website content to a Dataverse environment.

```yaml
- task: PowerPlatformUploadPAPortal@2
  displayName: 'Upload Power Pages content'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'QA Environment'
    UploadPath: '$(Build.SourcesDirectory)/portals/website1'
    ModelVersion: '2'
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationType` | string | For SPN | `PowerPlatformSPN` or `PowerPlatformEnvironment` |
| `PowerPlatformSPN` | string | Yes* | Service connection name (SPN auth) |
| `PowerPlatformEnvironment` | string | Yes* | Service connection name (username/password auth) |
| `UploadPath` | string | **Yes** | Local path containing portal content |
| `ModelVersion` | string | No | Data model version: '1' (standard) or '2' (enhanced) |

**Use cases:**
- Deploy portal changes to environments
- Promote portal content through environments
- Automate portal deployments

**Portal CI/CD workflow:**
```yaml
# Download from dev
- task: PowerPlatformDownloadPAPortal@2
  inputs:
    PowerPlatformSPN: 'Dev'
    DownloadPath: '$(Build.ArtifactStagingDirectory)/portal'
    WebsiteId: '$(PortalWebsiteId)'

# Commit to source control
- script: |
    git add portals/
    git commit -m "Updated portal content"
    git push

# Upload to QA
- task: PowerPlatformUploadPAPortal@2
  inputs:
    PowerPlatformSPN: 'QA'
    UploadPath: '$(Pipeline.Workspace)/drop/portal'
```

---

## Catalog Tasks (Preview)

### Power Platform Install Catalog

Installs a catalog item from the Power Platform catalog to a target environment.

```yaml
- task: PowerPlatformInstallCatalog@2
  displayName: 'Install catalog item'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Production Environment'
    Environment: '$(BuildTools.EnvironmentUrl)'
    CatalogItemId: '00000000-0000-0000-0000-000000000001'
    TargetEnvironmentUrl: 'https://contoso-prod.crm.dynamics.com'
    PollStatus: true
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationType` | string | For SPN | `PowerPlatformSPN` or `PowerPlatformEnvironment` |
| `PowerPlatformSPN` | string | Yes* | Service connection name |
| `Environment` | string | **Yes** | Catalog environment URL |
| `CatalogItemId` | string | **Yes** | Catalog item ID (GUID) to install |
| `TargetEnvironmentUrl` | string | **Yes** | Target environment URL for installation |
| `PollStatus` | boolean | No | Poll for completion status |

### Power Platform Submit Catalog

Submits a solution or package to the Power Platform catalog for approval.

```yaml
- task: PowerPlatformSubmitCatalog@2
  displayName: 'Submit to catalog'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Catalog Environment'
    Environment: '$(BuildTools.EnvironmentUrl)'
    CatalogSubmissionFile: 'submission.json'
    UsePackageSolutionZipFile: true
    SolutionZipFile: '$(Build.ArtifactStagingDirectory)/solution_managed.zip'
    PollStatus: true
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationType` | string | For SPN | `PowerPlatformSPN` or `PowerPlatformEnvironment` |
| `PowerPlatformSPN` | string | Yes* | Service connection name |
| `Environment` | string | **Yes** | Catalog environment URL |
| `CatalogSubmissionFile` | string | **Yes** | Path to catalog submission JSON file |
| `UsePackageSolutionZipFile` | boolean | No | Use solution zip (true) or package (false) |
| `SolutionZipFile` | string | When UsePackageSolutionZipFile=true | Path to solution .zip file |
| `PackageFile` | string | When UsePackageSolutionZipFile=false | Path to package .dll file |
| `PollStatus` | boolean | No | Poll for completion status |

### Power Platform Catalog Status

Checks the status of a catalog install or submit request.

```yaml
- task: PowerPlatformCatalogStatus@2
  displayName: 'Check catalog status'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Catalog Environment'
    Environment: '$(BuildTools.EnvironmentUrl)'
    TrackingId: '$(CatalogTrackingId)'
    RequestType: 'Submit'
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationType` | string | For SPN | `PowerPlatformSPN` or `PowerPlatformEnvironment` |
| `PowerPlatformSPN` | string | Yes* | Service connection name |
| `Environment` | string | **Yes** | Catalog environment URL |
| `TrackingId` | string | **Yes** | Request tracking ID from previous task |
| `RequestType` | string | **Yes** | 'Install' or 'Submit' |

**Note:** Catalog tasks are currently in preview and subject to change.

---

## Common Pipeline Scenarios

### Scenario 1: Export Solution from Dev (CI)

Export unmanaged solution from dev environment on commit to main branch.

```yaml
trigger:
  branches:
    include:
    - main
  paths:
    include:
    - Solutions/**

pool:
  vmImage: 'windows-latest'

variables:
  solutionName: 'ContosoSample'
  
steps:
- task: PowerPlatformToolInstaller@2
  displayName: 'Install Power Platform Tools'

- task: PowerPlatformWhoAmi@2
  displayName: 'Verify dev connection'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Dev Environment'

- task: PowerPlatformSetSolutionVersion@2
  displayName: 'Update solution version'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Dev Environment'
    SolutionName: '$(solutionName)'
    SolutionVersionNumber: '1.0.$(Build.BuildId).0'

- task: PowerPlatformExportSolution@2
  displayName: 'Export unmanaged solution'
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Dev Environment'
    SolutionName: '$(solutionName)'
    SolutionOutputFile: '$(Build.ArtifactStagingDirectory)/$(solutionName).zip'
    AsyncOperation: true
    Managed: false

- task: PowerPlatformUnpackSolution@2
  displayName: 'Unpack solution'
  inputs:
    SolutionInputFile: '$(Build.ArtifactStagingDirectory)/$(solutionName).zip'
    SolutionTargetFolder: '$(Build.SourcesDirectory)/Solutions/$(solutionName)'
    SolutionType: Unmanaged

# Commit unpacked files back to repository
- script: |
    git config user.email "build@contoso.com"
    git config user.name "Build Pipeline"
    git add Solutions/$(solutionName)
    git commit -m "Updated solution files [skip ci]"
    git push origin HEAD:$(Build.SourceBranch)
  displayName: 'Commit solution files'
  condition: succeeded()
```

### Scenario 2: Build Managed Solution (CI)

Pack source-controlled solution into managed .zip for deployment.

```yaml
trigger:
  branches:
    include:
    - main
  paths:
    include:
    - Solutions/**

pool:
  vmImage: 'windows-latest'

variables:
  solutionName: 'ContosoSample'

steps:
- task: PowerPlatformToolInstaller@2
  displayName: 'Install Power Platform Tools'

- task: PowerPlatformPackSolution@2
  displayName: 'Pack as managed solution'
  inputs:
    SolutionSourceFolder: '$(Build.SourcesDirectory)/Solutions/$(solutionName)'
    SolutionOutputFile: '$(Build.ArtifactStagingDirectory)/$(solutionName)_managed.zip'
    SolutionType: Managed

- task: PowerPlatformChecker@2
  displayName: 'Run Solution Checker'
  inputs:
    PowerPlatformSPN: 'Checker Service Connection'
    FilesToAnalyze: '$(Build.ArtifactStagingDirectory)/**/*_managed.zip'
    RuleSet: '0ad12346-e108-40b8-a956-9a8f95ea18c9'
    ErrorLevel: 'HighIssueCount'
    ErrorThreshold: 0
  continueOnError: true

- task: PublishPipelineArtifact@1
  displayName: 'Publish solution artifact'
  inputs:
    targetPath: '$(Build.ArtifactStagingDirectory)'
    artifact: 'drop'
    publishLocation: 'pipeline'
```

### Scenario 3: Deploy to Production (CD)

Multi-stage release pipeline deploying to QA then Production with approval.

```yaml
trigger: none  # Manual or triggered by CI pipeline

pool:
  vmImage: 'windows-latest'

variables:
  solutionName: 'ContosoSample'

stages:
- stage: DeployQA
  displayName: 'Deploy to QA'
  jobs:
  - deployment: DeployQAJob
    displayName: 'Deploy to QA Environment'
    environment: 'QA'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: PowerPlatformToolInstaller@2
            displayName: 'Install Power Platform Tools'

          - task: PowerPlatformImportSolution@2
            displayName: 'Import solution to QA'
            inputs:
              authenticationType: PowerPlatformSPN
              PowerPlatformSPN: 'QA Environment'
              SolutionInputFile: '$(Pipeline.Workspace)/drop/$(solutionName)_managed.zip'
              AsyncOperation: true
              PublishWorkflows: true
              UseDeploymentSettingsFile: true
              DeploymentSettingsFile: '$(Pipeline.Workspace)/drop/deployment-qa.json'

- stage: DeployProduction
  displayName: 'Deploy to Production'
  dependsOn: DeployQA
  condition: succeeded()
  jobs:
  - deployment: DeployProdJob
    displayName: 'Deploy to Production Environment'
    environment: 'Production'
    strategy:
      runOnce:
        preDeploy:
          steps:
          - task: PowerPlatformBackupEnvironment@2
            displayName: 'Backup production'
            inputs:
              authenticationType: PowerPlatformSPN
              PowerPlatformSPN: 'Production Environment'
              BackupLabel: 'Pre-deploy $(Build.BuildNumber)'
        
        deploy:
          steps:
          - task: PowerPlatformToolInstaller@2
            displayName: 'Install Power Platform Tools'

          - task: PowerPlatformImportSolution@2
            displayName: 'Import solution to Production'
            inputs:
              authenticationType: PowerPlatformSPN
              PowerPlatformSPN: 'Production Environment'
              SolutionInputFile: '$(Pipeline.Workspace)/drop/$(solutionName)_managed.zip'
              AsyncOperation: true
              MaxAsyncWaitTime: 120
              PublishWorkflows: true
              UseDeploymentSettingsFile: true
              DeploymentSettingsFile: '$(Pipeline.Workspace)/drop/deployment-prod.json'
```

---

## Best Practices

### 1. Always Use Service Principal for Production

**Why:** Supports MFA, better security, no user license consumption

```yaml
# ✓ Good: Service Principal
inputs:
  authenticationType: PowerPlatformSPN
  PowerPlatformSPN: 'Production Service Connection'

# ✗ Avoid: Username/password in production
inputs:
  authenticationType: PowerPlatformEnvironment
  PowerPlatformEnvironment: 'User Connection'
```

### 2. Enable Async for Large Solutions

**Why:** Prevents 4-minute task timeout

```yaml
# ✓ Good: Async with sufficient wait time
- task: PowerPlatformImportSolution@2
  inputs:
    AsyncOperation: true
    MaxAsyncWaitTime: 120  # 2 hours for large solutions
```

### 3. Use Solution Checker in CI

**Why:** Catch issues early before deployment

```yaml
- task: PowerPlatformChecker@2
  displayName: 'Quality check'
  inputs:
    FilesToAnalyze: '$(Build.ArtifactStagingDirectory)/**/*.zip'
    ErrorLevel: 'HighIssueCount'
    ErrorThreshold: 0
  continueOnError: true  # Don't block build, but report issues
```

### 4. Version Solutions Automatically

**Why:** Track deployments and enable rollback

```yaml
variables:
  solutionVersion: '1.0.$(Build.BuildId).0'

steps:
- task: PowerPlatformSetSolutionVersion@2
  inputs:
    SolutionVersionNumber: '$(solutionVersion)'
```

### 5. Use Deployment Settings Files

**Why:** Environment-specific connection references and variables

```yaml
- task: PowerPlatformImportSolution@2
  inputs:
    UseDeploymentSettingsFile: true
    DeploymentSettingsFile: '$(Pipeline.Workspace)/drop/deployment-$(Environment.Name).json'
```

### 6. Backup Before Production Deployments

**Why:** Enable quick rollback if deployment fails

```yaml
- task: PowerPlatformBackupEnvironment@2
  inputs:
    BackupLabel: 'Pre-deploy $(Build.BuildNumber) $(System.TeamFoundationCollectionUri)'
```

### 7. Separate Build and Release Pipelines

**Why:** Build once, deploy many times to different environments

- **Build pipeline:** Export → Pack → Check quality → Publish artifact
- **Release pipeline:** Download artifact → Import to environment(s)

### 8. Optimize Import Performance for Managed Solutions

**Why:** Avoid options that significantly slow down the import process ([Microsoft performance recommendations](https://learn.microsoft.com/en-us/power-platform/alm/performance-recommendations))

```yaml
# ✓ Good: Fast import — default single-stage upgrade, no overwrite, no publish-all
- task: PowerPlatformImportSolution@2
  inputs:
    SolutionInputFile: '$(Pipeline.Workspace)/drop/MySolution_managed.zip'
    AsyncOperation: true
    MaxAsyncWaitTime: 120
    PublishWorkflows: true             # Activates flows/plugins only
    # OverwriteUnmanagedCustomizations: false  # Default — leave this out
    # HoldingSolution: false           # Default — single-stage is faster

# ✗ Avoid: Slow import options for managed solutions
- task: PowerPlatformImportSolution@2
  inputs:
    OverwriteUnmanagedCustomizations: true  # ❌ Significantly slows import
    HoldingSolution: true                   # ❌ Two-stage is slower than single-stage
```

**Rules for fast managed solution imports:**
- Do **not** set `OverwriteUnmanagedCustomizations: true` — enforce no unmanaged customizations in your environments instead
- Do **not** use `HoldingSolution: true` unless you specifically need to stage the upgrade
- Do **not** publish all customizations — use `PublishWorkflows: true` to activate flows and plugins
- Do **not** use `ConvertToManaged` — this option is deprecated

---

## Troubleshooting

### Authentication Failures

**Error:** "Authentication failed" or "Invalid credentials"

**Solutions:**
1. Verify service connection in Project Settings
2. Check Service Principal has correct permissions:
   - System Administrator or System Customizer role
   - Application User in target environment
3. Ensure client secret hasn't expired
4. For SPN: Verify Tenant ID, App ID, Secret all correct

### Import Timeout

**Error:** "Task timed out after 4 minutes" during import

**Solution:** Enable async operation:

```yaml
- task: PowerPlatformImportSolution@2
  inputs:
    AsyncOperation: true
    MaxAsyncWaitTime: 120  # Increase from default 60
```

### Solution Not Found

**Error:** "Solution [name] not found"

**Cause:** Using display name instead of unique name

**Solution:** Always use solution unique name (no spaces):

```yaml
# ✓ Correct: Unique name
SolutionName: 'ContosoSampleSolution'

# ✗ Wrong: Display name
SolutionName: 'Contoso Sample Solution'
```

### Checker Analysis Failed

**Error:** Checker task fails with analysis error

**Solutions:**
1. Ensure service connection points to **licensed** environment (trial or paid)
2. Check solution .zip is valid (not unpacked folder)
3. Verify geography endpoint if using custom endpoint
4. Use `continueOnError: true` to not block pipeline

### BuildTools.EnvironmentUrl Not Set

**Error:** Subsequent tasks fail with "environment URL not provided"

**Cause:** Using wrong parameter name or authentication type

**Solution:** Check task documentation for correct parameter:

```yaml
# Some tasks use PowerPlatformSPN
- task: PowerPlatformImportSolution@2
  inputs:
    authenticationType: PowerPlatformSPN
    PowerPlatformSPN: 'Connection Name'  # Not PowerPlatformEnvironment
```

---

## Cross-References

**Related skills:**
- **[export-solution](../../export-solution/SKILL.md)** - PowerShell script for pac CLI solution export
- **[dataverse-solution-parser](../../dataverse-solution-parser/SKILL.md)** - Parse and analyze solution XML files

**Official resources:**
- [Microsoft Power Platform Build Tools](https://learn.microsoft.com/en-us/power-platform/alm/devops-build-tools)
- [Build tool tasks reference](https://learn.microsoft.com/en-us/power-platform/alm/devops-build-tool-tasks)
- [Configure service connections](https://learn.microsoft.com/en-us/power-platform/alm/devops-build-tools#configure-service-connections-using-a-service-principal)
- [Deployment settings file format](https://learn.microsoft.com/en-us/power-platform/alm/conn-ref-env-variables-build-tools)
- [Power Platform ALM guide](https://learn.microsoft.com/en-us/power-platform/alm/)
- [Import solution performance recommendations](https://learn.microsoft.com/en-us/power-platform/alm/performance-recommendations)
