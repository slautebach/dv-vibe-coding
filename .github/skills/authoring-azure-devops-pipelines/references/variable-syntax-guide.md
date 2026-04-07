# Variable Syntax Guide

Comprehensive reference for Azure Pipelines variable syntax, scoping, output variables, and cross-job/stage passing.

## Table of Contents

1. [Three Variable Syntaxes](#three-variable-syntaxes)
2. [When to Use Each Syntax](#when-to-use-each-syntax)
3. [Variable Scopes](#variable-scopes)
4. [Setting Variables](#setting-variables)
5. [Output Variables](#output-variables)
6. [Cross-Job Variable Passing](#cross-job-variable-passing)
7. [Cross-Stage Variable Passing](#cross-stage-variable-passing)
8. [Secret Variables](#secret-variables)
9. [Common Patterns](#common-patterns)
10. [Troubleshooting](#troubleshooting)

## Three Variable Syntaxes

Azure Pipelines has three different variable syntaxes that evaluate at different times:

### 1. Macro Syntax: `$(variableName)`

**Evaluation:** Before each step execution, after conditions are evaluated  
**Context:** Task inputs, script parameters  
**String replacement:** Simple text replacement

```yaml
variables:
  myVar: 'hello'

steps:
- script: echo $(myVar)  # Prints: hello
  displayName: 'Using macro syntax'

- task: SomeTask@1
  inputs:
    parameter: $(myVar)  # Value passed to task
```

### 2. Template Expression Syntax: `${{ variables.variableName }}`

**Evaluation:** At pipeline compilation time (before pipeline runs)  
**Context:** Template parameters, conditional insertion, compile-time decisions  
**Processing:** Expanded before pipeline starts executing

```yaml
variables:
  myVar: 'production'

steps:
- ${{ if eq(variables.myVar, 'production') }}:
  - script: echo "Production mode"
  
- script: echo ${{ variables.myVar }}  # Replaced at compile time
  displayName: 'Template syntax'
```

### 3. Runtime Expression Syntax: `$[variables.variableName]`

**Evaluation:** At runtime when the expression is encountered  
**Context:** Conditions, dependency expressions  
**Processing:** Evaluated during pipeline execution

```yaml
variables:
  myVar: 'value'

steps:
- script: echo "Running"
  condition: eq(variables['myVar'], 'value')  # Runtime evaluation
  
- script: echo "Status: $[variables.myVar]"  # Runtime evaluation
```

## When to Use Each Syntax

| Scenario | Syntax | Example |
|----------|--------|---------|
| Task input values | Macro `$(var)` | `inputs: path: $(Build.SourcesDirectory)` |
| Script parameters | Macro `$(var)` | `script: echo $(myVar)` |
| Template parameters | Template `${{ parameters.name }}` | `${{ parameters.buildConfig }}` |
| Conditional template insertion | Template `${{ if }}` | `${{ if eq(variables.env, 'prod') }}:` |
| Runtime conditions | Runtime `$[ ]` | `condition: eq(variables['status'], 'ready')` |
| Dependency variables | Runtime `$[ ]` | `$[ dependencies.JobA.outputs['step.var'] ]` |
| Stage dependency variables | Runtime `$[ ]` | `$[ stageDependencies.StageA.JobA.outputs['step.var'] ]` |

## Variable Scopes

### Pipeline-level Variables

Defined at the root or in variable groups:

```yaml
variables:
  globalVar: 'available everywhere'
  
stages:
- stage: Build
  jobs:
  - job: BuildJob
    steps:
    - script: echo $(globalVar)  # Accessible
```

### Stage-level Variables

Available to all jobs in the stage:

```yaml
stages:
- stage: Build
  variables:
    stageVar: 'build stage value'
  jobs:
  - job: BuildJob
    steps:
    - script: echo $(stageVar)  # Accessible
```

### Job-level Variables

Available only within the job:

```yaml
jobs:
- job: JobA
  variables:
    jobVar: 'job A value'
  steps:
  - script: echo $(jobVar)  # Accessible
  
- job: JobB
  steps:
  - script: echo $(jobVar)  # NOT accessible (empty)
```

### Step-level Variables

Set within a step, available to subsequent steps in same job:

```yaml
steps:
- script: echo "##vso[task.setvariable variable=stepVar]my value"
  displayName: 'Set variable'

- script: echo $(stepVar)  # Accessible: prints "my value"
  displayName: 'Use variable'
```

## Setting Variables

### Static Definition

```yaml
variables:
  myVar: 'static value'
  myNumber: 42
  myBool: true
```

### Variable Groups

```yaml
variables:
- group: 'MyVariableGroup'  # From Azure DevOps Library
- name: localVar
  value: 'local value'
```

### Runtime (in Scripts)

```bash
# Bash
echo "##vso[task.setvariable variable=myVar]new value"

# PowerShell
Write-Host "##vso[task.setvariable variable=myVar]new value"
```

### Computed Variables

```yaml
variables:
  timestamp: $[format('{0:yyyy}{0:MM}{0:dd}', pipeline.startTime)]
  buildNumber: $[format('{0}.{1}', variables['Build.SourceBranchName'], counter(variables['Build.SourceBranchName'], 1))]
```

## Output Variables

Output variables allow passing data between jobs and stages.

### Setting Output Variables

```yaml
steps:
- script: |
    echo "##vso[task.setvariable variable=myOutputVar;isOutput=true]my value"
  name: outputStep  # Step name is required for output variables
  displayName: 'Set output variable'
```

**Critical requirements:**
- Must include `isOutput=true`
- Step must have a `name:` property
- Variable is referenced as `stepName.variableName`

### Using Output Variables in Same Job

```yaml
jobs:
- job: JobA
  steps:
  - script: echo "##vso[task.setvariable variable=myVar;isOutput=true]hello"
    name: setVar
  
  - script: echo $(setVar.myVar)  # Works: prints "hello"
    displayName: 'Use in same job'
```

## Cross-Job Variable Passing

### Syntax

```yaml
$[ dependencies.JobName.outputs['stepName.variableName'] ]
```

### Complete Example

```yaml
jobs:
- job: JobA
  steps:
  - script: echo "##vso[task.setvariable variable=myVar;isOutput=true]value from A"
    name: setOutput
    displayName: 'Set output in Job A'
  
  - script: echo $(setOutput.myVar)
    displayName: 'Use in Job A: $(setOutput.myVar)'

- job: JobB
  dependsOn: JobA  # Required: must depend on the job
  variables:
    varFromA: $[ dependencies.JobA.outputs['setOutput.myVar'] ]
  steps:
  - script: echo "Received: $(varFromA)"
    displayName: 'Use in Job B'

- job: JobC
  dependsOn: 
  - JobA
  - JobB
  variables:
    varFromA: $[ dependencies.JobA.outputs['setOutput.myVar'] ]
    # Note: Can only reference immediate dependencies
  steps:
  - script: echo "Received: $(varFromA)"
```

**Key points:**
- Job must have `dependsOn:` to access outputs
- Use runtime expression syntax `$[ ]`
- Map to job-level variable before using in steps

## Cross-Stage Variable Passing

### Syntax

```yaml
$[ stageDependencies.StageName.JobName.outputs['stepName.variableName'] ]
```

### Complete Example

```yaml
stages:
- stage: StageA
  jobs:
  - job: JobA
    steps:
    - script: echo "##vso[task.setvariable variable=myVar;isOutput=true]value from Stage A"
      name: setOutput
      displayName: 'Set output'
    
    - script: echo "In same job: $(setOutput.myVar)"
      displayName: 'Use in same job'

- stage: StageB
  dependsOn: StageA  # Required: must depend on the stage
  variables:
    varFromStageA: $[ stageDependencies.StageA.JobA.outputs['setOutput.myVar'] ]
  jobs:
  - job: JobB
    steps:
    - script: echo "Received from Stage A: $(varFromStageA)"
      displayName: 'Use in Stage B'

- stage: StageC
  dependsOn: 
  - StageA
  - StageB
  variables:
    # Can reference any dependent stage
    varFromA: $[ stageDependencies.StageA.JobA.outputs['setOutput.myVar'] ]
  jobs:
  - job: JobC
    steps:
    - script: echo "Received: $(varFromA)"
```

**Key points:**
- Stage must have `dependsOn:` to access outputs
- Use `stageDependencies` (not `dependencies`)
- Syntax: `stageDependencies.StageName.JobName.outputs[...]`
- Map to stage-level variable before using in jobs

## Secret Variables

Secret variables have special handling for security:

### Defining Secrets

```yaml
variables:
- group: 'MySecrets'  # From variable group with secret values

steps:
- script: echo $(MySecret)  # Prints: ***
  displayName: 'Secret is masked'
```

### Using Secrets in Tasks

```yaml
steps:
- task: AzureCLI@2
  inputs:
    azureSubscription: 'MyServiceConnection'
    scriptType: 'bash'
    scriptLocation: 'inlineScript'
    inlineScript: |
      echo "Secret: $(MySecret)"  # Available as $(variable)
```

### Exposing Secrets to Scripts

Secrets are NOT automatically available as environment variables. Must explicitly map:

```yaml
steps:
- script: |
    echo "Secret: $MY_SECRET"  # Available as env var
  env:
    MY_SECRET: $(MySecretVariable)  # Explicit mapping required
  displayName: 'Use secret in script'
```

### Secret Output Variables

Secrets can be output variables but remain masked:

```yaml
steps:
- script: |
    SECRET_VALUE="my-secret-value"
    echo "##vso[task.setvariable variable=mySecret;isOutput=true;issecret=true]$SECRET_VALUE"
  name: setSecret

- script: echo $(setSecret.mySecret)  # Prints: ***
  displayName: 'Secret is still masked'
```

## Common Patterns

### Pattern 1: Build Number from Variable

```yaml
variables:
  majorVersion: '1'
  minorVersion: '0'

name: $(majorVersion).$(minorVersion).$(Rev:r)  # Generates: 1.0.1, 1.0.2, etc.

steps:
- script: echo "Build: $(Build.BuildNumber)"
```

### Pattern 2: Environment-Specific Variables

```yaml
variables:
- ${{ if eq(variables['Build.SourceBranchName'], 'main') }}:
  - name: environment
    value: 'production'
  - name: apiUrl
    value: 'https://api.prod.example.com'
- ${{ if ne(variables['Build.SourceBranchName'], 'main') }}:
  - name: environment
    value: 'development'
  - name: apiUrl
    value: 'https://api.dev.example.com'

steps:
- script: echo "Deploying to $(environment) at $(apiUrl)"
```

### Pattern 3: Conditional Variable Setting

```yaml
steps:
- script: |
    if [ "$(Build.SourceBranchName)" == "main" ]; then
      echo "##vso[task.setvariable variable=deployFlag]true"
    else
      echo "##vso[task.setvariable variable=deployFlag]false"
    fi
  displayName: 'Set deploy flag'

- script: echo "Deploy: $(deployFlag)"
  condition: eq(variables.deployFlag, 'true')
```

### Pattern 4: Multi-Job Data Flow

```yaml
jobs:
- job: GetVersion
  steps:
  - script: |
      VERSION=$(cat version.txt)
      echo "##vso[task.setvariable variable=appVersion;isOutput=true]$VERSION"
    name: readVersion

- job: Build
  dependsOn: GetVersion
  variables:
    version: $[ dependencies.GetVersion.outputs['readVersion.appVersion'] ]
  steps:
  - script: echo "Building version $(version)"
  - script: echo "##vso[task.setvariable variable=buildId;isOutput=true]$(Build.BuildId)"
    name: buildOutput

- job: Test
  dependsOn: 
  - GetVersion
  - Build
  variables:
    version: $[ dependencies.GetVersion.outputs['readVersion.appVersion'] ]
    buildId: $[ dependencies.Build.outputs['buildOutput.buildId'] ]
  steps:
  - script: echo "Testing version $(version) build $(buildId)"
```

## Troubleshooting

### Issue: Variable Shows as Empty or Literal `$(var)`

**Causes:**
1. Variable not defined
2. Wrong syntax for context
3. Variable not in scope

**Solutions:**
```yaml
# ✓ Check variable is defined
variables:
  myVar: 'value'

# ✓ Use correct syntax
steps:
- script: echo $(myVar)  # Macro for scripts
  condition: eq(variables['myVar'], 'value')  # Runtime for conditions

# ✓ Check scope
jobs:
- job: JobA
  variables:
    jobVar: 'only in JobA'
  steps:
  - script: echo $(jobVar)  # Works
  
- job: JobB
  steps:
  - script: echo $(jobVar)  # Empty - not in scope
```

### Issue: Output Variable Not Available in Next Job

**Causes:**
1. Missing `isOutput=true`
2. Step doesn't have `name:`
3. Missing `dependsOn:`
4. Wrong syntax for accessing output

**Solutions:**
```yaml
# ✓ Correct complete pattern
jobs:
- job: JobA
  steps:
  - script: echo "##vso[task.setvariable variable=myVar;isOutput=true]value"
    name: setVar  # Required

- job: JobB
  dependsOn: JobA  # Required
  variables:
    # ✓ Correct syntax
    myVar: $[ dependencies.JobA.outputs['setVar.myVar'] ]
  steps:
  - script: echo $(myVar)

# ✗ Common mistakes
- job: JobB
  # Missing dependsOn
  variables:
    myVar: $[ dependencies.JobA.outputs['setVar.myVar'] ]  # Will be empty

- job: JobB
  dependsOn: JobA
  variables:
    # Wrong syntax - using macro instead of runtime
    myVar: $(dependencies.JobA.outputs.setVar.myVar)  # Won't work
```

### Issue: Cross-Stage Variable is Empty

**Causes:**
1. Using `dependencies` instead of `stageDependencies`
2. Missing stage `dependsOn:`
3. Wrong stage or job name

**Solutions:**
```yaml
# ✓ Correct pattern
stages:
- stage: StageA
  jobs:
  - job: JobA  # Note the exact job name
    steps:
    - script: echo "##vso[task.setvariable variable=myVar;isOutput=true]value"
      name: setVar  # Note the exact step name

- stage: StageB
  dependsOn: StageA  # Required
  variables:
    # ✓ Correct: stageDependencies (not dependencies)
    myVar: $[ stageDependencies.StageA.JobA.outputs['setVar.myVar'] ]
  jobs:
  - job: JobB
    steps:
    - script: echo $(myVar)

# ✗ Common mistake
- stage: StageB
  dependsOn: StageA
  variables:
    # Wrong: using dependencies instead of stageDependencies
    myVar: $[ dependencies.StageA.JobA.outputs['setVar.myVar'] ]  # Empty
```

### Issue: Secret Variable Not Available in Script

**Cause:** Secrets aren't automatically mapped to environment variables

**Solution:**
```yaml
# ✗ Wrong - secret not available as env var
steps:
- script: echo $MY_SECRET  # Empty
  displayName: 'Try to use secret'

# ✓ Correct - explicitly map to env var
steps:
- script: echo $MY_SECRET  # Works
  env:
    MY_SECRET: $(MySecretVariable)
  displayName: 'Use secret'
```

### Issue: Template Expression Not Evaluating

**Cause:** Template expressions only work at compile time

**Solution:**
```yaml
# ✗ Won't work - trying to use runtime value in template expression
steps:
- script: echo "##vso[task.setvariable variable=myVar]value"
- ${{ if eq(variables.myVar, 'value') }}:  # Won't work - myVar set at runtime
  - script: echo "Condition met"

# ✓ Works - template expressions only for compile-time values
variables:
  myVar: 'value'

steps:
- ${{ if eq(variables.myVar, 'value') }}:  # Works - compile-time value
  - script: echo "Condition met"

# ✓ Alternative - use runtime condition
steps:
- script: echo "##vso[task.setvariable variable=myVar]value"
- script: echo "Condition met"
  condition: eq(variables['myVar'], 'value')  # Runtime evaluation
```

## Best Practices

1. **Use descriptive variable names** - `deploymentEnvironment` not `env`
2. **Document secret variables** - Add comments explaining what secrets are needed
3. **Minimize cross-job dependencies** - Keep jobs independent when possible
4. **Use variable groups for secrets** - Don't hardcode secrets in YAML
5. **Validate output variables** - Check if empty before using
6. **Use consistent naming** - camelCase or snake_case throughout pipeline
7. **Avoid deep dependency chains** - More than 2-3 levels becomes fragile
