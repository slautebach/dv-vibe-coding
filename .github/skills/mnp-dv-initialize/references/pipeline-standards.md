# Pipeline Standards

Source: wiki/Welcome/Platform-Delivery-Playbook/Implementation-Standards/Application-Lifecycle-Management/DevOps-Pipeline-Guidance.md

## Approach: YAML Pipelines (Required)

Use **YAML pipelines** for all pipeline types. Classic Release Pipelines are not enabled by default in new Azure DevOps organizations and are in maintenance mode. All MNP Digital engagements use YAML pipelines.

## Folder Structure

```
pipelines/
├── build/          <- compile plugins, package solutions, produce deployment artifacts
├── export/         <- extract & unpack solutions, portal content, and config data
├── deploy/         <- deploy packaged artifacts to target environments
├── templates/      <- reusable YAML step templates
└── scripts/        <- PowerShell scripts invoked by pipeline steps
```

## Naming Convention

Lowercase kebab-case filenames. The folder provides context — filename describes the subject only.

```
pipelines/
├── export/
│   ├── solution.yml
│   ├── portal.yml
│   └── data.yml
├── build/
│   ├── solution.yml
│   └── solution-pr.yml
├── deploy/
│   ├── solution.yml
│   ├── portal.yml
│   └── data.yml
├── templates/
│   ├── steps-export.yml
│   ├── steps-build.yml
│   └── steps-deploy.yml
└── scripts/
    ├── update-connection-references.ps1
    ├── activate-workflows.ps1
    └── validate-deployment.ps1
```

## Pipeline Structures by Type

### Export Pipelines — Single Stage

Triggered manually or on PR. Two approaches:

**Raise a PR (recommended for team engagements):**
```yaml
# pipelines/export/solution.yml
trigger: none

stages:
- stage: Export
  jobs:
  - job: ExportSolution
    steps:
    - template: ../templates/steps-export.yml
      parameters:
        commitTarget: pullRequest
```

**Commit directly to main (solo/low-risk):**
```yaml
trigger: none

stages:
- stage: Export
  jobs:
  - job: ExportSolution
    steps:
    - template: ../templates/steps-export.yml
      parameters:
        commitTarget: main
```

### Build Pipelines — Single Stage

Triggered on merge to `main`:
```yaml
# pipelines/build/solution.yml
trigger:
- main

stages:
- stage: Build
  jobs:
  - job: BuildSolution
    steps:
    - template: ../templates/steps-build.yml
```

### Deploy Pipelines — Multi-Stage (Recommended)

```yaml
# pipelines/deploy/solution.yml
stages:
- stage: DeployDev
  jobs:
  - deployment: Deploy
    environment: DC-{Solution}-DEV
    strategy:
      runOnce:
        deploy:
          steps:
          - template: ../templates/steps-deploy.yml

- stage: DeploySIT
  dependsOn: DeployDev
  jobs:
  - deployment: Deploy
    environment: DC-{Solution}-SIT  # manual approval gate
    strategy:
      runOnce:
        deploy:
          steps:
          - template: ../templates/steps-deploy.yml

- stage: DeployUAT
  dependsOn: DeploySIT
  jobs:
  - deployment: Deploy
    environment: DC-{Solution}-UAT  # manual approval gate
    strategy:
      runOnce:
        deploy:
          steps:
          - template: ../templates/steps-deploy.yml

- stage: DeployProd
  dependsOn: DeployUAT
  jobs:
  - deployment: Deploy
    environment: DC-{Solution}-PROD  # manual approval gate
    strategy:
      runOnce:
        deploy:
          steps:
          - template: ../templates/steps-deploy.yml
```

## Agent Pool

Use `windows-2022` for Power Platform pipelines (pac CLI and PowerShell requirements):

```yaml
pool:
  vmImage: 'windows-2022'
```

## Key Variables

Common pipeline variables to define:

| Variable | Purpose |
|---|---|
| `SolutionName` | Dataverse solution unique name |
| `TargetEnvironment` | Target environment URL or org name |
| `AppId` | Service principal application ID |
| `ClientSecret` | Service principal secret (use secret variable) |
| `BuildPackageFile` | Name for the build artifact package |

## Pipeline Run Naming Convention

```yaml
name: $(pipeline-type)-$(Date:yyyyMMdd)-$(Rev:.rrr)
```

Examples:
- `CI-Build-20250101-001`
- `Export-Solution-20250101-001`
- `Deploy-Solution-20250101-001`
