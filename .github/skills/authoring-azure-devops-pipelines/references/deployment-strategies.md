# Deployment Strategies

Comprehensive guide to Azure Pipelines deployment jobs, strategies, lifecycle hooks, and environment management.

## Table of Contents

- [Deployment Jobs Overview](#deployment-jobs-overview)
- [Deployment Strategies](#deployment-strategies)
- [Lifecycle Hooks](#lifecycle-hooks)
- [Environments](#environments)
- [Output Variables in Deployments](#output-variables-in-deployments)
- [Deployment Patterns](#deployment-patterns)

## Deployment Jobs Overview

Deployment jobs are specialized jobs that deploy to environments and track deployment history.

### Basic Deployment Job Structure

```yaml
jobs:
- deployment: DeployWeb
  displayName: 'Deploy to Web App'
  environment: 'production'
  pool:
    vmImage: 'ubuntu-latest'
  strategy:
    runOnce:
      deploy:
        steps:
        - script: echo "Deploying application"
```

**Key differences from regular jobs:**
- Uses `deployment:` instead of `job:`
- Requires `environment:` specification
- Must have a `strategy:` block
- Steps go inside strategy lifecycle hooks
- Tracks deployment history in Azure DevOps

### Environment Specification

```yaml
# Simple environment name
environment: 'production'

# Environment with resource
environment:
  name: 'production'
  resourceType: VirtualMachine
  tags: 'web,frontend'

# Environment with resource name
environment: 'production.web-server-01'
```

## Deployment Strategies

Azure Pipelines supports three deployment strategies:

### 1. RunOnce Strategy

Deploy once to all targets. Most common strategy.

```yaml
jobs:
- deployment: DeployApp
  environment: 'production'
  strategy:
    runOnce:
      preDeploy:
        steps:
        - script: echo "Pre-deployment validation"
      
      deploy:
        steps:
        - script: echo "Deploying application"
        - task: AzureWebApp@1
          inputs:
            azureSubscription: 'MySubscription'
            appName: 'myapp'
      
      routeTraffic:
        steps:
        - script: echo "Routing traffic to new version"
      
      postRouteTraffic:
        steps:
        - script: echo "Running smoke tests"
        - script: sleep 60  # Monitor for 60 seconds
      
      on:
        failure:
          steps:
          - script: echo "Deployment failed, rolling back"
        success:
          steps:
          - script: echo "Deployment successful"
```

**Lifecycle hook execution order:**
1. preDeploy
2. deploy
3. routeTraffic
4. postRouteTraffic
5. on: success (if all succeeded) OR on: failure (if any failed)

### 2. Rolling Strategy

Deploy incrementally to subsets of targets.

```yaml
jobs:
- deployment: DeployApp
  environment:
    name: 'production'
    resourceType: VirtualMachine
    tags: 'web'
  strategy:
    rolling:
      maxParallel: 2  # Deploy to 2 VMs at a time
      preDeploy:
        steps:
        - script: echo "Pre-deploy on $(Agent.MachineName)"
      
      deploy:
        steps:
        - script: echo "Deploying to $(Agent.MachineName)"
        - task: IISWebAppDeploymentOnMachineGroup@0
          inputs:
            WebSiteName: 'Default Web Site'
            Package: '$(Pipeline.Workspace)/drop/app.zip'
      
      routeTraffic:
        steps:
        - script: echo "Enabling server $(Agent.MachineName)"
      
      postRouteTraffic:
        steps:
        - script: echo "Running health check on $(Agent.MachineName)"
      
      on:
        failure:
          steps:
          - script: echo "Deployment failed on $(Agent.MachineName)"
        success:
          steps:
          - script: echo "Deployment succeeded on $(Agent.MachineName)"
```

**How it works:**
- Deploys to `maxParallel` targets at a time
- Each target goes through all lifecycle hooks
- Proceeds to next batch only if current batch succeeds
- If any target fails, deployment stops

### 3. Canary Strategy

Deploy to progressively larger groups.

```yaml
jobs:
- deployment: DeployApp
  environment:
    name: 'production'
    resourceType: Kubernetes
    tags: 'web'
  strategy:
    canary:
      increments: [10, 20, 50, 100]  # Deploy to 10%, then 20%, then 50%, then 100%
      preDeploy:
        steps:
        - script: echo "Preparing canary deployment"
      
      deploy:
        steps:
        - script: echo "Deploying $(strategy.increment)% of traffic"
        - task: KubernetesManifest@0
          inputs:
            action: 'deploy'
            manifests: '$(Pipeline.Workspace)/manifests/deployment.yml'
            containers: 'myapp:$(Build.BuildId)'
            trafficSplitMethod: 'baseline-canary'
            percentage: $(strategy.increment)
      
      routeTraffic:
        steps:
        - script: echo "Routing $(strategy.increment)% of traffic to new version"
      
      postRouteTraffic:
        steps:
        - script: echo "Monitoring $(strategy.increment)% deployment"
        - script: sleep 300  # Monitor for 5 minutes
      
      on:
        failure:
          steps:
          - script: echo "Canary deployment failed, rolling back"
          - task: KubernetesManifest@0
            inputs:
              action: 'reject'
        success:
          steps:
          - script: echo "Canary deployment successful"
```

**How it works:**
- Deploys to progressively larger percentages
- `$(strategy.increment)` variable contains current percentage
- Each increment goes through all lifecycle hooks
- Manual or automated promotion between increments

## Lifecycle Hooks

Lifecycle hooks define when steps execute during deployment.

### Available Hooks

| Hook | Purpose | When It Runs |
|------|---------|--------------|
| `preDeploy` | Setup, validation | Before deployment |
| `deploy` | Actual deployment | Main deployment phase |
| `routeTraffic` | Traffic management | After deployment |
| `postRouteTraffic` | Validation, monitoring | After traffic routing |
| `on: failure` | Rollback, cleanup | If any hook fails |
| `on: success` | Notifications, cleanup | If all hooks succeed |

### Hook Execution Flow

```
preDeploy
    ↓
    Success? ──No───→ on: failure
    ↓
    Yes
    ↓
deploy
    ↓
    Success? ──No───→ on: failure
    ↓
    Yes
    ↓
routeTraffic
    ↓
    Success? ──No───→ on: failure
    ↓
    Yes
    ↓
postRouteTraffic
    ↓
    Success? ──No───→ on: failure
    ↓
    Yes
    ↓
on: success
```

### Complete Hook Example

```yaml
strategy:
  runOnce:
    preDeploy:
      pool:
        vmImage: 'ubuntu-latest'
      steps:
      - script: echo "Validating prerequisites"
      - task: AzureCLI@2
        inputs:
          azureSubscription: 'MySubscription'
          scriptType: 'bash'
          scriptLocation: 'inlineScript'
          inlineScript: |
            # Check if target is healthy
            az webapp show --name myapp --resource-group myRG
    
    deploy:
      steps:
      - download: current
        artifact: drop
      - task: AzureWebApp@1
        inputs:
          azureSubscription: 'MySubscription'
          appName: 'myapp'
          package: '$(Pipeline.Workspace)/drop/*.zip'
    
    routeTraffic:
      steps:
      - script: echo "Traffic will now go to new version"
    
    postRouteTraffic:
      steps:
      - script: |
          echo "Waiting for app to stabilize..."
          sleep 60
      - script: |
          echo "Running smoke tests"
          curl https://myapp.azurewebsites.net/health
    
    on:
      failure:
        steps:
        - script: echo "##vso[task.logissue type=error]Deployment failed!"
        - task: AzureAppServiceManage@0
          inputs:
            azureSubscription: 'MySubscription'
            Action: 'Swap Slots'
            WebAppName: 'myapp'
            SourceSlot: 'production'
            SwapWithProduction: false
            TargetSlot: 'staging'
      
      success:
        steps:
        - script: echo "Deployment successful!"
        - task: InvokeRESTAPI@1
          inputs:
            connectionType: 'connectedServiceName'
            serviceConnection: 'SlackWebhook'
            method: 'POST'
            body: '{"text": "Production deployment completed successfully"}'
```

## Environments

Environments represent deployment targets and track deployment history.

### Creating Environment References

```yaml
# Simple environment
environment: 'production'

# With resource type
environment:
  name: 'production'
  resourceType: VirtualMachine

# With resource name (specific VM)
environment: 'production.vm-web-01'

# With tags (subset of resources)
environment:
  name: 'production'
  resourceType: Kubernetes
  tags: 'frontend,web'
```

### Environment Features in Azure DevOps

1. **Manual Approvals** - Require approval before deployment
2. **Checks** - Automated gates (Azure Policy, REST API, etc.)
3. **Deployment History** - Track all deployments
4. **Resource Tagging** - Target specific resources

### Environment Approval Example

```yaml
stages:
- stage: DeployStaging
  jobs:
  - deployment: DeployStaging
    environment: 'staging'  # Auto-deploys (if configured)
    strategy:
      runOnce:
        deploy:
          steps:
          - script: echo "Deploying to staging"

- stage: DeployProduction
  dependsOn: DeployStaging
  jobs:
  - deployment: DeployProduction
    environment: 'production'  # Requires manual approval (if configured)
    strategy:
      runOnce:
        deploy:
          steps:
          - script: echo "Deploying to production"
```

**Configure approvals in Azure DevOps:**
- Pipelines → Environments → Select environment → Approvals and checks

## Output Variables in Deployments

Output variables in deployment jobs require special syntax.

### Setting Output Variables

```yaml
jobs:
- deployment: DeployApp
  environment: 'production'
  strategy:
    runOnce:
      deploy:
        steps:
        - script: |
            deploymentTime=$(date)
            echo "##vso[task.setvariable variable=deployTime;isOutput=true]$deploymentTime"
          name: DeployApp  # MUST match deployment job name
          displayName: 'Set deployment time'
```

**Critical:** Step `name:` must match the deployment job name for output variables.

### Consuming Output Variables

**From another job in same stage:**

```yaml
jobs:
- deployment: DeployApp
  environment: 'production'
  strategy:
    runOnce:
      deploy:
        steps:
        - script: |
            echo "##vso[task.setvariable variable=buildId;isOutput=true]$(Build.BuildId)"
          name: DeployApp  # Matches deployment job name

- job: PostDeploymentTests
  dependsOn: DeployApp
  variables:
    deployedBuildId: $[ dependencies.DeployApp.outputs['DeployApp.DeployApp.buildId'] ]
    #                  ─────────────────────────┬────────  ┬────────  ┬────────
    #                                           │           │          └─ Variable name
    #                                           │           └──────────── Step name (matches job name)
    #                                           └──────────────────────── Deployment job name
  steps:
  - script: echo "Deployed build: $(deployedBuildId)"
```

**From another stage:**

```yaml
stages:
- stage: Deploy
  jobs:
  - deployment: DeployApp
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - script: |
              echo "##vso[task.setvariable variable=version;isOutput=true]1.0.0"
            name: DeployApp

- stage: Validate
  dependsOn: Deploy
  variables:
    deployedVersion: $[ stageDependencies.Deploy.DeployApp.outputs['DeployApp.DeployApp.version'] ]
    #                  ─────────────────┬──────  ─────┬────  ─────┬────  ─────┬─────
    #                                   │             │            │           └─ Variable name
    #                                   │             │            └───────────── Step name
    #                                   │             └────────────────────────── Deployment job name
    #                                   └──────────────────────────────────────── Stage name
  jobs:
  - job: ValidateDeployment
    steps:
    - script: echo "Validating version: $(deployedVersion)"
```

**Pattern summary:**
```yaml
# Same stage, different job
$[ dependencies.DeploymentJobName.outputs['DeploymentJobName.stepName.variableName'] ]

# Different stage
$[ stageDependencies.StageName.DeploymentJobName.outputs['DeploymentJobName.stepName.variableName'] ]
```

## Deployment Patterns

### Blue-Green Deployment

Use Azure App Service deployment slots:

```yaml
jobs:
- deployment: DeployToGreen
  displayName: 'Deploy to Green Slot'
  environment: 'production'
  strategy:
    runOnce:
      deploy:
        steps:
        - task: AzureWebApp@1
          inputs:
            azureSubscription: 'MySubscription'
            appName: 'myapp'
            deployToSlotOrASE: true
            resourceGroupName: 'myResourceGroup'
            slotName: 'staging'  # Green slot
            package: '$(Pipeline.Workspace)/drop/*.zip'
      
      postRouteTraffic:
        steps:
        - script: |
            echo "Running smoke tests on staging slot"
            curl https://myapp-staging.azurewebsites.net/health
        
        - task: AzureAppServiceManage@0
          displayName: 'Swap slots (Blue/Green)'
          inputs:
            azureSubscription: 'MySubscription'
            action: 'Swap Slots'
            webAppName: 'myapp'
            resourceGroupName: 'myResourceGroup'
            sourceSlot: 'staging'
            swapWithProduction: true
      
      on:
        failure:
          steps:
          - task: AzureAppServiceManage@0
            displayName: 'Rollback - Swap back'
            inputs:
              azureSubscription: 'MySubscription'
              action: 'Swap Slots'
              webAppName: 'myapp'
              resourceGroupName: 'myResourceGroup'
              sourceSlot: 'staging'
              swapWithProduction: true
```

### Multi-Region Deployment

Deploy to multiple regions sequentially:

```yaml
parameters:
- name: regions
  type: object
  default:
  - name: 'eastus'
    environment: 'prod-eastus'
  - name: 'westus'
    environment: 'prod-westus'
  - name: 'northeurope'
    environment: 'prod-europe'

stages:
- stage: Build
  jobs:
  - job: BuildApp
    steps:
    - script: echo "Building application"

- ${{ each region in parameters.regions }}:
  - stage: Deploy_${{ replace(region.name, '-', '_') }}
    displayName: 'Deploy to ${{ region.name }}'
    dependsOn: Build
    jobs:
    - deployment: Deploy_${{ region.name }}
      environment: ${{ region.environment }}
      strategy:
        runOnce:
          deploy:
            steps:
            - script: echo "Deploying to ${{ region.name }}"
            - task: AzureWebApp@1
              inputs:
                azureSubscription: 'MySubscription'
                appName: 'myapp-${{ region.name }}'
                package: '$(Pipeline.Workspace)/drop/*.zip'
```

### Database Deployment with Validation

```yaml
jobs:
- deployment: DeployDatabase
  displayName: 'Deploy Database Changes'
  environment: 'production-database'
  strategy:
    runOnce:
      preDeploy:
        steps:
        - script: echo "Backing up database"
        - task: AzureCLI@2
          inputs:
            azureSubscription: 'MySubscription'
            scriptType: 'bash'
            scriptLocation: 'inlineScript'
            inlineScript: |
              # Create backup
              az sql db copy \
                --name mydb \
                --resource-group myRG \
                --server myserver \
                --dest-name "mydb-backup-$(Build.BuildId)"
      
      deploy:
        steps:
        - task: SqlAzureDacpacDeployment@1
          inputs:
            azureSubscription: 'MySubscription'
            serverName: 'myserver.database.windows.net'
            databaseName: 'mydb'
            sqlUsername: $(dbUsername)
            sqlPassword: $(dbPassword)
            deployType: 'DacpacTask'
            dacpacFile: '$(Pipeline.Workspace)/drop/database.dacpac'
      
      postRouteTraffic:
        steps:
        - script: echo "Running database validation"
        - task: AzureCLI@2
          inputs:
            azureSubscription: 'MySubscription'
            scriptType: 'bash'
            scriptLocation: 'inlineScript'
            inlineScript: |
              # Run validation queries
              sqlcmd -S myserver.database.windows.net -d mydb \
                -U $(dbUsername) -P $(dbPassword) \
                -i validation.sql
      
      on:
        failure:
          steps:
          - script: echo "##vso[task.logissue type=error]Database deployment failed!"
          - task: AzureCLI@2
            displayName: 'Restore from backup'
            inputs:
              azureSubscription: 'MySubscription'
              scriptType: 'bash'
              scriptLocation: 'inlineScript'
              inlineScript: |
                # Restore from backup
                az sql db restore \
                  --name mydb \
                  --resource-group myRG \
                  --server myserver \
                  --time "$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
```

### Kubernetes Canary Deployment

```yaml
jobs:
- deployment: CanaryDeploy
  displayName: 'Canary Deploy to AKS'
  environment:
    name: 'production'
    resourceType: Kubernetes
  strategy:
    canary:
      increments: [25, 50, 100]
      preDeploy:
        steps:
        - script: echo "Preparing canary deployment to $(strategy.increment)%"
      
      deploy:
        steps:
        - task: KubernetesManifest@0
          displayName: 'Deploy canary $(strategy.increment)%'
          inputs:
            action: 'deploy'
            kubernetesServiceConnection: 'MyK8sConnection'
            namespace: 'production'
            strategy: 'canary'
            percentage: $(strategy.increment)
            manifests: |
              $(Pipeline.Workspace)/manifests/deployment.yml
              $(Pipeline.Workspace)/manifests/service.yml
            containers: 'myregistry.azurecr.io/myapp:$(Build.BuildId)'
      
      postRouteTraffic:
        steps:
        - script: |
            echo "Monitoring canary at $(strategy.increment)%"
            # Wait and monitor
            sleep 180
        
        - script: |
            echo "Checking error rates"
            # Query monitoring system for error rates
            # If error rate > threshold, exit 1 to fail deployment
      
      on:
        failure:
          steps:
          - task: KubernetesManifest@0
            displayName: 'Reject canary deployment'
            inputs:
              action: 'reject'
              kubernetesServiceConnection: 'MyK8sConnection'
              namespace: 'production'
              strategy: 'canary'
        
        success:
          steps:
          - task: KubernetesManifest@0
            displayName: 'Promote canary deployment'
            inputs:
              action: 'promote'
              kubernetesServiceConnection: 'MyK8sConnection'
              namespace: 'production'
              strategy: 'canary'
```

## Best Practices

### 1. Use Appropriate Strategy

```yaml
# ✅ runOnce - For single target or managed PaaS
strategy:
  runOnce:

# ✅ rolling - For multiple VMs
strategy:
  rolling:
    maxParallel: 3

# ✅ canary - For progressive rollout
strategy:
  canary:
    increments: [10, 25, 50, 100]
```

### 2. Always Implement Rollback

```yaml
strategy:
  runOnce:
    deploy:
      steps:
      - script: echo "Deploying"
    
    on:
      failure:
        steps:
        - script: echo "Rolling back deployment"
        - task: AzureAppServiceManage@0
          inputs:
            action: 'Swap Slots'
            sourceSlot: 'production'
            swapWithProduction: false
```

### 3. Validate After Deployment

```yaml
postRouteTraffic:
  steps:
  - script: |
      echo "Running health check"
      response=$(curl -s -o /dev/null -w "%{http_code}" https://myapp.com/health)
      if [ $response -ne 200 ]; then
        echo "##vso[task.logissue type=error]Health check failed"
        exit 1
      fi
```

### 4. Use Environment Approvals

Configure manual approvals for production:
- Azure DevOps → Pipelines → Environments → production → Approvals and checks

```yaml
- deployment: DeployProduction
  environment: 'production'  # Configured with manual approval
  strategy:
    runOnce:
      deploy:
        steps:
        - script: echo "Deploying to production"
```

### 5. Track Deployment Metadata

```yaml
deploy:
  steps:
  - script: |
      echo "##vso[task.setvariable variable=deploymentId;isOutput=true]$(Build.BuildId)"
      echo "##vso[task.setvariable variable=deploymentTime;isOutput=true]$(date -u)"
    name: DeploymentJob
  
  - script: |
      echo "Deployment ID: $(deploymentId)"
      echo "Deployment Time: $(deploymentTime)"
```

## Quick Reference

### Deployment Job Structure

```yaml
jobs:
- deployment: JobName
  displayName: 'Display Name'
  environment: 'environmentName'
  pool:
    vmImage: 'ubuntu-latest'
  strategy:
    runOnce:  # or rolling: or canary:
      preDeploy:
        steps: []
      deploy:
        steps: []
      routeTraffic:
        steps: []
      postRouteTraffic:
        steps: []
      on:
        failure:
          steps: []
        success:
          steps: []
```

### Output Variable Syntax

```yaml
# Set in deployment job
- script: echo "##vso[task.setvariable variable=myVar;isOutput=true]value"
  name: DeploymentJobName  # Must match deployment job name

# Consume in same stage
$[ dependencies.DeploymentJobName.outputs['DeploymentJobName.DeploymentJobName.myVar'] ]

# Consume in different stage
$[ stageDependencies.StageName.DeploymentJobName.outputs['DeploymentJobName.DeploymentJobName.myVar'] ]
```

### Strategy Types

```yaml
# RunOnce
strategy:
  runOnce:
    deploy:
      steps: []

# Rolling
strategy:
  rolling:
    maxParallel: 2
    deploy:
      steps: []

# Canary
strategy:
  canary:
    increments: [10, 20, 50, 100]
    deploy:
      steps: []
```
