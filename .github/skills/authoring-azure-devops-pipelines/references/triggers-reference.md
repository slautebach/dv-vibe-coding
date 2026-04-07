# Triggers Reference

Comprehensive guide to Azure Pipelines triggers including CI, PR, scheduled, and pipeline resource triggers.

## Table of Contents

- [Trigger Types Overview](#trigger-types-overview)
- [CI Triggers (Push)](#ci-triggers-push)
- [Pull Request Triggers](#pull-request-triggers)
- [Scheduled Triggers](#scheduled-triggers)
- [Pipeline Resource Triggers](#pipeline-resource-triggers)
- [Disabling Triggers](#disabling-triggers)
- [Trigger Best Practices](#trigger-best-practices)

## Trigger Types Overview

| Trigger Type | Keyword | Purpose | Trigger On |
|--------------|---------|---------|------------|
| CI (Continuous Integration) | `trigger:` | Build on code push | Commit to branch |
| Pull Request | `pr:` | Build on PR | PR creation/update |
| Scheduled | `schedules:` | Time-based builds | Cron schedule |
| Pipeline Resource | `resources: pipelines:` | Chain pipelines | Other pipeline completion |

## CI Triggers (Push)

CI triggers run the pipeline when code is pushed to specified branches.

### Basic CI Trigger

```yaml
# Trigger on any push to any branch
trigger:
- '*'

# Trigger on specific branches
trigger:
- main
- develop
- release/*
```

### Branch Filters

```yaml
trigger:
  branches:
    include:
    - main
    - develop
    - release/*
    - feature/*
    exclude:
    - feature/experimental
    - temp/*
```

**Wildcard patterns:**
- `*` - Matches any string within a segment
- `**` - Matches any string across segments

```yaml
trigger:
  branches:
    include:
    - main
    - releases/*      # matches: releases/v1, releases/v2
    - features/*/*    # matches: features/team/feature-name
    - refs/tags/*     # matches: tags
```

### Path Filters

Only trigger when specific paths change:

```yaml
trigger:
  branches:
    include:
    - main
  paths:
    include:
    - src/*
    - tests/*
    exclude:
    - docs/*
    - '*.md'
    - .gitignore
```

**Path filter rules:**
- Paths are relative to repository root
- Use forward slashes (`/`) even on Windows
- `*` matches files in current directory
- `**` matches files in any subdirectory

**Common patterns:**
```yaml
trigger:
  paths:
    include:
    - src/**            # All files under src/
    - '*.csproj'        # All .csproj files in root
    - 'src/**/*.cs'     # All C# files under src/
    exclude:
    - '**/*.md'         # All markdown files
    - 'tests/**'        # All files under tests/
```

### Combined Branch and Path Filters

```yaml
trigger:
  branches:
    include:
    - main
    - develop
    exclude:
    - feature/experimental
  paths:
    include:
    - src/**
    - tests/**
    exclude:
    - docs/**
    - '**/*.md'
```

**Logic:** Trigger if **branch matches AND path matches**

### Batch CI Builds

Prevent multiple builds for rapid commits:

```yaml
trigger:
  batch: true  # Batch builds if one is already running
  branches:
    include:
    - main
```

**How it works:**
- If build is running and new commits arrive, they're batched
- After current build finishes, one new build runs with all batched commits
- Reduces queue congestion for busy branches

### Tag Triggers

Trigger on Git tags:

```yaml
trigger:
  tags:
    include:
    - v*        # v1.0, v2.0, etc.
    - release-*
```

### Full CI Trigger Example

```yaml
trigger:
  batch: true
  branches:
    include:
    - main
    - develop
    - release/*
    exclude:
    - experimental/*
  paths:
    include:
    - src/**
    - build/**
    - azure-pipelines.yml
    exclude:
    - docs/**
    - '**/*.md'
    - '.github/**'
  tags:
    include:
    - v*
    - release-*
```

## Pull Request Triggers

PR triggers run when pull requests are created or updated.

### Basic PR Trigger

```yaml
# Trigger on PRs to any branch
pr:
- '*'

# Trigger on PRs to specific branches
pr:
- main
- develop
```

### PR Branch Filters

```yaml
pr:
  branches:
    include:
    - main
    - develop
    - release/*
    exclude:
    - experimental/*
```

**Condition:** Pipeline triggers when PR targets an included branch (and not an excluded one).

### PR Path Filters

```yaml
pr:
  branches:
    include:
    - main
  paths:
    include:
    - src/**
    - tests/**
    exclude:
    - docs/**
    - '**.md'
```

**Logic:** Trigger if **target branch matches AND changed files match paths**

### PR Auto-Cancel

Cancel previous PR builds when new commit is pushed:

```yaml
pr:
  autoCancel: true  # Cancel outdated PR builds
  branches:
    include:
    - main
```

### Draft PR Handling

```yaml
pr:
  drafts: false  # Don't trigger on draft PRs
  branches:
    include:
    - main
```

### Full PR Trigger Example

```yaml
pr:
  autoCancel: true
  drafts: false
  branches:
    include:
    - main
    - develop
    exclude:
    - feature/experimental
  paths:
    include:
    - src/**
    - tests/**
    - azure-pipelines.yml
    exclude:
    - docs/**
    - '**/*.md'
```

### PR Comments and Updates

```yaml
# Trigger on PR comments containing /azp run
pr:
  branches:
    include:
    - main
  
# Users can comment "/azp run" or "/azp run <pipeline-name>" to manually trigger
```

## Scheduled Triggers

Run pipelines on a schedule using cron syntax.

### Basic Scheduled Trigger

```yaml
schedules:
- cron: "0 0 * * *"  # Midnight UTC every day
  displayName: 'Nightly build'
  branches:
    include:
    - main
```

### Cron Syntax

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12 or JAN-DEC)
│ │ │ │ ┌───────────── day of week (0 - 6 or SUN-SAT)
│ │ │ │ │
│ │ │ │ │
* * * * *
```

**Common patterns:**
```yaml
schedules:
# Every day at midnight UTC
- cron: "0 0 * * *"
  displayName: 'Daily build'
  branches:
    include:
    - main

# Every Monday at 3 AM UTC
- cron: "0 3 * * MON"
  displayName: 'Weekly build'
  branches:
    include:
    - main

# Every 6 hours
- cron: "0 */6 * * *"
  displayName: 'Every 6 hours'
  branches:
    include:
    - develop

# Weekdays at 9 AM and 5 PM UTC
- cron: "0 9,17 * * MON-FRI"
  displayName: 'Business hours build'
  branches:
    include:
    - main

# First day of every month
- cron: "0 0 1 * *"
  displayName: 'Monthly build'
  branches:
    include:
    - main
```

### Always Run Schedule

Run even if no code changes:

```yaml
schedules:
- cron: "0 0 * * *"
  displayName: 'Nightly build'
  branches:
    include:
    - main
  always: true  # Run even if no code changes since last successful scheduled build
```

**Default behavior (`always: false`):**
- Only runs if code changed since last successful scheduled build
- Prevents redundant builds

### Multiple Schedules

```yaml
schedules:
# Nightly build of main
- cron: "0 0 * * *"
  displayName: 'Nightly main build'
  branches:
    include:
    - main
  always: true

# Weekly build of develop
- cron: "0 0 * * SUN"
  displayName: 'Weekly develop build'
  branches:
    include:
    - develop
  always: false

# Hourly build during business hours (weekdays)
- cron: "0 9-17 * * MON-FRI"
  displayName: 'Business hours build'
  branches:
    include:
    - develop
  always: false
```

## Pipeline Resource Triggers

Trigger a pipeline when another pipeline completes.

### Basic Pipeline Trigger

```yaml
resources:
  pipelines:
  - pipeline: buildPipeline  # Resource identifier
    source: MyProject-CI     # Pipeline name
    trigger:
      branches:
        include:
        - main
```

**Triggers when:** `MyProject-CI` pipeline completes successfully on `main` branch.

### Pipeline Trigger with Stages

```yaml
resources:
  pipelines:
  - pipeline: buildPipeline
    source: MyProject-CI
    trigger:
      branches:
        include:
        - main
      stages:
      - Build
      - Test
```

**Triggers when:** `MyProject-CI` completes **Build** and **Test** stages successfully.

### Pipeline Trigger with Tags

```yaml
resources:
  pipelines:
  - pipeline: buildPipeline
    source: MyProject-CI
    trigger:
      branches:
        include:
        - main
      tags:
      - Production
      - Release
```

**Triggers when:** `MyProject-CI` completes with tags `Production` or `Release`.

### Accessing Pipeline Resource Artifacts

```yaml
resources:
  pipelines:
  - pipeline: buildPipeline
    source: MyProject-CI
    trigger:
      branches:
        include:
        - main

jobs:
- job: Deploy
  steps:
  - download: buildPipeline  # Download artifacts from triggered pipeline
    artifact: drop
  
  - script: |
      echo "Deploying artifacts from buildPipeline"
      ls $(Pipeline.Workspace)/buildPipeline/drop
```

### Disable Pipeline Trigger

```yaml
resources:
  pipelines:
  - pipeline: buildPipeline
    source: MyProject-CI
    trigger: none  # Don't trigger on pipeline completion
```

### Multiple Pipeline Resources

```yaml
resources:
  pipelines:
  - pipeline: backendBuild
    source: Backend-CI
    trigger:
      branches:
        include:
        - main
  
  - pipeline: frontendBuild
    source: Frontend-CI
    trigger:
      branches:
        include:
        - main

jobs:
- job: IntegrationTest
  steps:
  - download: backendBuild
    artifact: api
  - download: frontendBuild
    artifact: webapp
  - script: echo "Running integration tests"
```

### Full Pipeline Resource Example

```yaml
resources:
  pipelines:
  - pipeline: buildPipeline
    source: MyProject-Build
    project: MyProject  # If in different project
    trigger:
      branches:
        include:
        - main
        - release/*
        exclude:
        - experimental/*
      stages:
      - Build
      - Test
      tags:
      - Production

stages:
- stage: Deploy
  jobs:
  - deployment: DeployApp
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - download: buildPipeline
            artifact: drop
          - script: echo "Deploying $(resources.pipeline.buildPipeline.runName)"
```

## Disabling Triggers

### Disable All Triggers

```yaml
trigger: none
pr: none
schedules: []
```

**Use for:**
- Pipelines that should only run manually
- Template pipelines not meant to run directly
- Testing/experimental pipelines

### Disable Specific Triggers

```yaml
# CI only (no PR or schedules)
trigger:
  branches:
    include:
    - main
pr: none
schedules: []

# PR only (no CI or schedules)
trigger: none
pr:
  branches:
    include:
    - main
schedules: []

# Manual and scheduled only (no CI or PR)
trigger: none
pr: none
schedules:
- cron: "0 0 * * *"
  branches:
    include:
    - main
```

## Trigger Best Practices

### 1. Use Path Filters to Reduce Noise

```yaml
# ✅ Good - Only build when code changes
trigger:
  branches:
    include:
    - main
  paths:
    include:
    - src/**
    - tests/**
    exclude:
    - docs/**
    - '**/*.md'

# ❌ Bad - Builds on every change including docs
trigger:
- main
```

### 2. Batch CI for Busy Branches

```yaml
# ✅ Good - Batch rapid commits
trigger:
  batch: true
  branches:
    include:
    - develop  # Busy integration branch
```

### 3. Auto-Cancel Outdated PR Builds

```yaml
# ✅ Good - Save resources
pr:
  autoCancel: true
  branches:
    include:
    - main
```

### 4. Use Specific Branch Patterns

```yaml
# ✅ Good - Explicit patterns
trigger:
  branches:
    include:
    - main
    - release/*
    - hotfix/*

# ❌ Bad - Too permissive
trigger:
- '*'
```

### 5. Schedule Resource-Intensive Builds

```yaml
# ✅ Good - Run heavy tests off-hours
schedules:
- cron: "0 2 * * *"  # 2 AM UTC
  displayName: 'Nightly integration tests'
  branches:
    include:
    - main
  always: true
```

### 6. Pin Pipeline Resource Versions

```yaml
# ✅ Good - Stable dependencies
resources:
  pipelines:
  - pipeline: buildPipeline
    source: MyProject-CI
    trigger:
      tags:
      - v*  # Only trigger on versioned releases
```

### 7. Document Trigger Decisions

```yaml
# CI Trigger: Build on main and release branches
# Excludes: Documentation changes (.md files)
# Path filters: Only src/ and tests/ directories
trigger:
  batch: true
  branches:
    include:
    - main
    - release/*
  paths:
    include:
    - src/**
    - tests/**
    exclude:
    - '**/*.md'
```

## Conditional Pipeline Logic Based on Trigger

Check what triggered the pipeline:

### Build.Reason Variable

```yaml
steps:
- script: echo "Build reason: $(Build.Reason)"

# Conditional steps based on trigger
- script: echo "Triggered by CI"
  condition: in(variables['Build.Reason'], 'IndividualCI', 'BatchedCI')

- script: echo "Triggered by PR"
  condition: eq(variables['Build.Reason'], 'PullRequest')

- script: echo "Triggered by schedule"
  condition: eq(variables['Build.Reason'], 'Schedule')

- script: echo "Triggered manually"
  condition: eq(variables['Build.Reason'], 'Manual')

- script: echo "Triggered by another pipeline"
  condition: eq(variables['Build.Reason'], 'ResourceTrigger')
```

### Build.Reason Values

| Value | Meaning |
|-------|---------|
| `Manual` | Pipeline started manually |
| `IndividualCI` | CI trigger (single commit) |
| `BatchedCI` | CI trigger (batched commits) |
| `PullRequest` | PR trigger |
| `Schedule` | Scheduled trigger |
| `ResourceTrigger` | Pipeline resource trigger |
| `BuildCompletion` | Build completion trigger |

### Conditional Deployment

```yaml
stages:
- stage: Build
  jobs:
  - job: BuildJob
    steps:
    - script: echo "Building"

- stage: Deploy
  # Only deploy if triggered by CI on main (not PRdeploy or manual)
  condition: |
    and(
      succeeded(),
      eq(variables['Build.SourceBranch'], 'refs/heads/main'),
      in(variables['Build.Reason'], 'IndividualCI', 'BatchedCI')
    )
  jobs:
  - deployment: DeployJob
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - script: echo "Deploying to production"
```

## Quick Reference

### Trigger Syntax

```yaml
# CI (push) trigger
trigger:
  batch: true
  branches:
    include: [ main, develop ]
    exclude: [ experimental/* ]
  paths:
    include: [ src/** ]
    exclude: [ docs/**, '**/*.md' ]
  tags:
    include: [ v*, release-* ]

# PR trigger
pr:
  autoCancel: true
  drafts: false
  branches:
    include: [ main ]
  paths:
    exclude: [ docs/** ]

# Scheduled trigger
schedules:
- cron: "0 0 * * *"
  displayName: 'Nightly'
  branches:
    include: [ main ]
  always: true

# Pipeline resource trigger
resources:
  pipelines:
  - pipeline: buildPipeline
    source: Build-Pipeline-Name
    trigger:
      branches:
        include: [ main ]
      stages: [ Build, Test ]
      tags: [ Production ]

# Disable triggers
trigger: none
pr: none
```

### Cron Quick Reference

```yaml
# Every day at midnight
"0 0 * * *"

# Every hour
"0 * * * *"

# Every 6 hours
"0 */6 * * *"

# Weekdays at 9 AM
"0 9 * * MON-FRI"

# First day of month
"0 0 1 * *"

# Every Monday
"0 0 * * MON"
```

### Build.Reason Checks

```yaml
# Check if CI trigger
condition: in(variables['Build.Reason'], 'IndividualCI', 'BatchedCI')

# Check if PR
condition: eq(variables['Build.Reason'], 'PullRequest')

# Check if scheduled
condition: eq(variables['Build.Reason'], 'Schedule')

# Check if manual
condition: eq(variables['Build.Reason'], 'Manual')
```
