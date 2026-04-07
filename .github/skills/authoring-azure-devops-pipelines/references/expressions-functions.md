# Expressions and Functions Reference

Comprehensive guide to Azure Pipelines expressions, functions, operators, and conditional logic.

## Table of Contents

- [Expression Syntax](#expression-syntax)
- [Conditional Operators](#conditional-operators)
- [Logical Operators](#logical-operators)
- [Comparison Functions](#comparison-functions)
- [Type Functions](#type-functions)
- [String Functions](#string-functions)
- [Array Functions](#array-functions)
- [Job Status Functions](#job-status-functions)
- [Special Functions](#special-functions)
- [Complex Expressions](#complex-expressions)

## Expression Syntax

Expressions use runtime evaluation syntax: `$[...]`

**Common contexts:**
- **Conditions:** When stages/jobs/steps should run
- **Variable definitions:** Dynamic variable values
- **Dependency values:** Accessing outputs from other jobs/stages

**Basic structure:**
```yaml
# In a condition
condition: eq(variables['myVar'], 'value')

# In a variable
variables:
  dynamicVar: $[ upper(variables.baseVar) ]

# In dependencies
myOutput: $[ dependencies.JobA.outputs['step.var'] ]
```

## Conditional Operators

### eq - Equals

Tests if two values are equal.

```yaml
# String comparison
condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')

# Number comparison
condition: eq(variables['retry'], 3)

# Boolean comparison
condition: eq(variables.isProduction, true)
```

**Case-sensitive for strings.**

### ne - Not Equal

Tests if two values are not equal.

```yaml
condition: ne(variables['Build.Reason'], 'PullRequest')

condition: ne(variables.environment, 'production')
```

### lt, le, gt, ge - Comparison

Numeric comparisons:
- `lt` - Less than
- `le` - Less than or equal
- `gt` - Greater than
- `ge` - Greater than or equal

```yaml
# Less than
condition: lt(variables.retry, 5)

# Greater than or equal
condition: ge(variables.buildNumber, 100)

# Chaining with and()
condition: and(gt(variables.count, 0), le(variables.count, 10))
```

## Logical Operators

### and - Logical AND

All conditions must be true.

```yaml
# Two conditions
condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))

# Multiple conditions
condition: |
  and(
    succeeded(),
    eq(variables['Build.SourceBranch'], 'refs/heads/main'),
    eq(variables['Build.Reason'], 'Manual')
  )
```

### or - Logical OR

At least one condition must be true.

```yaml
# Deploy on main or release branches
condition: |
  or(
    eq(variables['Build.SourceBranch'], 'refs/heads/main'),
    startsWith(variables['Build.SourceBranch'], 'refs/heads/release/')
  )

# Run on success or partial success
condition: or(succeeded(), succeededOrFailed())
```

### not - Logical NOT

Inverts a condition.

```yaml
# Not a pull request
condition: not(eq(variables['Build.Reason'], 'PullRequest'))

# Not on main branch
condition: not(eq(variables['Build.SourceBranch'], 'refs/heads/main'))

# Combined with and
condition: and(succeeded(), not(canceled()))
```

## Comparison Functions

### in - Value in List

Checks if value is in a list.

```yaml
# Check if branch is in list
condition: in(variables['Build.SourceBranchName'], 'main', 'develop', 'staging')

# Check dependency result
condition: in(dependencies.PreviousJob.result, 'Succeeded', 'SucceededWithIssues')

# Check build reason
condition: in(variables['Build.Reason'], 'IndividualCI', 'BatchedCI')
```

### notIn - Value not in List

Checks if value is not in a list.

```yaml
# Exclude branches
condition: notIn(variables['Build.SourceBranchName'], 'experimental', 'temp')

# Exclude build reasons
condition: notIn(variables['Build.Reason'], 'PullRequest', 'Schedule')
```

## Type Functions

### convertToJson

Converts a value to JSON string.

```yaml
variables:
  myObject: |
    {
      "name": "test",
      "value": 123
    }
  jsonString: $[ convertToJson(variables.myObject) ]

steps:
- script: echo '$(jsonString)'
```

### length

Returns the length of a string or array.

```yaml
parameters:
- name: environments
  type: object
  default:
  - dev
  - staging
  - prod

steps:
- script: echo "Deploying to ${{ length(parameters.environments) }} environments"
```

## String Functions

### contains - Substring Check

Checks if a string contains a substring.

```yaml
# Check if branch contains hotfix
condition: contains(variables['Build.SourceBranch'], 'hotfix')

# Check if commit message contains skip-ci
condition: contains(variables['Build.SourceVersionMessage'], '[skip-ci]')
```

### startsWith - Prefix Check

Checks if string starts with a prefix.

```yaml
# Release branches
condition: startsWith(variables['Build.SourceBranch'], 'refs/heads/release/')

# Feature branches
condition: startsWith(variables['Build.SourceBranchName'], 'feature/')

# Version tags
condition: startsWith(variables['Build.SourceBranch'], 'refs/tags/v')
```

### endsWith - Suffix Check

Checks if string ends with a suffix.

```yaml
# Production branches
condition: endsWith(variables['Build.SourceBranchName'], '-prod')

# Release candidate tags
condition: endsWith(variables['Build.SourceBranch'], '-rc')
```

### format - String Formatting

Formats a string with placeholders.

```yaml
variables:
  buildName: $[ format('{0}-{1}', variables['Build.DefinitionName'], variables['Build.BuildId']) ]

steps:
- script: echo $(buildName)

# With date
variables:
  deploymentTag: $[ format('deploy-{0}-{1}', variables['Build.SourceBranchName'], variables['Build.BuildNumber']) ]
```

### replace - String Replace

Replaces occurrences of a substring.

```yaml
variables:
  # Replace slashes in branch name
  sanitizedBranch: $[ replace(variables['Build.SourceBranchName'], '/', '-') ]

steps:
- script: echo "Branch: $(sanitizedBranch)"
```

### lower - Lowercase

Converts string to lowercase.

```yaml
variables:
  branchLower: $[ lower(variables['Build.SourceBranchName']) ]

condition: eq(lower(variables.environment), 'production')
```

### upper - Uppercase

Converts string to uppercase.

```yaml
variables:
  envUpper: $[ upper(variables.environment) ]

steps:
- script: echo "Environment: $(envUpper)"
```

### split - String Split

Splits a string into an array.

```yaml
# Split comma-separated values
variables:
  environments: 'dev,staging,prod'
  envArray: $[ split(variables.environments, ',') ]
```

### join - Array Join

Joins array elements into a string.

```yaml
parameters:
- name: targets
  type: object
  default:
  - web
  - api
  - worker

variables:
  targetString: $[ join(';', parameters.targets) ]

steps:
- script: echo "Targets: $(targetString)"
```

## Array Functions

### length

Returns array length (also works on strings).

```yaml
parameters:
- name: environments
  type: object
  default:
  - dev
  - staging

steps:
- ${{ if gt(length(parameters.environments), 0) }}:
  - script: echo "Has environments"
```

### contains

Checks if array contains a value.

```yaml
parameters:
- name: platforms
  type: object
  default:
  - linux
  - windows

steps:
- ${{ if contains(parameters.platforms, 'linux') }}:
  - script: echo "Linux included"
```

## Job Status Functions

These functions check the status of the current job or its dependencies.

### succeeded

Returns true if previous job/stage succeeded.

```yaml
# Default condition (implicit)
- job: DeployJob
  condition: succeeded()  # Runs only if dependencies succeeded

# Explicit in step
- script: echo "Build succeeded"
  condition: succeeded()
```

### failed

Returns true if previous job/stage failed.

```yaml
# Cleanup on failure
- job: CleanupJob
  condition: failed()
  steps:
  - script: echo "Cleaning up after failure"

# Step-level
- script: echo "Previous step failed"
  condition: failed()
```

### succeededOrFailed

Returns true if not canceled (succeeded or failed, but not skipped/canceled).

```yaml
# Always run unless canceled
- job: NotifyJob
  condition: succeededOrFailed()
  steps:
  - script: echo "Sending notification"
```

### always

Always returns true (runs regardless of previous status).

```yaml
# Cleanup that always runs
- job: AlwaysCleanup
  condition: always()
  steps:
  - script: echo "Cleaning up resources"

# Publish logs even on failure
- task: PublishBuildArtifacts@1
  condition: always()
  inputs:
    artifactName: 'logs'
```

### canceled

Returns true if pipeline was canceled.

```yaml
- script: echo "Pipeline was canceled"
  condition: canceled()
```

## Special Functions

### dependencies

Access results and outputs from dependent jobs.

```yaml
jobs:
- job: JobA
  steps:
  - script: echo "Job A"

- job: JobB
  dependsOn: JobA
  condition: succeeded('JobA')  # Check if JobA succeeded
  steps:
  - script: echo "Job B"

# Check result
- job: JobC
  dependsOn: JobA
  condition: in(dependencies.JobA.result, 'Succeeded', 'SucceededWithIssues')
  steps:
  - script: echo "Job C"
```

**Access output variables:**
```yaml
jobs:
- job: JobA
  steps:
  - script: echo "##vso[task.setvariable variable=output;isOutput=true]value"
    name: step1

- job: JobB
  dependsOn: JobA
  variables:
    fromJobA: $[ dependencies.JobA.outputs['step1.output'] ]
  steps:
  - script: echo $(fromJobA)
```

### stageDependencies

Access results and outputs from stages.

```yaml
stages:
- stage: Build
  jobs:
  - job: BuildJob
    steps:
    - script: echo "##vso[task.setvariable variable=version;isOutput=true]1.0.0"
      name: setVersion

- stage: Deploy
  dependsOn: Build
  condition: succeeded('Build')  # Check if Build stage succeeded
  variables:
    buildVersion: $[ stageDependencies.Build.BuildJob.outputs['setVersion.version'] ]
  jobs:
  - job: DeployJob
    steps:
    - script: echo "Deploying $(buildVersion)"
```

### variables

Access variables in expressions.

```yaml
# Indexed notation (case-sensitive)
condition: eq(variables['myVar'], 'value')

# Dot notation
condition: eq(variables.myVar, 'value')

# Predefined variables
condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
```

### parameters

Access template parameters (compile-time only).

```yaml
parameters:
- name: environment
  type: string
  default: 'dev'

- name: deployEnabled
  type: boolean
  default: true

steps:
- script: echo "Deploying to ${{ parameters.environment }}"

- ${{ if eq(parameters.deployEnabled, true) }}:
  - script: echo "Deployment enabled"
```

### coalesce

Returns first non-null/non-empty value.

```yaml
variables:
  # Use parameter value if provided, otherwise default
  deployEnv: $[ coalesce(variables.ProvidedEnvironment, 'dev') ]

steps:
- script: echo "Environment: $(deployEnv)"
```

## Complex Expressions

### Multiline Expressions

Use `|` for readability:

```yaml
condition: |
  and(
    succeeded(),
    eq(variables['Build.SourceBranch'], 'refs/heads/main'),
    eq(variables['Build.Reason'], 'Manual'),
    not(contains(variables['Build.SourceVersionMessage'], '[skip-deploy]'))
  )
```

### Nested Functions

Combine multiple functions:

```yaml
# Lowercase and check
condition: eq(lower(variables['environment']), 'production')

# Check if sanitized branch name is main
condition: eq(replace(lower(variables['Build.SourceBranchName']), '/', '-'), 'main')

# Format and compare
variables:
  tag: $[ format('v{0}', variables['Build.BuildNumber']) ]
condition: startsWith(variables['Build.SourceBranch'], format('refs/tags/{0}', variables.tag))
```

### Branch Patterns

Common branch-checking patterns:

```yaml
# Main branch only
condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')

# Release branches
condition: startsWith(variables['Build.SourceBranch'], 'refs/heads/release/')

# Not feature branches
condition: not(startsWith(variables['Build.SourceBranch'], 'refs/heads/feature/'))

# Main or develop
condition: |
  or(
    eq(variables['Build.SourceBranch'], 'refs/heads/main'),
    eq(variables['Build.SourceBranch'], 'refs/heads/develop')
  )

# Any protected branch
condition: |
  or(
    eq(variables['Build.SourceBranch'], 'refs/heads/main'),
    startsWith(variables['Build.SourceBranch'], 'refs/heads/release/'),
    startsWith(variables['Build.SourceBranch'], 'refs/heads/hotfix/')
  )
```

### Deployment Conditions

Production deployment patterns:

```yaml
# Production: main branch, manual trigger
condition: |
  and(
    succeeded(),
    eq(variables['Build.SourceBranch'], 'refs/heads/main'),
    eq(variables['Build.Reason'], 'Manual')
  )

# Staging: on push or PR to develop
condition: |
  and(
    succeeded(),
    eq(variables['Build.SourceBranch'], 'refs/heads/develop'),
    in(variables['Build.Reason'], 'IndividualCI', 'BatchedCI')
  )

# Dev: always on success
condition: succeeded()
```

### Dependency Status Checks

```yaml
# Run if any dependency succeeded
condition: |
  or(
    eq(dependencies.JobA.result, 'Succeeded'),
    eq(dependencies.JobB.result, 'Succeeded')
  )

# Run if all dependencies completed (success or failure)
condition: |
  and(
    in(dependencies.JobA.result, 'Succeeded', 'Failed'),
    in(dependencies.JobB.result, 'Succeeded', 'Failed')
  )

# Run if at least one dependency failed
condition: |
  or(
    eq(dependencies.JobA.result, 'Failed'),
    eq(dependencies.JobB.result, 'Failed')
  )
```

### Variable Default Values

```yaml
# Use environment variable or default to 'dev'
variables:
  deployTarget: $[ coalesce(variables['DEPLOY_ENV'], 'dev') ]

# Use conditional logic
variables:
  buildConfig: $[ if(eq(variables['Build.SourceBranch'], 'refs/heads/main'), 'Release', 'Debug') ]
```

## Expression Evaluation Order

**Compile-time (Template expressions `${{ }}`)**
1. Parameters resolved
2. Template conditions evaluated
3. Template includes/extends processed

**Runtime (Job start)**
4. Variables defined
5. Dependencies checked
6. Runtime expressions `$[ ]` evaluated
7. Job conditions evaluated

**Step execution**
8. Macro variables `$(var)` expanded per step
9. Step conditions evaluated before each step

## Best Practices

### Use Appropriate Syntax

```yaml
# ✅ Template parameters
- script: echo "${{ parameters.environment }}"

# ✅ Conditions
condition: eq(variables['myVar'], 'value')

# ✅ Task inputs
- task: MyTask@1
  inputs:
    parameter: $(myVar)

# ❌ Don't use macro in conditions
condition: eq($(myVar), 'value')  # WRONG

# ❌ Don't use template for runtime values
- script: echo "${{ variables['Build.BuildId'] }}"  # WRONG
```

### Keep Conditions Readable

```yaml
# ✅ Good - multiline with clear logic
condition: |
  and(
    succeeded(),
    eq(variables['Build.SourceBranch'], 'refs/heads/main'),
    not(contains(variables['Build.SourceVersionMessage'], '[skip-deploy]'))
  )

# ❌ Bad - hard to read
condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'), not(contains(variables['Build.SourceVersionMessage'], '[skip-deploy]')))
```

### Test Complex Conditions

Add debug steps to verify condition logic:

```yaml
- script: |
    echo "Branch: $(Build.SourceBranch)"
    echo "Reason: $(Build.Reason)"
    echo "Message: $(Build.SourceVersionMessage)"
  displayName: 'Debug: Show variables'

- script: echo "Deploying"
  condition: |
    and(
      succeeded(),
      eq(variables['Build.SourceBranch'], 'refs/heads/main')
    )
  displayName: 'Deploy (conditional)'
```

## Quick Reference

### Common Functions

```yaml
# Equality
eq(a, b)
ne(a, b)

# Comparison
lt(a, b), le(a, b), gt(a, b), ge(a, b)

# Logical
and(a, b, ...)
or(a, b, ...)
not(a)
in(value, a, b, c)
notIn(value, a, b, c)

# Strings
contains(haystack, needle)
startsWith(string, prefix)
endsWith(string, suffix)
lower(string)
upper(string)
replace(string, old, new)
format('{0} {1}', a, b)

# Status
succeeded()
failed()
succeededOrFailed()
always()
canceled()

# Dependencies
dependencies.JobName.result
dependencies.JobName.outputs['step.var']
stageDependencies.Stage.Job.outputs['step.var']
```
