# Common Troubleshooting

Comprehensive troubleshooting guide for Azure Pipelines with error patterns, solutions, and debugging techniques.

## Table of Contents

- [YAML Syntax Errors](#yaml-syntax-errors)
- [Variable Issues](#variable-issues)
- [Template Errors](#template-errors)
- [Agent and Pool Issues](#agent-and-pool-issues)
- [Authentication Errors](#authentication-errors)
- [Artifact Issues](#artifact-issues)
- [Condition and Expression Errors](#condition-and-expression-errors)
- [Deployment Job Issues](#deployment-job-issues)
- [Performance Issues](#performance-issues)
- [Debugging Techniques](#debugging-techniques)

## YAML Syntax Errors

### Indentation Errors

**Error:** "Unexpected value" or "Mapping values are not allowed here"

**Cause:** Incorrect YAML indentation

```yaml
# ❌ Wrong - Inconsistent indentation
steps:
- script: echo "Step 1"
  - script: echo "Step 2"  # Too many spaces

# ✅ Correct - Consistent 2-space indentation
steps:
- script: echo "Step 1"
- script: echo "Step 2"
```

**Fix:**
- Use consistent 2-space indentation
- Don't mix spaces and tabs
- Align list items (`-`) consistently

### Reserved Keywords

**Error:** "Unexpected value 'on'" or similar

**Cause:** Using YAML reserved keywords without quotes

```yaml
# ❌ Wrong - 'on' is reserved
variables:
  on: true

# ✅ Correct - Quote reserved keywords
variables:
  "on": true
  # Other reserved: yes, no, true, false, null
```

### String Escaping

**Error:** Character sequences interpreted incorrectly

```yaml
# ❌ Wrong - Colon requires quotes
displayName: Deploy to: Production

# ✅ Correct - Quote strings with special chars
displayName: 'Deploy to: Production'

# ❌ Wrong - Dollar sign needs escaping
script: echo ${{ variables.path }}

# ✅ Correct - Use single quotes or escape
script: echo '${{ variables.path }}'
```

### List vs Object Confusion

```yaml
# ❌ Wrong - Mixing list and object syntax
jobs:
  job: BuildJob  # Object syntax
  - job: TestJob  # List syntax

# ✅ Correct - Use list syntax for multiple items
jobs:
- job: BuildJob
- job: TestJob

# ✅ Correct - Use object syntax for single item
jobs:
  job: BuildJob
```

## Variable Issues

### Variable Not Found

**Error:** Variable evaluates to empty or literal `$(variableName)`

**Diagnose:**
```yaml
steps:
- script: |
    echo "Variable value: $(myVar)"
    echo "Variable name: myVar"
  displayName: 'Debug variable'
```

**Common causes:**

1. **Wrong scope:**
```yaml
# ❌ Variable defined in different job
jobs:
- job: JobA
  variables:
    myVar: 'value'
- job: JobB
  steps:
  - script: echo $(myVar)  # Empty - not in scope

# ✅ Define at pipeline level
variables:
  myVar: 'value'
```

2. **Wrong syntax for output variables:**
```yaml
# ❌ Wrong - Using macro syntax
variables:
  myVar: $(dependencies.JobA.outputs['step.var'])

# ✅ Correct - Using runtime syntax
variables:
  myVar: $[ dependencies.JobA.outputs['step.var'] ]
```

3. **Variable not set yet:**
```yaml
# ❌ Wrong - Variable used before it's set
- script: echo $(buildVersion)
- script: echo "##vso[task.setvariable variable=buildVersion]1.0"

# ✅ Correct - Set before use
- script: echo "##vso[task.setvariable variable=buildVersion]1.0"
- script: echo $(buildVersion)
```

### Secret Variable Not Working

**Error:** Secret variable empty or not available

**Fix:**
```yaml
# ❌ Wrong - Secrets not auto-exported to environment
- script: echo $MY_SECRET

# ✅ Correct - Explicitly map secret to env var
- script: echo $MY_SECRET
  env:
    MY_SECRET: $(MySecret)

# ✅ Correct - Use macro syntax in script
- script: echo $(MySecret)  # Masked as ***
```

### Cross-Job Variable Issues

**Error:** Output variable from another job is empty

**Diagnose:**
```yaml
- job: JobA
  steps:
  - script: echo "##vso[task.setvariable variable=myVar;isOutput=true]value"
    name: outputStep
  # Echo to verify it was set
  - script: echo "Value set: $(outputStep.myVar)"

- job: JobB
  dependsOn: JobA
  variables:
    fromA: $[ dependencies.JobA.outputs['outputStep.myVar'] ]
  steps:
  - script: |
      echo "Value: $(fromA)"
      echo "Raw: $[ dependencies.JobA.outputs['outputStep.myVar'] ]"
```

**Common fixes:**
1. Ensure step has `name:` property
2. Use correct syntax: `$[ dependencies.JobName.outputs['stepName.variableName'] ]`
3. Verify `dependsOn:` is set
4. Check for typos in job/step/variable names

## Template Errors

### Template Not Found

**Error:** "File not found" or "Template could not be found"

**Diagnose:**
```yaml
# Check path is correct relative to pipeline file
- template: templates/build.yml  # Looks in templates/ folder
- template: ../shared/build.yml  # Looks in parent folder
```

**Fixes:**
```yaml
# ✅ Relative to repository root
- template: /templates/build.yml

# ✅ Relative to current file
- template: ./templates/build.yml

# ✅ From another repository
resources:
  repositories:
  - repository: templates
    type: git
    name: MyProject/Templates

- template: build.yml@templates
```

### Parameter Type Mismatch

**Error:** "Expected X, got Y" or "Cannot convert"

```yaml
# Template definition
parameters:
- name: buildConfig
  type: string  # Expects string

# ❌ Wrong - Passing boolean
- template: build.yml
  parameters:
    buildConfig: true

# ✅ Correct - Pass string
- template: build.yml
  parameters:
    buildConfig: 'Release'
```

### Template Parameter Not Defined

**Error:** "Parameter 'X' is not defined"

```yaml
# ❌ Wrong - Using parameter that doesn't exist in template
- template: build.yml
  parameters:
    unknownParam: 'value'

# ✅ Correct - Check template definition
# templates/build.yml:
parameters:
- name: buildConfig
  type: string

# Pass correct parameter
- template: build.yml
  parameters:
    buildConfig: 'Release'
```

### Wrong Syntax for Template Parameters

**Error:** Parameter evaluates incorrectly

```yaml
parameters:
- name: environment
  type: string

# ❌ Wrong - Using macro syntax
steps:
- script: echo $(environment)

# ✅ Correct - Use template syntax for parameters
steps:
- script: echo "${{ parameters.environment }}"
```

## Agent and Pool Issues

### No Agent Found

**Error:** "No agent could be found" or pipeline queued indefinitely

**Causes:**
1. **Pool doesn't exist:**
```yaml
# ❌ Wrong - Typo in pool name
pool:
  name: 'MyAgenPool'  # Typo

# ✅ Correct
pool:
  name: 'MyAgentPool'
```

2. **No agents online:**
- Check: Azure DevOps → Project Settings → Agent pools → Select pool
- Verify agents are online
- Check agent capabilities match demands

3. **Parallel job limit reached:**
- Check: Organization Settings → Pipelines → Parallel jobs
- Verify available Microsoft-hosted or self-hosted parallelism

4. **Agent demands not met:**
```yaml
# ❌ Agent doesn't have required capability
pool:
  name: 'Default'
  demands:
  - npm
  - docker  # Agent might not have Docker

# ✅ Check agent capabilities first
# Or use Microsoft-hosted agents with tools pre-installed
pool:
  vmImage: 'ubuntu-latest'
```

### Wrong Agent Image

**Error:** "The image 'X' does not exist" or task failures

```yaml
# ❌ Wrong - Old or incorrect image name
pool:
  vmImage: 'ubuntu-16.04'  # Deprecated

# ✅ Correct - Use current image names
pool:
  vmImage: 'ubuntu-latest'  # or ubuntu-22.04, ubuntu-20.04

# Other valid images:
# - windows-latest, windows-2022, windows-2019
# - macos-latest, macos-13, macos-12
```

**Current images:** https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/hosted

### Tool Not Found on Agent

**Error:** "Command not found" or "X is not recognized"

**Fixes:**
```yaml
# ✅ Install tool before use
steps:
- task: UseDotNet@2
  inputs:
    version: '8.x'

- task: NodeTool@0
  inputs:
    versionSpec: '18.x'

- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.11'

# ✅ For self-hosted agents, install tools manually or use container jobs
jobs:
- job: Build
  container: mcr.microsoft.com/dotnet/sdk:8.0
  steps:
  - script: dotnet build
```

## Authentication Errors

### Service Connection Not Found

**Error:** "Could not find service connection" or "Unauthorized"

**Fixes:**
1. Verify service connection exists: Project Settings → Service connections
2. Check service connection name matches exactly (case-sensitive)
3. Ensure pipeline has permission to use service connection
4. Grant access: Service connection → ... → Security → Add pipeline

```yaml
# ✅ Correct - Exact name from service connections
- task: AzureWebApp@1
  inputs:
    azureSubscription: 'MyAzureConnection'  # Exact name
```

### Permission Denied

**Error:** "Access denied" or "403 Forbidden"

**Common causes:**
1. **Pipeline doesn't have repo access:**
   - Project Settings → Repositories → Select repo → Security
   - Grant "Project Collection Build Service" access

2. **Environment protection:**
   - Pipelines → Environments → Select environment → Approvals and checks
   - Configure approvals or remove restrictions

3. **Service principal permissions:**
   - Azure Portal → Subscription/Resource Group → Access Control (IAM)
   - Grant required role to service principal

### Token Authentication Failed

**Error:** "Authentication failed" with System.AccessToken

```yaml
# ❌ Wrong - Token not mapped
- script: git push origin main

# ✅ Correct - Map System.AccessToken
- script: git push origin main
  env:
    SYSTEM_ACCESSTOKEN: $(System.AccessToken)

# Configure git credentials
- script: |
    git config --global user.email "pipeline@azuredevops.com"
    git config --global user.name "Azure Pipeline"
    git remote set-url origin https://${SYSTEM_ACCESSTOKEN}@dev.azure.com/org/project/_git/repo
  env:
    SYSTEM_ACCESSTOKEN: $(System.AccessToken)
```

**Enable script access to OAuth token:**
- Pipeline → Edit → ... → Triggers → YAML → Get sources → Check "Allow scripts to access OAuth token"

## Artifact Issues

### Artifact Not Published

**Error:** Artifact not found in later stage/job

**Diagnose:**
```yaml
# Verify artifact was published
- task: PublishPipelineArtifact@1
  inputs:
    targetPath: '$(Build.ArtifactStagingDirectory)'
    artifactName: 'drop'
  displayName: 'Publish artifacts'

# Check publish task output for "Artifact 'drop' has been published"
```

**Common issues:**
1. **Empty publish path:**
```yaml
# ❌ Nothing staged - publish path is empty
- task: PublishPipelineArtifact@1
  inputs:
    targetPath: '$(Build.ArtifactStagingDirectory)'

# ✅ Copy files to staging first
- task: CopyFiles@2
  inputs:
    contents: '**'
    targetFolder: '$(Build.ArtifactStagingDirectory)'

- task: PublishPipelineArtifact@1
  inputs:
    targetPath: '$(Build.ArtifactStagingDirectory)'
```

2. **Download uses wrong name:**
```yaml
# Published as 'drop'
- task: PublishPipelineArtifact@1
  inputs:
    artifactName: 'drop'

# ❌ Wrong name
- task: DownloadPipelineArtifact@2
  inputs:
    artifactName: 'build'  # Doesn't match

# ✅ Correct name
- task: DownloadPipelineArtifact@2
  inputs:
    artifactName: 'drop'
```

### Artifact Download Fails

**Error:** "Artifact does not exist" or "Not found"

**Fixes:**
```yaml
# ✅ Download from current pipeline
- download: current
  artifact: drop

# ✅ Download from pipeline resource
resources:
  pipelines:
  - pipeline: buildPipeline
    source: Build-Pipeline-Name

- download: buildPipeline
  artifact: drop

# ✅ Download specific artifacts
- task: DownloadPipelineArtifact@2
  inputs:
    source: 'current'
    artifact: 'drop'
    path: '$(Pipeline.Workspace)/artifacts'
```

## Condition and Expression Errors

### Condition Always False

**Error:** Stage/job/step never runs

**Diagnose:**
```yaml
# Add debug output
- script: |
    echo "Build.SourceBranch: $(Build.SourceBranch)"
    echo "Build.Reason: $(Build.Reason)"
  displayName: 'Debug condition variables'

- script: echo "Running conditional step"
  condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
```

**Common issues:**
1. **Wrong branch format:**
```yaml
# ❌ Wrong - Missing refs/heads/
condition: eq(variables['Build.SourceBranch'], 'main')

# ✅ Correct - Full ref
condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')

# ✅ Or use branch name only
condition: eq(variables['Build.SourceBranchName'], 'main')
```

2. **Wrong syntax:**
```yaml
# ❌ Wrong - Using macro in condition
condition: eq($(myVar), 'value')

# ✅ Correct - Use runtime expression
condition: eq(variables['myVar'], 'value')
```

3. **Case sensitivity:**
```yaml
# ❌ Might fail - case mismatch
condition: eq(variables['myVar'], 'Value')

# ✅ Better - Use lower() for case-insensitive
condition: eq(lower(variables['myVar']), 'value')
```

### Condition Syntax Error

**Error:** "Unexpected token" or "Invalid expression"

```yaml
# ❌ Wrong - Missing quotes
condition: eq(variables['myVar'], value)

# ✅ Correct - Quote string values
condition: eq(variables['myVar'], 'value')

# ❌ Wrong - Wrong parentheses
condition: and(succeeded(), eq(variables['myVar'], 'value'))

# ✅ Correct - Proper nesting
condition: and(succeeded(), eq(variables['myVar'], 'value'))

# ❌ Wrong - Invalid function name
condition: equals(variables['myVar'], 'value')

# ✅ Correct - Use 'eq'
condition: eq(variables['myVar'], 'value')
```

## Deployment Job Issues

### Missing Strategy Block

**Error:** "Deployment strategy is required"

```yaml
# ❌ Wrong - No strategy
jobs:
- deployment: Deploy
  environment: 'production'
  steps:
  - script: echo "Deploying"

# ✅ Correct - Has strategy
jobs:
- deployment: Deploy
  environment: 'production'
  strategy:
    runOnce:
      deploy:
        steps:
        - script: echo "Deploying"
```

### Steps in Wrong Location

**Error:** "Unexpected value 'steps'"

```yaml
# ❌ Wrong - Steps directly under deployment
jobs:
- deployment: Deploy
  environment: 'production'
  strategy:
    runOnce:
  steps:  # Wrong location
  - script: echo "Deploying"

# ✅ Correct - Steps inside deploy hook
jobs:
- deployment: Deploy
  environment: 'production'
  strategy:
    runOnce:
      deploy:
        steps:
        - script: echo "Deploying"
```

### Output Variable Syntax Error

**Error:** Output variable from deployment job is empty

```yaml
# ❌ Wrong - Missing job name repetition
- deployment: DeployJob
  strategy:
    runOnce:
      deploy:
        steps:
        - script: echo "##vso[task.setvariable variable=x;isOutput=true]val"
          name: setVar  # Wrong - should match job name

# ✅ Correct - Step name matches job name
- deployment: DeployJob
  strategy:
    runOnce:
      deploy:
        steps:
        - script: echo "##vso[task.setvariable variable=x;isOutput=true]val"
          name: DeployJob  # Matches deployment job name

# Access in another job
- job: UseIt
  dependsOn: DeployJob
  variables:
    myVar: $[ dependencies.DeployJob.outputs['DeployJob.DeployJob.x'] ]
```

## Performance Issues

### Slow Pipeline Starts

**Causes:**
1. **Too many triggers firing**
2. **Agent pool queue buildup**
3. **Waiting for approval**

**Fixes:**
```yaml
# Reduce unnecessary builds
trigger:
  batch: true  # Batch rapid commits
  paths:
    exclude:
    - docs/**
    - '**/*.md'

pr:
  autoCancel: true  # Cancel outdated PR builds
```

### Long-Running Jobs

**Optimize:**
```yaml
# Use caching
- task: Cache@2
  inputs:
    key: 'nuget | "$(Agent.OS)" | **/packages.lock.json'
    path: $(NUGET_PACKAGES)
  displayName: 'Cache NuGet packages'

# Parallelize jobs
jobs:
- job: Test_Windows
- job: Test_Linux
- job: Test_macOS

# Use matrix strategy
jobs:
- job: Test
  strategy:
    matrix:
      Python37:
        python.version: '3.7'
      Python38:
        python.version: '3.8'
      Python39:
        python.version: '3.9'
```

### Checkout Taking Too Long

**Optimize:**
```yaml
# Shallow checkout
- checkout: self
  fetchDepth: 1  # Only latest commit

# Skip checkout if not needed
steps:
- checkout: none
- script: echo "No source code needed"

# Checkout submodules only if needed
- checkout: self
  submodules: false  # Skip submodules
```

## Debugging Techniques

### Enable System Diagnostics

Add to pipeline run:
- Queue pipeline → Variables → Add variable
- Name: `System.Debug`
- Value: `true`

**Output:** Verbose logging of all pipeline operations

### Debug Variables

```yaml
- script: |
    echo "=== Build Variables ==="
    echo "Build.BuildId: $(Build.BuildId)"
    echo "Build.BuildNumber: $(Build.BuildNumber)"
    echo "Build.SourceBranch: $(Build.SourceBranch)"
    echo "Build.SourceBranchName: $(Build.SourceBranchName)"
    echo "Build.Reason: $(Build.Reason)"
    echo "Build.Repository.Name: $(Build.Repository.Name)"
    echo "=== Agent Variables ==="
    echo "Agent.OS: $(Agent.OS)"
    echo "Agent.MachineName: $(Agent.MachineName)"
    echo "=== Custom Variables ==="
    echo "myVar: $(myVar)"
  displayName: 'Debug: Print variables'
```

### Test Conditions

```yaml
- script: echo "Testing condition..."
  displayName: 'Debug: Show values for condition'

- script: |
    echo "Build.SourceBranch: $(Build.SourceBranch)"
    echo "Expected: refs/heads/main"
    if [ "$(Build.SourceBranch)" = "refs/heads/main" ]; then
      echo "MATCH"
    else
      echo "NO MATCH"
    fi
  displayName: 'Debug: Test branch condition'

- script: echo "Condition passed!"
  condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
  displayName: 'Conditional step'
```

### Inspect Files and Directories

```yaml
- script: |
    echo "=== Current Directory ==="
    pwd
    echo "=== Directory Contents ==="
    ls -la
    echo "=== Build Directory ==="
    ls -la $(Build.ArtifactStagingDirectory)
  displayName: 'Debug: Inspect directories'

# Windows
- powershell: |
    Write-Host "=== Current Directory ==="
    Get-Location
    Write-Host "=== Directory Contents ==="
    Get-ChildItem
  displayName: 'Debug: Inspect directories (Windows)'
```

### Test Template Parameters

```yaml
# In template
parameters:
- name: environment
  type: string

steps:
- script: echo "Parameter value: ${{ parameters.environment }}"
  displayName: 'Debug: Show parameter'

- script: |
    echo "All parameters:"
    echo ${{ parameters }}
  displayName: 'Debug: Show all parameters'
```

### Validate YAML Locally

Use Azure Pipelines extension for VS Code:
- Install: "Azure Pipelines" extension
- Right-click pipeline file → "Azure Pipelines: Validate"
- Or use: [Pipelines YAML validator](https://marketplace.visualstudio.com/items?itemName=ms-azure-devops.azure-pipelines)

## Validation Checklist

Before troubleshooting, verify:

- [ ] YAML syntax is valid (consistent indentation, no tabs)
- [ ] Variable names match exactly (case-sensitive in some contexts)
- [ ] Job/step names are unique within their scope
- [ ] Template paths are correct
- [ ] Service connections exist and have permissions
- [ ] Agent pool has online agents
- [ ] Parallel job limits not exceeded
- [ ] All required parameters provided to templates
- [ ] Conditions use correct syntax ($[ ] for expressions, not $( ))
- [ ] Output variables have `isOutput=true` flag
- [ ] Deployment jobs have proper strategy block
- [ ] Branch names use full refs (refs/heads/main) in conditions

## Getting Help

1. **Check logs:** Click on failed step for detailed output
2. **Enable System.Debug:** Add variable for verbose logging
3. **Search errors:** Copy exact error message to search
4. **Check documentation:** https://learn.microsoft.com/en-us/azure/devops/pipelines/
5. **Community:** Stack Overflow tag: `azure-pipelines`
6. **Report issues:** https://github.com/microsoft/azure-pipelines-tasks/issues

## Quick Fixes

```yaml
# Condition not working?
# Use: eq(variables['var'], 'value')
# Not: eq($(var), 'value')

# Variable empty?
# Check: Scope (pipeline/stage/job level)
# Check: Output syntax $[ dependencies... ]

# Template not found?
# Check: Path relative to pipeline file
# Try: Absolute path /templates/file.yml

# Agent timeout?
# Add: timeoutInMinutes: 60

# Secret not working?
# Map: env: SECRET: $(SecretVar)

# Deployment output var empty?
# Name: Step name must match job name
# Syntax: dependencies.Job.outputs['Job.Job.var']
```
