# Dataverse Solution Component Type Codes

Use these codes in `AddSolutionComponent`, `RemoveSolutionComponent`, and `UpdateSolutionComponent` API calls.

Source: [Microsoft Learn — Web API reference: solutioncomponent](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/reference/solutioncomponent)

---

## Most Common Types (Day-to-Day Development)

| Code | Name | Notes |
|------|------|-------|
| `1` | Entity | Custom table (use MetadataId from EntityDefinitions) |
| `2` | Attribute | Custom column (use MetadataId from EntityDefinitions Attributes) |
| `3` | Relationship | N:N relationship |
| `9` | Option Set | Global option set / choice column |
| `10` | Entity Relationship | 1:N or N:1 relationship |
| `14` | Entity Key | Alternate key on a table |
| `20` | Role | Security role |
| `24` | Form | Classic form (non-system) |
| `26` | Saved Query | View (system view) |
| `29` | Workflow | Classic workflow or Business Process Flow |
| `59` | Saved Query Visualization | Chart |
| `60` | System Form | Main/Quick View/Quick Create form |
| `61` | Web Resource | JavaScript, HTML, CSS, image, etc. |
| `62` | Site Map | App navigation site map |
| `66` | Custom Control | PCF control |
| `70` | Field Security Profile | Column security profile |
| `71` | Field Permission | Column permission record |
| `91` | Plugin Assembly | C# plugin DLL |
| `92` | SDK Message Processing Step | Plugin step registration |
| `93` | SDK Message Processing Step Image | Pre/post image registration |
| `95` | Service Endpoint | Azure Service Bus / webhook endpoint |
| `300` | Canvas App | Canvas Power App |
| `380` | Environment Variable Definition | Environment variable schema |
| `381` | Environment Variable Value | Environment variable value |
| `401` | AI Project | AI Builder project |

---

## Full Component Type Table

| Code | Name |
|------|------|
| 1 | Entity |
| 2 | Attribute |
| 3 | Relationship |
| 4 | Attribute Picklist Value |
| 5 | Attribute Lookup Value |
| 6 | View Attribute |
| 7 | Localized Label |
| 8 | Relationship Extra Condition |
| 9 | Option Set |
| 10 | Entity Relationship |
| 11 | Entity Relationship Role |
| 12 | Entity Relationship Relationships |
| 13 | Managed Property |
| 14 | Entity Key |
| 16 | Privilege |
| 17 | PrivilegeObjectTypeCode |
| 18 | Index |
| 20 | Role |
| 21 | Role Privilege |
| 22 | Display String |
| 23 | Display String Map |
| 24 | Form |
| 25 | Organization |
| 26 | Saved Query |
| 29 | Workflow |
| 31 | Report |
| 32 | Report Entity |
| 33 | Report Category |
| 34 | Report Visibility |
| 35 | Attachment |
| 36 | Email Template |
| 37 | Contract Template |
| 38 | KB Article Template |
| 39 | Mail Merge Template |
| 44 | Duplicate Rule |
| 45 | Duplicate Rule Condition |
| 46 | Entity Map |
| 47 | Attribute Map |
| 48 | Ribbon Command |
| 49 | Ribbon Context Group |
| 50 | Ribbon Customization |
| 52 | Ribbon Rule |
| 53 | Ribbon Tab To Command Map |
| 55 | Ribbon Diff |
| 59 | Saved Query Visualization |
| 60 | System Form |
| 61 | Web Resource |
| 62 | Site Map |
| 63 | Connection Role |
| 64 | Complex Control |
| 65 | Hierarchy Rule |
| 66 | Custom Control |
| 68 | Custom Control Default Config |
| 70 | Field Security Profile |
| 71 | Field Permission |
| 90 | Plugin Type |
| 91 | Plugin Assembly |
| 92 | SDK Message Processing Step |
| 93 | SDK Message Processing Step Image |
| 95 | Service Endpoint |
| 150 | Routing Rule |
| 151 | Routing Rule Item |
| 152 | SLA |
| 153 | SLA Item |
| 154 | Convert Rule |
| 155 | Convert Rule Item |
| 161 | Mobile Offline Profile |
| 162 | Mobile Offline Profile Item |
| 165 | Similarity Rule |
| 166 | Data Source Mapping |
| 201 | SDKMessage |
| 202 | SDKMessageFilter |
| 203 | SdkMessagePair |
| 204 | SdkMessageRequest |
| 205 | SdkMessageRequestField |
| 206 | SdkMessageResponse |
| 207 | SdkMessageResponseField |
| 208 | Import Map |
| 210 | WebWizard |
| 300 | Canvas App |
| 371 | Connector |
| 372 | Connector |
| 380 | Environment Variable Definition |
| 381 | Environment Variable Value |
| 400 | AI Project Type |
| 401 | AI Project |
| 402 | AI Configuration |
| 430 | Entity Analytics Configuration |
| 431 | Attribute Image Configuration |
| 432 | Entity Image Configuration |

---

## Resolving a Component ID by Type

Before calling `AddSolutionComponent`, resolve the component's GUID from the appropriate entity set:

| Component Type | Code | Resolution Endpoint |
|---|---|---|
| Entity | 1 | `GET /EntityDefinitions?$filter=LogicalName eq '{logicalname}'&$select=MetadataId` |
| Attribute | 2 | `GET /EntityDefinitions(LogicalName='{entity}')/Attributes?$filter=LogicalName eq '{attr}'&$select=MetadataId` |
| Global Option Set | 9 | `GET /GlobalOptionSetDefinitions?$filter=Name eq '{name}'&$select=MetadataId` |
| Role | 20 | `GET /roles?$filter=name eq '{name}'&$select=roleid` |
| View (Saved Query) | 26 | `GET /savedqueries?$filter=name eq '{name}'&$select=savedqueryid` |
| Workflow | 29 | `GET /workflows?$filter=name eq '{name}'&$select=workflowid` |
| System Form | 60 | `GET /systemforms?$filter=name eq '{name}'&$select=formid` |
| Web Resource | 61 | `GET /webresourceset?$filter=name eq '{name}'&$select=webresourceid` |
| Canvas App | 300 | `GET /canvasapps?$filter=name eq '{name}'&$select=canvasappid` |
| Env Variable Definition | 380 | `GET /environmentvariabledefinitions?$filter=schemaname eq '{name}'&$select=environmentvariabledefinitionid` |
| Plugin Assembly | 91 | `GET /pluginassemblies?$filter=name eq '{name}'&$select=pluginassemblyid` |
| SDK Message Processing Step | 92 | `GET /sdkmessageprocessingsteps?$filter=name eq '{name}'&$select=sdkmessageprocessingstepid` |
