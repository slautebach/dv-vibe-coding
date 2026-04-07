---
name: authoring-azure-devops-pipelines
description: Expert guidance for authoring and maintaining Azure DevOps YAML pipelines. Use when working with pipeline syntax, structure, CI/CD implementation, debugging, trigger configuration, templates, deployment strategies, variable management, troubleshooting pipeline errors, Power Platform solution deployments, or Dynamics 365/Dataverse CI/CD. Do NOT use for exporting D365 solutions (use export-solution skill) or parsing solution XML files (use dataverse-solution-parser skill).
---

# Azure DevOps Pipelines Expert

Expert guidance for authoring and maintaining Azure DevOps YAML pipelines covering syntax, structure, troubleshooting, and CI/CD patterns.

## Core Concepts

### Pipeline Hierarchy

```
Pipeline
└── Stages (logical boundaries, e.g., Build, Test, Deploy)
    └── Jobs (units of work executed on an agent)
        └── Steps (individual tasks or scripts)
```

### Agent Types

| Type                 | Description                         | Use For                                          |
| -------------------- | ----------------------------------- | ------------------------------------------------ |
| **Microsoft-hosted** | Pre-configured VMs managed by Azure | Standard builds, no special requirements         |
| **Self-hosted**      | Your own machines/VMs               | Custom tools, network access, persistent caching |

**Specify agent:**

```yaml
pool:
  vmImage: "ubuntu-latest" # Microsoft-hosted
  # OR
  name: "MyAgentPool" # Self-hosted
```

## Variable Syntax Quick Reference

Azure Pipelines has THREE variable syntaxes with different evaluation times:

| Syntax                 | When Evaluated       | Use For                                    |
| ---------------------- | -------------------- | ------------------------------------------ |
| `$(var)`               | Before job execution | Task inputs, script parameters             |
| `${{ variables.var }}` | Pipeline compilation | Template parameters, conditional insertion |
| `$[variables.var]`     | Runtime              | Conditions, dependency expressions         |

Use macro `$()` for task inputs, template `${{}}` for compile-time decisions, and runtime `$[]` for conditions. **For comprehensive variable guidance, output variables, cross-job/stage passing, and secret handling, see [variable-syntax-guide.md](references/variable-syntax-guide.md).**

## Common Pipeline Patterns

### 1. Basic CI Pipeline

```yaml
trigger:
  branches:
    include:
      - main
      - develop

pool:
  vmImage: "ubuntu-latest"

variables:
  buildConfiguration: "Release"

steps:
  - task: UseDotNet@2
    displayName: "Install .NET SDK"
    inputs:
      version: "8.x"

  - script: dotnet restore
    displayName: "Restore dependencies"

  - script: dotnet build --configuration $(buildConfiguration)
    displayName: "Build project"

  - script: dotnet test --configuration $(buildConfiguration) --logger trx
    displayName: "Run tests"

  - task: PublishTestResults@2
    displayName: "Publish test results"
    inputs:
      testResultsFormat: "VSTest"
      testResultsFiles: "**/*.trx"
```

### 2. Multi-Stage Deployment Pipeline

```yaml
trigger:
  branches:
    include:
      - main

stages:
  - stage: Build
    displayName: "Build Application"
    jobs:
      - job: BuildJob
        pool:
          vmImage: "ubuntu-latest"
        steps:
          - script: echo "Building..."
          - script: echo "##vso[task.setvariable variable=buildNumber;isOutput=true]$(Build.BuildId)"
            name: outputVars

  - stage: DeployDev
    displayName: "Deploy to Dev"
    dependsOn: Build
    condition: succeeded()
    jobs:
      - deployment: DeployDevJob
        environment: "Development"
        strategy:
          runOnce:
            deploy:
              steps:
                - script: echo "Deploying to Dev..."

  - stage: DeployProd
    displayName: "Deploy to Production"
    dependsOn: DeployDev
    condition: succeeded()
    jobs:
      - deployment: DeployProdJob
        environment: "Production"
        strategy:
          runOnce:
            deploy:
              steps:
                - script: echo "Deploying to Production..."
```

### 3. Template Usage (Include Pattern)

**azure-pipelines.yml:**

```yaml
trigger:
  branches:
    include:
      - main

stages:
  - stage: Build
    jobs:
      - template: templates/build-job.yml
        parameters:
          buildConfiguration: "Release"
          runTests: true
```

**templates/build-job.yml:**

```yaml
parameters:
  - name: buildConfiguration
    type: string
    default: "Debug"
  - name: runTests
    type: boolean
    default: false

jobs:
  - job: Build
    pool:
      vmImage: "ubuntu-latest"
    steps:
      - script: dotnet build --configuration ${{ parameters.buildConfiguration }}
        displayName: "Build"

      - ${{ if eq(parameters.runTests, true) }}:
          - script: dotnet test
            displayName: "Test"
```

### 4. Conditional Execution

```yaml
stages:
  - stage: Build
    jobs:
      - job: BuildJob
        steps:
          - script: echo "Building"

  # Only run if branch is main
  - stage: Deploy
    condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
    dependsOn: Build
    jobs:
      - job: DeployJob
        steps:
          - script: echo "Deploying"

  # Run on success or partial success
  - stage: Notify
    condition: in(dependencies.Deploy.result, 'Succeeded', 'SucceededWithIssues')
    dependsOn: Deploy
    jobs:
      - job: NotifyJob
        steps:
          - script: echo "Sending notification"
```

## Trigger Types

| Type          | YAML Key                | Use For                                 |
| ------------- | ----------------------- | --------------------------------------- |
| **CI (Push)** | `trigger:`              | Continuous integration on code push     |
| **PR**        | `pr:`                   | Pull request validation                 |
| **Scheduled** | `schedules:`            | Nightly builds, periodic tasks          |
| **Pipeline**  | `resources: pipelines:` | Trigger when another pipeline completes |

**Examples:**

```yaml
# CI Trigger with branch and path filters
trigger:
  branches:
    include:
      - main
      - release/*
    exclude:
      - experimental/*
  paths:
    include:
      - src/*
    exclude:
      - docs/*

# PR Trigger
pr:
  branches:
    include:
      - main
  paths:
    exclude:
      - "*.md"

# Scheduled Trigger (cron)
schedules:
  - cron: "0 0 * * *" # Midnight UTC
    displayName: "Nightly build"
    branches:
      include:
        - main
    always: true # Run even if no code changes
```

**For comprehensive trigger configuration, see [triggers-reference.md](references/triggers-reference.md).**

## Troubleshooting Quick Reference

Common issues when authoring Azure Pipelines:

- **Variable Not Found or Empty** - Wrong syntax context (macro `$()` vs template `${{}}` vs runtime `$[]`)
- **Cross-Job Variables Empty** - Missing `dependsOn:` declaration or incorrect output variable syntax `$[dependencies.JobName.outputs['stepName.varName']]`
- **Conditions Not Working** - Using macro syntax in conditions instead of runtime `$[]`, or not overriding default `succeeded()` condition
- **Template Parameter Errors** - Wrong parameter path, missing parameter definition, or using macro syntax `$()` instead of template `${{}}` for parameters
- **Deployment Job Fails** - Missing `strategy:` block or placing steps directly under deployment instead of under `strategy.runOnce.deploy`

**For detailed solutions, code examples, and debugging techniques**, see [common-troubleshooting.md](references/common-troubleshooting.md).

## Power Platform Build Tools

Microsoft Power Platform Build Tools provides Azure DevOps tasks for automating Dynamics 365/Dataverse solution deployments and environment management.

**Install extension:** [Azure DevOps Marketplace](https://marketplace.visualstudio.com/items?itemName=microsoft-IsvExpTools.PowerPlatform-BuildTools)

**Key Tasks:**

- **PowerPlatformToolInstaller** - Install pac CLI (required first step)
- **PowerPlatformExportSolution** - Export solutions from environment
- **PowerPlatformImportSolution** - Import solutions to environment
- **PowerPlatformPackSolution** - Pack source files into .zip
- **PowerPlatformUnpackSolution** - Unpack .zip to source files
- **PowerPlatformChecker** - Solution quality analysis
- **PowerPlatformSetSolutionVersion** - Automate version numbering

**Quick Start:**

```yaml
steps:
  - task: PowerPlatformToolInstaller@2 # Required first

  - task: PowerPlatformExportSolution@2
    inputs:
      authenticationType: PowerPlatformSPN
      PowerPlatformSPN: "Dev Environment"
      SolutionName: "MySolution"
      SolutionOutputFile: "$(Build.ArtifactStagingDirectory)/solution.zip"
      AsyncOperation: true # Prevents timeout on large solutions
```

**Service Connection:** Use Service Principal authentication (supports MFA). Create connection at **Project Settings** > **Service connections** > **Power Platform**.

**For comprehensive task reference, complete pipeline examples, parameters, and troubleshooting**, see [powerplatform-build-tools.md](references/powerplatform-build-tools.md).

**Related skills:**

- **[export-solution](../export-solution/SKILL.md)** - PowerShell pac CLI solution export
- **[dataverse-solution-parser](../dataverse-solution-parser/SKILL.md)** - Parse solution XML files

## Reference Documentation

For deep-dive topics, consult these references:

- **[variable-syntax-guide.md](references/variable-syntax-guide.md)** - All three variable syntaxes, output variables, cross-job/stage passing, secret handling
- **[expressions-functions.md](references/expressions-functions.md)** - Expression functions (succeeded, failed, eq, ne, and, or, etc.), conditional operators
- **[template-patterns.md](references/template-patterns.md)** - Template types (includes vs extends), parameterization, multi-repo templates, best practices
- **[deployment-strategies.md](references/deployment-strategies.md)** - Deployment jobs, runOnce/rolling/canary strategies, lifecycle hooks, environments
- **[triggers-reference.md](references/triggers-reference.md)** - CI triggers, PR triggers, scheduled triggers, pipeline triggers, branch/path filters
- **[common-troubleshooting.md](references/common-troubleshooting.md)** - Error patterns, debugging techniques, validation checklist
- **[powerplatform-build-tools.md](references/powerplatform-build-tools.md)** - Power Platform Build Tools tasks, Dynamics 365/Dataverse solution deployments, environment management, quality checks

## Additional Resources

**Official Microsoft Documentation:**

- [YAML Schema Reference](https://learn.microsoft.com/en-us/azure/devops/pipelines/yaml-schema/?view=azure-pipelines)
- [Key Pipeline Concepts](https://learn.microsoft.com/en-us/azure/devops/pipelines/get-started/key-pipelines-concepts?view=azure-devops)
- [Expression Syntax](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/expressions?view=azure-devops)
- [Variables](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/variables?view=azure-devops)
- [Templates](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/templates?view=azure-devops)
- [Tasks Index](https://learn.microsoft.com/en-us/azure/devops/pipelines/tasks/reference/?view=azure-devops)

```

```
