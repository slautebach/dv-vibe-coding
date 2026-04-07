# Template Patterns

Comprehensive guide to Azure Pipelines templates, including template types, parameterization, multi-repo templates, and best practices.

## Table of Contents

- [Template Types](#template-types)
- [Includes Pattern](#includes-pattern)
- [Extends Pattern](#extends-pattern)
- [Template Parameters](#template-parameters)
- [Variable Templates](#variable-templates)
- [Multi-Repository Templates](#multi-repository-templates)
- [Template Expressions](#template-expressions)
- [Best Practices](#best-practices)

## Template Types

Azure Pipelines supports two template patterns:

| Pattern | Use Case | Structure |
|---------|----------|-----------|
| **Includes** | Reuse steps, jobs, or stages | Template inserts content into parent pipeline |
| **Extends** | Enforce standards, security | Parent pipeline extends template structure |

### When to Use Each

**Use Includes when:**
- Sharing common build/test/deploy steps across pipelines
- Reusing job definitions with parameters
- Creating modular, composable pipelines
- Teams want flexibility to modify pipelines

**Use Extends when:**
- Enforcing organizational standards
- Required security/compliance checks
- Protecting production deployments
- Centralized pipeline governance

## Includes Pattern

Includes insert template content into the parent pipeline at specified locations.

### Step Template

Reusable sequence of steps.

**templates/build-steps.yml:**
```yaml
parameters:
- name: buildConfiguration
  type: string
  default: 'Release'

steps:
- task: UseDotNet@2
  inputs:
    version: '8.x'

- script: dotnet restore
  displayName: 'Restore NuGet packages'

- script: dotnet build --configuration ${{ parameters.buildConfiguration }}
  displayName: 'Build solution'

- script: dotnet test --configuration ${{ parameters.buildConfiguration }}
  displayName: 'Run tests'
```

**azure-pipelines.yml:**
```yaml
trigger:
  branches:
    include:
    - main

pool:
  vmImage: 'ubuntu-latest'

steps:
- template: templates/build-steps.yml
  parameters:
    buildConfiguration: 'Release'
```

### Job Template

Reusable job definition.

**templates/build-job.yml:**
```yaml
parameters:
- name: jobName
  type: string
  default: 'Build'
- name: pool
  type: string
  default: 'ubuntu-latest'
- name: configuration
  type: string
  default: 'Release'

jobs:
- job: ${{ parameters.jobName }}
  displayName: 'Build ${{ parameters.configuration }}'
  pool:
    vmImage: ${{ parameters.pool }}
  steps:
  - script: dotnet build --configuration ${{ parameters.configuration }}
  - script: dotnet test --configuration ${{ parameters.configuration }}
```

**azure-pipelines.yml:**
```yaml
trigger:
- main

stages:
- stage: Build
  jobs:
  - template: templates/build-job.yml
    parameters:
      jobName: 'BuildRelease'
      pool: 'ubuntu-latest'
      configuration: 'Release'
  
  - template: templates/build-job.yml
    parameters:
      jobName: 'BuildDebug'
      pool: 'windows-latest'
      configuration: 'Debug'
```

### Stage Template

Reusable stage definition.

**templates/deployment-stage.yml:**
```yaml
parameters:
- name: stageName
  type: string
- name: environment
  type: string
- name: dependsOn
  type: string
  default: ''

stages:
- stage: ${{ parameters.stageName }}
  displayName: 'Deploy to ${{ parameters.environment }}'
  ${{ if ne(parameters.dependsOn, '') }}:
    dependsOn: ${{ parameters.dependsOn }}
  jobs:
  - deployment: Deploy
    environment: ${{ parameters.environment }}
    strategy:
      runOnce:
        deploy:
          steps:
          - script: echo "Deploying to ${{ parameters.environment }}"
          - task: AzureWebApp@1
            inputs:
              azureSubscription: 'MyServiceConnection'
              appName: 'myapp-${{ parameters.environment }}'
```

**azure-pipelines.yml:**
```yaml
trigger:
- main

stages:
- stage: Build
  jobs:
  - job: BuildJob
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - script: echo "Building"

- template: templates/deployment-stage.yml
  parameters:
    stageName: 'DeployDev'
    environment: 'dev'
    dependsOn: 'Build'

- template: templates/deployment-stage.yml
  parameters:
    stageName: 'DeployProd'
    environment: 'production'
    dependsOn: 'DeployDev'
```

## Extends Pattern

Extends allows a pipeline to inherit structure from a template.

### Basic Extends

**templates/base-pipeline.yml:**
```yaml
parameters:
- name: buildConfiguration
  type: string
  default: 'Release'

stages:
- stage: SecurityScan
  displayName: 'Security Scanning'
  jobs:
  - job: Scan
    steps:
    - script: echo "Running security scan"
    - script: echo "Checking for vulnerabilities"

- ${{ parameters.buildStages }}

- stage: Compliance
  displayName: 'Compliance Check'
  jobs:
  - job: ComplianceCheck
    steps:
    - script: echo "Verifying compliance"
```

**azure-pipelines.yml:**
```yaml
trigger:
- main

extends:
  template: templates/base-pipeline.yml
  parameters:
    buildConfiguration: 'Release'
    buildStages:
    - stage: Build
      jobs:
      - job: BuildJob
        pool:
          vmImage: 'ubuntu-latest'
        steps:
        - script: dotnet build --configuration Release
    
    - stage: Test
      jobs:
      - job: TestJob
        pool:
          vmImage: 'ubuntu-latest'
        steps:
        - script: dotnet test
```

**Result:** Pipeline runs stages in order: SecurityScan → Build → Test → Compliance

### Extends with Required Steps

Force specific steps to always run:

**templates/secure-pipeline.yml:**
```yaml
parameters:
- name: applicationStages
  type: stageList
  default: []

stages:
- stage: PreDeploymentValidation
  jobs:
  - job: Validate
    steps:
    - script: echo "Validating prerequisites"
    - task: ManualValidation@0
      inputs:
        instructions: 'Review and approve deployment'

- ${{ parameters.applicationStages }}

- stage: PostDeploymentTests
  jobs:
  - job: SmokeTests
    steps:
    - script: echo "Running smoke tests"
```

**azure-pipelines.yml:**
```yaml
extends:
  template: templates/secure-pipeline.yml
  parameters:
    applicationStages:
    - stage: Deploy
      jobs:
      - deployment: DeployApp
        environment: 'production'
        strategy:
          runOnce:
            deploy:
              steps:
              - script: echo "Deploying application"
```

## Template Parameters

Parameters make templates flexible and reusable.

### Parameter Types

```yaml
parameters:
# String parameter
- name: environment
  type: string
  default: 'dev'
  values:  # Optionally restrict values
  - dev
  - staging
  - production

# Boolean parameter
- name: runTests
  type: boolean
  default: true

# Number parameter
- name: retryCount
  type: number
  default: 3

# Object parameter
- name: deploymentSettings
  type: object
  default:
    timeout: 30
    retries: 3

# Array parameter (string list)
- name: environments
  type: object
  default:
  - dev
  - staging
  - prod

# Stage list parameter
- name: customStages
  type: stageList
  default: []

# Job list parameter
- name: additionalJobs
  type: jobList
  default: []

# Step list parameter
- name: buildSteps
  type: stepList
  default: []
```

### Using Parameters

```yaml
parameters:
- name: buildConfig
  type: string
  default: 'Release'

- name: platforms
  type: object
  default:
  - linux
  - windows

steps:
# String parameter
- script: dotnet build --configuration ${{ parameters.buildConfig }}

# Boolean parameter conditional
- ${{ if eq(parameters.runTests, true) }}:
  - script: dotnet test

# Iterate over array
- ${{ each platform in parameters.platforms }}:
  - script: echo "Building for ${{ platform }}"
    displayName: 'Build for ${{ platform }}'
```

### Parameter Validation

```yaml
parameters:
- name: environment
  type: string
  values:  # Only these values allowed
  - dev
  - staging
  - production

- name: deploymentType
  type: string
  default: 'standard'
  values:
  - standard
  - bluegreen
  - canary

# Use in template
steps:
- ${{ if eq(parameters.deploymentType, 'bluegreen') }}:
  - script: echo "Blue/Green deployment"
- ${{ if eq(parameters.deploymentType, 'canary') }}:
  - script: echo "Canary deployment"
- ${{ if eq(parameters.deploymentType, 'standard') }}:
  - script: echo "Standard deployment"
```

## Variable Templates

Separate variable definitions into templates.

### Basic Variable Template

**templates/variables/common.yml:**
```yaml
variables:
- name: buildConfiguration
  value: 'Release'
- name: nodeVersion
  value: '18.x'
- name: dotnetVersion
  value: '8.x'
```

**azure-pipelines.yml:**
```yaml
variables:
- template: templates/variables/common.yml

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UseDotNet@2
  inputs:
    version: $(dotnetVersion)
- script: dotnet build --configuration $(buildConfiguration)
```

### Environment-Specific Variables

**templates/variables/dev.yml:**
```yaml
variables:
- name: environment
  value: 'dev'
- name: apiUrl
  value: 'https://api-dev.example.com'
- name: databaseName
  value: 'myapp-dev'
```

**templates/variables/prod.yml:**
```yaml
variables:
- name: environment
  value: 'production'
- name: apiUrl
  value: 'https://api.example.com'
- name: databaseName
  value: 'myapp-prod'
```

**azure-pipelines.yml:**
```yaml
parameters:
- name: environment
  type: string
  default: 'dev'
  values:
  - dev
  - staging
  - production

variables:
- template: templates/variables/${{ parameters.environment }}.yml

steps:
- script: echo "Deploying to $(environment)"
- script: echo "API URL: $(apiUrl)"
```

## Multi-Repository Templates

Reference templates from other repositories.

### Setup Repository Resource

**azure-pipelines.yml:**
```yaml
resources:
  repositories:
  - repository: templates
    type: git
    name: MyProject/PipelineTemplates
    ref: refs/heads/main  # Or specific tag/branch

extends:
  template: common/secure-pipeline.yml@templates
  parameters:
    buildConfiguration: 'Release'
```

### Reference Template from Another Repo

```yaml
resources:
  repositories:
  - repository: templates
    type: git
    name: MyProject/PipelineTemplates

stages:
- stage: Build
  jobs:
  - template: jobs/build-dotnet.yml@templates
    parameters:
      configuration: 'Release'
  
- stage: Deploy
  jobs:
  - template: jobs/deploy-azure.yml@templates
    parameters:
      environment: 'production'
```

### GitHub Repository Templates

```yaml
resources:
  repositories:
  - repository: templates
    type: github
    endpoint: MyGitHubConnection
    name: myorg/pipeline-templates
    ref: refs/tags/v1.0.0  # Pin to specific version

stages:
- template: build-stage.yml@templates
```

### Template Versioning

**Best practice: Pin to specific tags**

```yaml
resources:
  repositories:
  - repository: templates
    type: git
    name: MyProject/PipelineTemplates
    ref: refs/tags/v2.1.0  # Specific version

# Or use branches for testing
resources:
  repositories:
  - repository: templates
    type: git
    name: MyProject/PipelineTemplates
    ref: refs/heads/feature/new-template
```

## Template Expressions

### Conditional Template Insertion

```yaml
parameters:
- name: runSecurityScan
  type: boolean
  default: false

- name: deployToProd
  type: boolean
  default: false

stages:
- stage: Build
  jobs:
  - job: BuildJob
    steps:
    - script: echo "Building"

- ${{ if eq(parameters.runSecurityScan, true) }}:
  - stage: SecurityScan
    jobs:
    - job: Scan
      steps:
      - script: echo "Scanning for vulnerabilities"

- ${{ if eq(parameters.deployToProd, true) }}:
  - stage: DeployProduction
    jobs:
    - deployment: DeployProd
      environment: 'production'
      strategy:
        runOnce:
          deploy:
            steps:
            - script: echo "Deploying to production"
```

### Each Loop

Iterate over collections:

```yaml
parameters:
- name: environments
  type: object
  default:
  - dev
  - staging
  - prod

stages:
- ${{ each env in parameters.environments }}:
  - stage: Deploy_${{ env }}
    displayName: 'Deploy to ${{ env }}'
    jobs:
    - deployment: Deploy
      environment: ${{ env }}
      strategy:
        runOnce:
          deploy:
            steps:
            - script: echo "Deploying to ${{ env }}"
```

**Matrix with each:**

```yaml
parameters:
- name: platforms
  type: object
  default:
  - name: Linux
    vmImage: 'ubuntu-latest'
  - name: Windows
    vmImage: 'windows-latest'
  - name: macOS
    vmImage: 'macos-latest'

jobs:
- ${{ each platform in parameters.platforms }}:
  - job: Build_${{ platform.name }}
    displayName: 'Build on ${{ platform.name }}'
    pool:
      vmImage: ${{ platform.vmImage }}
    steps:
    - script: echo "Building on ${{ platform.name }}"
```

### Conditional Steps

```yaml
parameters:
- name: buildSteps
  type: stepList
  default: []

- name: includeTests
  type: boolean
  default: true

steps:
- ${{ parameters.buildSteps }}

- ${{ if eq(parameters.includeTests, true) }}:
  - script: echo "Running tests"
  - task: VSTest@2
    inputs:
      testAssemblyVer2: '**\*test*.dll'
```

## Best Practices

### 1. Use Descriptive Parameter Names

```yaml
# ✅ Good
parameters:
- name: buildConfiguration
  type: string
- name: deployToProduction
  type: boolean

# ❌ Bad
parameters:
- name: config
  type: string
- name: deploy
  type: boolean
```

### 2. Provide Parameter Defaults

```yaml
# ✅ Good - has sensible defaults
parameters:
- name: buildConfiguration
  type: string
  default: 'Release'
- name: runTests
  type: boolean
  default: true

# ❌ Bad - no defaults, harder to use
parameters:
- name: buildConfiguration
  type: string
- name: runTests
  type: boolean
```

### 3. Document Template Parameters

```yaml
# Build template for .NET applications
#
# Parameters:
#   buildConfiguration: Build configuration (Debug/Release)
#   targetFramework: .NET target framework version
#   runTests: Whether to execute unit tests
#   publishArtifacts: Whether to publish build artifacts

parameters:
- name: buildConfiguration
  type: string
  default: 'Release'
  values:
  - Debug
  - Release

- name: targetFramework
  type: string
  default: 'net8.0'

- name: runTests
  type: boolean
  default: true

- name: publishArtifacts
  type: boolean
  default: true
```

### 4. Use Extends for Governance

When you need to enforce standards:

```yaml
# templates/secure-pipeline.yml - Enforced security checks
parameters:
- name: applicationStages
  type: stageList

stages:
- stage: SecurityGate
  jobs:
  - job: SecurityCheck
    steps:
    - task: CredScan@3
    - task: SonarQube@5

- ${{ parameters.applicationStages }}

- stage: ComplianceGate
  jobs:
  - job: ComplianceCheck
    steps:
    - task: ComplianceTask@1
```

### 5. Version Your Templates

```yaml
# Pin to specific versions in production
resources:
  repositories:
  - repository: templates
    type: git
    name: MyProject/PipelineTemplates
    ref: refs/tags/v2.0.0  # Specific version

# Use branch for development
resources:
  repositories:
  - repository: templates
    type: git
    name: MyProject/PipelineTemplates
    ref: refs/heads/develop  # Latest development version
```

### 6. Keep Templates Focused

```yaml
# ✅ Good - Single responsibility
# templates/dotnet-build.yml - Build only
# templates/dotnet-test.yml - Test only
# templates/dotnet-publish.yml - Publish only

# ❌ Bad - Doing too much
# templates/dotnet-everything.yml - Build, test, deploy, notify, etc.
```

### 7. Use Step Lists for Flexibility

```yaml
parameters:
- name: preBuildSteps
  type: stepList
  default: []
- name: postBuildSteps
  type: stepList
  default: []

steps:
- ${{ parameters.preBuildSteps }}

- script: dotnet build
  displayName: 'Build application'

- ${{ parameters.postBuildSteps }}
```

### 8. Template File Organization

```
templates/
├── stages/
│   ├── build-stage.yml
│   ├── test-stage.yml
│   └── deploy-stage.yml
├── jobs/
│   ├── build-job.yml
│   ├── test-job.yml
│   └── deploy-job.yml
├── steps/
│   ├── dotnet-build.yml
│   ├── npm-build.yml
│   └── docker-build.yml
└── variables/
    ├── dev.yml
    ├── staging.yml
    └── prod.yml
```

### 9. Error Handling in Templates

```yaml
parameters:
- name: environment
  type: string
  values:
  - dev
  - staging
  - production

steps:
- script: |
    if [ -z "$ENVIRONMENT" ]; then
      echo "##vso[task.logissue type=error]Environment not specified"
      exit 1
    fi
    echo "Deploying to $ENVIRONMENT"
  env:
    ENVIRONMENT: ${{ parameters.environment }}
  displayName: 'Validate and deploy'
```

### 10. Testing Templates

Create test pipelines for templates:

**test-build-template.yml:**
```yaml
# Test pipeline for build template

trigger: none  # Manual only

extends:
  template: templates/build-template.yml
  parameters:
    buildConfiguration: 'Debug'
    runTests: true
```

## Common Template Patterns

### Multi-Environment Deployment

```yaml
parameters:
- name: environments
  type: object
  default:
  - name: dev
    requiresApproval: false
  - name: staging
    requiresApproval: false
  - name: production
    requiresApproval: true

stages:
- stage: Build
  jobs:
  - job: BuildJob
    steps:
    - script: echo "Building"

- ${{ each env in parameters.environments }}:
  - stage: Deploy_${{ env.name }}
    dependsOn: Build
    jobs:
    - deployment: Deploy
      environment: ${{ env.name }}
      ${{ if eq(env.requiresApproval, true) }}:
        # Environment will have manual approval configured in Azure DevOps
      strategy:
        runOnce:
          deploy:
            steps:
            - script: echo "Deploying to ${{ env.name }}"
```

### Conditional Job Insertion

```yaml
parameters:
- name: runPerformanceTests
  type: boolean
  default: false

stages:
- stage: Test
  jobs:
  - job: UnitTests
    steps:
    - script: echo "Running unit tests"
  
  - ${{ if eq(parameters.runPerformanceTests, true) }}:
    - job: PerformanceTests
      steps:
      - script: echo "Running performance tests"
```

### Template with Multiple Artifacts

```yaml
parameters:
- name: artifacts
  type: object
  default:
  - name: 'webapp'
    path: '$(Build.ArtifactStagingDirectory)/webapp'
  - name: 'api'
    path: '$(Build.ArtifactStagingDirectory)/api'

steps:
- ${{ each artifact in parameters.artifacts }}:
  - task: PublishPipelineArtifact@1
    displayName: 'Publish ${{ artifact.name }}'
    inputs:
      targetPath: ${{ artifact.path }}
      artifactName: ${{ artifact.name }}
```

## Quick Reference

### Template Types

```yaml
# Step template
steps:
- template: templates/steps.yml

# Job template
jobs:
- template: templates/job.yml

# Stage template
stages:
- template: templates/stage.yml

# Extends
extends:
  template: templates/base.yml
```

### Parameter Syntax

```yaml
# Define parameters
parameters:
- name: myParam
  type: string
  default: 'value'

# Use parameters (compile-time)
${{ parameters.myParam }}

# Conditional
${{ if eq(parameters.myParam, 'value') }}:
  - script: echo "Matched"

# Loop
${{ each item in parameters.items }}:
  - script: echo "${{ item }}"
```

### Multi-Repo Reference

```yaml
resources:
  repositories:
  - repository: templates
    type: git
    name: Project/Repo

# Use template
- template: file.yml@templates
```
