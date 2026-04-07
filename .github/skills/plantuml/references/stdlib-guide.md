# PlantUML Standard Library (stdlib) Guide

Complete guide to using PlantUML's standard library for cloud providers, icons, and pre-built sprites.

## Overview

PlantUML's standard library (stdlib) provides pre-built icons and sprites for:
- **Cloud Providers**: AWS, Azure, GCP, IBM Cloud
- **Technologies**: Kubernetes, Docker, databases
- **Icon Sets**: Font Awesome, Material Design, Office
- **Specialized**: C4 Model, ArchiMate, networking

Libraries are hosted on GitHub and loaded via `!include` directives.

## Basic Usage

### Include Syntax

```plantuml
!include <library/path/to/icon>
```

### Using Icons

After including, reference icons with `$iconname`:

```plantuml
@startuml
!include <awslib/Compute/EC2>
EC2(server, "Web Server", "t3.medium")
@enduml
```

## AWS Icons

**Repository**: https://github.com/awslabs/aws-icons-for-plantuml

### Setup

```plantuml
!include <awslib/AWSCommon>
!include <awslib/Category/Service>
```

### Common Services

#### Compute
```plantuml
!include <awslib/Compute/EC2>
!include <awslib/Compute/Lambda>
!include <awslib/Compute/ECS>
!include <awslib/Compute/EKS>
!include <awslib/Compute/ElasticBeanstalk>
!include <awslib/Compute/Lightsail>
!include <awslib/Compute/AutoScaling>

EC2(ec2, "EC2 Instance", "t3.large")
Lambda(lambda, "Lambda Function", "Node.js 18")
ECS(ecs, "ECS Cluster", "Fargate")
EKS(eks, "Kubernetes", "v1.28")
```

#### Storage
```plantuml
!include <awslib/Storage/S3>
!include <awslib/Storage/EBS>
!include <awslib/Storage/EFS>
!include <awslib/Storage/FSx>
!include <awslib/Storage/StorageGateway>

S3(bucket, "S3 Bucket", "Data Lake")
EBS(volume, "EBS Volume", "1TB SSD")
EFS(fs, "Shared Storage", "NFS")
```

#### Database
```plantuml
!include <awslib/Database/RDS>
!include <awslib/Database/DynamoDB>
!include <awslib/Database/ElastiCache>
!include <awslib/Database/Aurora>
!include <awslib/Database/Redshift>
!include <awslib/Database/Neptune>
!include <awslib/Database/DocumentDB>

RDS(rds, "RDS PostgreSQL", "Multi-AZ")
DynamoDB(dynamo, "DynamoDB", "Users Table")
ElastiCache(cache, "Redis", "Cluster Mode")
Aurora(aurora, "Aurora", "Serverless v2")
```

#### Networking
```plantuml
!include <awslib/NetworkingContentDelivery/VPC>
!include <awslib/NetworkingContentDelivery/CloudFront>
!include <awslib/NetworkingContentDelivery/Route53>
!include <awslib/NetworkingContentDelivery/APIGateway>
!include <awslib/NetworkingContentDelivery/ElasticLoadBalancing>
!include <awslib/NetworkingContentDelivery/DirectConnect>

VPC(vpc, "VPC", "10.0.0.0/16")
CloudFront(cdn, "CloudFront", "CDN")
Route53(dns, "Route 53", "DNS")
APIGateway(api, "API Gateway", "REST API")
ElasticLoadBalancing(alb, "ALB", "Load Balancer")
```

#### Security & Identity
```plantuml
!include <awslib/SecurityIdentityCompliance/IAM>
!include <awslib/SecurityIdentityCompliance/Cognito>
!include <awslib/SecurityIdentityCompliance/SecretsManager>
!include <awslib/SecurityIdentityCompliance/WAF>
!include <awslib/SecurityIdentityCompliance/Shield>
!include <awslib/SecurityIdentityCompliance/GuardDuty>

IAM(iam, "IAM", "Roles & Policies")
Cognito(cognito, "Cognito", "User Pool")
SecretsManager(secrets, "Secrets Manager", "API Keys")
``` #### Messaging & Integration
```plantuml
!include <awslib/ApplicationIntegration/SQS>
!include <awslib/ApplicationIntegration/SNS>
!include <awslib/ApplicationIntegration/EventBridge>
!include <awslib/ApplicationIntegration/StepFunctions>

SQS(queue, "SQS Queue", "Task Queue")
SNS(topic, "SNS Topic", "Notifications")
EventBridge(events, "EventBridge", "Event Bus")
StepFunctions(workflow, "Step Functions", "Orchestration")
```

#### Management & Monitoring
```plantuml
!include <awslib/ManagementGovernance/CloudWatch>
!include <awslib/ManagementGovernance/CloudFormation>
!include <awslib/ManagementGovernance/SystemsManager>
!include <awslib/ManagementGovernance/CloudTrail>

CloudWatch(cw, "CloudWatch", "Logs & Metrics")
CloudFormation(cf, "CloudFormation", "IaC")
SystemsManager(ssm, "Systems Manager", "Parameter Store")
```

### Complete AWS Example

```plantuml
@startuml
!include <awslib/AWSCommon>
!include <awslib/Compute/Lambda>
!include <awslib/Database/DynamoDB>
!include <awslib/Storage/S3>
!include <awslib/NetworkingContentDelivery/APIGateway>

APIGateway(api, "API Gateway", "REST API")
Lambda(lambda, "Lambda", "Business Logic")
DynamoDB(db, "DynamoDB", "User Data")
S3(storage, "S3", "File Storage")

api -> lambda
lambda -> db
lambda -> storage
@enduml
```

## Azure Icons

**Repository**: https://github.com/plantuml-stdlib/Azure-PlantUML

### Setup

```plantuml
!define AzurePuml https://raw.githubusercontent.com/plantuml-stdlib/Azure-PlantUML/release/2-2/dist
!include AzurePuml/AzureCommon.puml
!include AzurePuml/Category/Service.puml
```

### Common Services

#### Compute
```plantuml
!include AzurePuml/Compute/AzureFunction.puml
!include AzurePuml/Compute/AzureAppService.puml
!include AzurePuml/Compute/AzureKubernetesService.puml
!include AzurePuml/Compute/AzureVirtualMachine.puml
!include AzurePuml/Compute/AzureContainerInstance.puml

AzureFunction(func, "Function App", "Serverless")
AzureAppService(webapp, "App Service", "Web App")
AzureKubernetesService(aks, "AKS", "Kubernetes")
AzureVirtualMachine(vm, "VM", "Windows Server")
```

#### Storage & Databases
```plantuml
!include AzurePuml/Storage/AzureBlobStorage.puml
!include AzurePuml/Storage/AzureFileStorage.puml
!include AzurePuml/Databases/AzureCosmosDb.puml
!include AzurePuml/Databases/AzureSqlDatabase.puml
!include AzurePuml/Databases/AzureRedisCache.puml

AzureBlobStorage(blob, "Blob Storage", "Hot Tier")
AzureCosmosDb(cosmos, "Cosmos DB", "NoSQL")
AzureSqlDatabase(sql, "SQL Database", "S2 Tier")
AzureRedisCache(redis, "Redis Cache", "Standard")
```

#### Networking
```plantuml
!include AzurePuml/Networking/AzureApplicationGateway.puml
!include AzurePuml/Networking/AzureLoadBalancer.puml
!include AzurePuml/Networking/AzureVirtualNetwork.puml
!include AzurePuml/Networking/AzureDNS.puml

AzureApplicationGateway(appgw, "App Gateway", "WAF")
AzureLoadBalancer(lb, "Load Balancer", "Standard")
AzureVirtualNetwork(vnet, "VNet", "10.0.0.0/16")
```

#### Integration
```plantuml
!include AzurePuml/Integration/AzureServiceBus.puml
!include AzurePuml/Integration/AzureEventGrid.puml
!include AzurePuml/Integration/AzureLogicApps.puml

AzureServiceBus(bus, "Service Bus", "Premium")
AzureEventGrid(grid, "Event Grid", "Custom Topics")
AzureLogicApps(logic, "Logic Apps", "Workflow")
```

### Complete Azure Example

```plantuml
@startuml
!define AzurePuml https://raw.githubusercontent.com/plantuml-stdlib/Azure-PlantUML/release/2-2/dist
!include AzurePuml/AzureCommon.puml
!include AzurePuml/Compute/AzureFunction.puml
!include AzurePuml/Databases/AzureCosmosDb.puml
!include AzurePuml/Storage/AzureBlobStorage.puml

AzureFunction(api, "HTTP Trigger", "Node.js")
AzureCosmosDb(db, "Cosmos DB", "SQL API")
AzureBlobStorage(storage, "Blob Storage", "Images")

api -> db : Read/Write
api -> storage : Upload
@enduml
```

## Google Cloud Platform (GCP)

**Repository**: https://github.com/Piotr1215/gcp-plantuml

### Setup

```plantuml
!define GCPPuml https://raw.githubusercontent.com/Piotr1215/gcp-plantuml/master/dist
!include GCPPuml/GCPCommon.puml
!include GCPPuml/Category/Service.puml
```

### Common Services

```plantuml
!include GCPPuml/Compute/ComputeEngine.puml
!include GCPPuml/Compute/CloudRun.puml
!include GCPPuml/Compute/CloudFunctions.puml
!include GCPPuml/Compute/GKE.puml
!include GCPPuml/Storage/CloudStorage.puml
!include GCPPuml/Database/CloudSQL.puml
!include GCPPuml/Database/Firestore.puml

ComputeEngine(vm, "VM Instance", "e2-medium")
CloudRun(service, "Cloud Run", "Container")
CloudFunctions(func, "Function", "Python 3.11")
GKE(cluster, "GKE", "Standard")
CloudStorage(bucket, "Cloud Storage", "Standard")
CloudSQL(db, "Cloud SQL", "PostgreSQL")
Firestore(nosql, "Firestore", "Native Mode")
```

## Kubernetes

**Repository**: Built into PlantUML stdlib

### Setup

```plantuml
!include <kubernetes/k8s-sprites-unlabeled-25pct>
```

### Common Resources

```plantuml
@startuml
!include <kubernetes/k8s-sprites-unlabeled-25pct>

rectangle "Kubernetes Cluster" {
  <$pod> as pod1
  <$pod> as pod2
  <$service> as svc
  <$deployment> as deploy
  <$ingress> as ingress
  <$configmap> as cm
  <$secret> as secret
  <$pv> as pv
  <$pvc> as pvc
}

ingress --> svc
svc --> pod1
svc --> pod2
deploy ..> pod1
deploy ..> pod2
pod1 ..> cm
pod1 ..> secret
pvc --> pv
@enduml
```

### Available Sprites

- `<$pod>` - Pod
- `<$deploy>` / `<$deployment>` - Deployment
- `<$svc>` / `<$service>` - Service
- `<$ing>` / `<$ingress>` - Ingress
- `<$ns>` / `<$namespace>` - Namespace
- `<$cm>` / `<$configmap>` - ConfigMap
- `<$secret>` - Secret
- `<$pv>` - PersistentVolume
- `<$pvc>` - PersistentVolumeClaim
- `<$sc>` / `<$storageclass>` - StorageClass
- `<$hpa>` - HorizontalPodAutoscaler
- `<$job>` - Job
- `<$cronjob>` - CronJob

## Font Awesome

**Repository**: Built into PlantUML stdlib

### Setup

```plantuml
!include <font-awesome-5/icon_name>
```

### Common Icons

```plantuml
!include <font-awesome-5/users>
!include <font-awesome-5/database>
!include <font-awesome-5/server>
!include <font-awesome-5/laptop>
!include <font-awesome-5/mobile>
!include <font-awesome-5/cloud>
!include <font-awesome-5/lock>
!include <font-awesome-5/key>
!include <font-awesome-5/shield_alt>
!include <font-awesome-5/cog>
!include <font-awesome-5/chart_line>
!include <font-awesome-5/envelope>

<$users> Users
<$database> Database
<$server> Server
<$laptop> Desktop
<$mobile> Mobile
<$cloud> Cloud
<$lock> Security
<$cog> Settings
```

### Usage in Diagrams

```plantuml
@startuml
!include <font-awesome-5/users>
!include <font-awesome-5/database>
!include <font-awesome-5/server>

rectangle "<$users>\nUser Management" as user_mgmt
rectangle "<$server>\nApplication" as app
database "<$database>\nDatabase" as db

user_mgmt --> app
app --> db
@enduml
```

## Material Design Icons

**Repository**: Built into PlantUML stdlib

### Setup

```plantuml
!include <material/icon_name>
```

### Common Icons

```plantuml
!include <material/computer>
!include <material/phone_android>
!include <material/cloud>
!include <material/storage>
!include <material/security>
!include <material/settings>
!include <material/dashboard>
!include <material/person>

<$computer> Desktop
<$phone_android> Mobile
<$cloud> Cloud
<$storage> Storage
<$security> Security
<$settings> Settings
```

## Office Icons

**Repository**: Built into PlantUML stdlib

### Setup

```plantuml
!include <office/Category/icon>
```

### Common Icons

```plantuml
!include <office/Servers/database_server>
!include <office/Servers/application_server>
!include <office/Servers/web_server>
!include <office/Devices/device_laptop>
!include <office/Devices/device_smartphone>
!include <office/Services/office_365>
!include <office/Communications/email>

<$database_server> Database
<$application_server> App Server
<$web_server> Web Server
<$device_laptop> Laptop
<$office_365> Office 365
```

## C4 Model

**Repository**: https://github.com/plantuml-stdlib/C4-PlantUML

### Setup

```plantuml
!include <C4/C4_Context>
!include <C4/C4_Container>
!include <C4/C4_Component>
!include <C4/C4_Deployment>
```

### Example

```plantuml
@startuml
!include <C4/C4_Container>

Person(user, "User", "A user of the system")
System_Boundary(c1, "System") {
    Container(web, "Web App", "React", "UI")
    Container(api, "API", "Node.js", "REST API")
    ContainerDb(db, "Database", "PostgreSQL", "Data store")
}

Rel(user, web, "Uses", "HTTPS")
Rel(web, api, "Calls", "JSON/HTTPS")
Rel(api, db, "Reads/Writes", "SQL")
@enduml
```

## Browsing Available Libraries

### List All Libraries

```bash
java -jar plantuml.jar -stdlib
```

### View Specific Library

```bash
java -jar plantuml.jar -stdlib awslib
java -jar plantuml.jar -stdlib kubernetes
```

### Online Browse

Visit: https://plantuml.com/stdlib

## Creating Custom Libraries

### Local Include

Create reusable components in separate files:

**common-components.puml:**
```plantuml
!procedure $CustomService($alias, $label, $tech)
  component "$label\n<size:10>$tech</size>" as $alias #LightBlue
!endprocedure

!procedure $CustomDatabase($alias, $label, $type)
  database "$label\n<size:10>$type</size>" as $alias #LightGreen
!endprocedure
```

**Use in diagrams:**
```plantuml
@startuml
!include common-components.puml

$CustomService(auth, "Auth Service", "Node.js")
$CustomService(user, "User Service", "Java")
$CustomDatabase(db, "Main DB", "PostgreSQL")

auth --> db
user --> db
@enduml
```

## Best Practices

1. **Use AWSCommon/AzureCommon**: Always include the common file first
2. **Consistent color schemes**: Stick to provider's official colors
3. **Label components**: Add names and descriptions for clarity
4. **Group by function**: Use packages to organize components
5. **Version control libraries**: Pin to specific releases for stability
6. **Test locally**: Verify icons render before committing
7. **Document dependencies**: List required libraries in diagram comments
8. **Use aliases**: Simplify long icon names with `as` keyword

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Icon not found | Check library path, use `-stdlib` to verify |
| Slow rendering | Reduce number of included libraries |
| Missing icons | Update PlantUML to latest version |
| Network errors | Libraries fetched from GitHub; check connectivity |
| Syntax errors | Verify parentheses and commas in icon macros |

## Resources

- **PlantUML Standard Library**: https://plantuml.com/stdlib
- **AWS Icons**: https://github.com/awslabs/aws-icons-for-plantuml
- **Azure Icons**: https://github.com/plantuml-stdlib/Azure-PlantUML
- **C4 Model**: https://github.com/plantuml-stdlib/C4-PlantUML
- **Icon Reference**: https://plantuml.com/stdlib

---

**Last Updated**: February 2026  
**Version**: 1.0
