# Dataverse Web API — Entity Metadata Endpoints

All endpoints are relative to `{env_url}/api/data/v9.2/`.

## Create Table (Entity)

**POST** `/api/data/v9.2/EntityDefinitions`

```json
{
  "@odata.type": "Microsoft.Dynamics.CRM.EntityMetadata",
  "SchemaName": "mnp_Application",
  "LogicalName": "mnp_application",
  "DisplayName": {
    "@odata.type": "Microsoft.Dynamics.CRM.Label",
    "LocalizedLabels": [
      {
        "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
        "Label": "Application",
        "LanguageCode": 1033
      }
    ]
  },
  "DisplayCollectionName": {
    "@odata.type": "Microsoft.Dynamics.CRM.Label",
    "LocalizedLabels": [
      {
        "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
        "Label": "Applications",
        "LanguageCode": 1033
      }
    ]
  },
  "Description": {
    "@odata.type": "Microsoft.Dynamics.CRM.Label",
    "LocalizedLabels": [
      {
        "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
        "Label": "Tracks grant applications submitted by clients.",
        "LanguageCode": 1033
      }
    ]
  },
  "OwnershipType": "UserOwned",
  "IsAuditEnabled": {
    "Value": true,
    "CanBeChanged": true,
    "ManagedPropertyLogicalName": "canauditentity"
  },
  "HasActivities": false,
  "HasNotes": false,
  "PrimaryNameAttribute": "mnp_name"
}
```

**OwnershipType values:**
- `"UserOwned"` — User or Team ownership (default for most tables)
- `"OrganizationOwned"` — Organization-owned (for reference/lookup tables only)

**Response:** `201 Created` with `OData-EntityId` header containing the new entity MetadataId URL.

## Update Table

**PATCH** `/api/data/v9.2/EntityDefinitions({MetadataId})`

Send only the properties to change. Use `MERGE` semantics (partial update).

## Add Attribute to Table

**POST** `/api/data/v9.2/EntityDefinitions(LogicalName='{entity}')/Attributes`

### String Attribute

```json
{
  "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
  "SchemaName": "mnp_Name",
  "LogicalName": "mnp_name",
  "RequiredLevel": { "Value": "None", "CanBeChanged": true, "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings" },
  "DisplayName": { "@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [{ "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel", "Label": "Name", "LanguageCode": 1033 }] },
  "Description": { "@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [{ "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel", "Label": "Name of the application.", "LanguageCode": 1033 }] },
  "MaxLength": 100,
  "IsAuditEnabled": { "Value": true, "CanBeChanged": true, "ManagedPropertyLogicalName": "canauditattribute" }
}
```

### Lookup Attribute (requires relationship)

```json
{
  "@odata.type": "Microsoft.Dynamics.CRM.LookupAttributeMetadata",
  "SchemaName": "mnp_ContactId",
  "LogicalName": "mnp_contactid",
  "DisplayName": { "@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [{ "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel", "Label": "Contact", "LanguageCode": 1033 }] },
  "Description": { "@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [{ "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel", "Label": "The contact associated with this application.", "LanguageCode": 1033 }] },
  "RequiredLevel": { "Value": "None", "CanBeChanged": true, "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings" },
  "IsAuditEnabled": { "Value": true, "CanBeChanged": true, "ManagedPropertyLogicalName": "canauditattribute" }
}
```

### DateTime Attribute

```json
{
  "@odata.type": "Microsoft.Dynamics.CRM.DateTimeAttributeMetadata",
  "SchemaName": "mnp_SubmittedOn",
  "LogicalName": "mnp_submittedon",
  "DisplayName": { "@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [{ "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel", "Label": "Submitted On", "LanguageCode": 1033 }] },
  "Description": { "@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [{ "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel", "Label": "Date the application was submitted.", "LanguageCode": 1033 }] },
  "DateTimeBehavior": { "Value": "UserLocal" },
  "Format": "DateAndTime",
  "RequiredLevel": { "Value": "None", "CanBeChanged": true, "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings" },
  "IsAuditEnabled": { "Value": true, "CanBeChanged": true, "ManagedPropertyLogicalName": "canauditattribute" }
}
```

**DateTimeBehavior values:** `"UserLocal"` | `"DateOnly"` | `"TimeZoneIndependent"`

### Currency Attribute

```json
{
  "@odata.type": "Microsoft.Dynamics.CRM.MoneyAttributeMetadata",
  "SchemaName": "mnp_GrantAmount",
  "LogicalName": "mnp_grantamount",
  "DisplayName": { "@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [{ "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel", "Label": "Grant Amount", "LanguageCode": 1033 }] },
  "Description": { "@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [{ "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel", "Label": "Total approved grant amount.", "LanguageCode": 1033 }] },
  "RequiredLevel": { "Value": "None", "CanBeChanged": true, "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings" },
  "IsAuditEnabled": { "Value": true, "CanBeChanged": true, "ManagedPropertyLogicalName": "canauditattribute" }
}
```

### Boolean (Two Option) Attribute

```json
{
  "@odata.type": "Microsoft.Dynamics.CRM.BooleanAttributeMetadata",
  "SchemaName": "mnp_IsApproved",
  "LogicalName": "mnp_isapproved",
  "DisplayName": { "@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [{ "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel", "Label": "Is Approved", "LanguageCode": 1033 }] },
  "Description": { "@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [{ "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel", "Label": "Indicates whether the application has been approved.", "LanguageCode": 1033 }] },
  "OptionSet": {
    "@odata.type": "Microsoft.Dynamics.CRM.BooleanOptionSetMetadata",
    "TrueOption": { "Value": 1, "Label": { "@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [{ "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel", "Label": "Yes", "LanguageCode": 1033 }] } },
    "FalseOption": { "Value": 0, "Label": { "@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [{ "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel", "Label": "No", "LanguageCode": 1033 }] } }
  },
  "RequiredLevel": { "Value": "None", "CanBeChanged": true, "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings" },
  "IsAuditEnabled": { "Value": true, "CanBeChanged": true, "ManagedPropertyLogicalName": "canauditattribute" }
}
```

### Integer Attribute

```json
{
  "@odata.type": "Microsoft.Dynamics.CRM.IntegerAttributeMetadata",
  "SchemaName": "mnp_TermInMonths",
  "LogicalName": "mnp_terminmonths",
  "DisplayName": { "@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [{ "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel", "Label": "Term (Months)", "LanguageCode": 1033 }] },
  "Description": { "@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [{ "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel", "Label": "Loan term expressed in months.", "LanguageCode": 1033 }] },
  "Format": "None",
  "MinValue": 0,
  "MaxValue": 2147483647,
  "RequiredLevel": { "Value": "None", "CanBeChanged": true, "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings" },
  "IsAuditEnabled": { "Value": true, "CanBeChanged": true, "ManagedPropertyLogicalName": "canauditattribute" }
}
```

## Update Attribute

**PUT** `/api/data/v9.2/EntityDefinitions(LogicalName='{entity}')/Attributes(LogicalName='{attribute}')`

Note: Use **PUT** (full replacement) for attribute updates, not PATCH.

## Add Entity to Solution Layer

After creating an entity, add it to the target solution using `AddSolutionComponentRequest`:

**POST** `/api/data/v9.2/AddSolutionComponent`

```json
{
  "ComponentId": "{EntityMetadataId}",
  "ComponentType": 1,
  "SolutionUniqueName": "IncomeAssistanceCore",
  "AddRequiredComponents": true,
  "DoNotIncludeSubcomponents": false,
  "IncludedComponentSettingsValues": null
}
```

**Component type codes:**
- `1` = Entity
- `2` = Attribute
- `10` = Relationship
- `59` = System Form
- `26` = Saved Query (View)

## SchemaName Conventions

SchemaName is the PascalCase version of the logical name:
- LogicalName: `mnp_application` → SchemaName: `mnp_Application`
- LogicalName: `mnp_contactid` → SchemaName: `mnp_ContactId`
- LogicalName: `mnp_isapproved` → SchemaName: `mnp_IsApproved`
- LogicalName: `mnp_submittedon` → SchemaName: `mnp_SubmittedOn`

## RequiredLevel Values

- `"None"` — Optional
- `"Recommended"` — Business recommended
- `"ApplicationRequired"` — Required by application
- `"SystemRequired"` — System required (platform-managed only)

## Authentication

Uses `DataverseClient` from `.github/scripts/dataverse_client.py`. See that file for connection setup. Always call `client.connect()` before any metadata write operations.
