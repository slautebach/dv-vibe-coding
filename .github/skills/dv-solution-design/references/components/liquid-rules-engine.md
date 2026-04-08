# Component: Liquid Rules Engine

**Source:** https://dev.azure.com/MNPDigital/DC-Delivery/_git/DC-StarterKits_Solution?path=/SharedLibraries/LiquidRuleEngine

## Overview

The LiquidRuleEngine library allows any CRM plugin, Azure Function App, or other application to interpret Liquid templates and perform actions based on the result. It enables rule-driven field updates using a flexible templating approach.

## Getting Started

### Environment Setup

**Option A: Power Pages with Enhanced Data Model**
- No additional setup needed (web templates are used natively)

**Option B: Custom Tables**
- Create a Dataverse table with at minimum a multiline text field (for the Liquid source code)
- Decide how to reference the template to run and create an appropriate field
- Configure the plugin step to point to this table

### Plugin Setup

1. Download the project from source control
2. Copy to your plugin solution folder
3. Open the solution in Visual Studio
4. Add the `LiquidRuleEngine` project to the solution
5. Add a reference to `LiquidRuleEngine` in your plugin project
6. Configure the plugin step (unsecured configuration)

## Plugin Step Configuration (Unsecured Config JSON)

```json
{
  "liquidIterations": 100,
  "targetVariableName": "target",
  "webtemplateEnabled": true,
  "additionalFileSystems": [],
  "templateSelection": {
    "templateName": "LiquidRuleEngine"
  }
}
```

### Custom Table + Target-Based Template Selection

```json
{
  "webtemplateEnabled": false,
  "additionalFileSystems": [{
    "entity": "mnp_appsectionconfig",
    "sourcefield": "mnp_liquidvalidation",
    "namefield": "mnp_appsectionconfigid"
  }],
  "templateSelection": {
    "basedOnTarget": true,
    "targetFieldName": "mnp_appsectionconfig"
  }
}
```

| Config Property | Default | Description |
|---|---|---|
| `liquidIterations` | 100 | Max loop iterations in the Liquid template |
| `targetVariableName` | `"target"` | Liquid variable name for the target entity |
| `webtemplateEnabled` | `true` | Use `mspp_webtemplate` as a template source |
| `additionalFileSystems` | `[]` | Array of custom table sources for templates |
| `templateSelection.basedOnTarget` | `false` | Look up template name from a field on the target record |
| `templateSelection.targetFieldName` | unset | Field on target entity containing the template name |
| `templateSelection.templateName` | `"LiquidRuleEngine"` | Fixed template name when not target-based |

## Writing the Return Value

The Liquid template must return a JSON array of record update instructions:

```json
[{
  "logicalName": "account",
  "recordId": "00000000-0000-0000-0000-000000000000",
  "name": "Updated Account Name"
}]
```

Each object specifies the table (`logicalName`), record (`recordId`), and any fields to update.

## Available Liquid Objects

| Object | Syntax | Description |
|---|---|---|
| `entities` | `entities["tablename"]["guid"]` or `entities.tablename[id]` | Access any Dataverse record by table and ID |
| `target` | `target.fieldname` | The triggering entity record (name set by `targetVariableName`) |

## Available Liquid Tags

### `fetchxml`

Execute a FetchXML query and use the results in the template:

```liquid
{% fetchxml myResults %}
<fetch>
  <entity name="account">
    <attribute name="name" />
    <filter>
      <condition attribute="name" operator="eq" value="Test" />
    </filter>
  </entity>
</fetch>
{% endfetchxml %}
{% assign account = myResults.results.entities[0] %}
{{ account.name }}
```

## Public API

| Method | Description |
|---|---|
| `RunAndApplyRules` | Main entry point. Renders the template using config, then applies the JSON return to update Dataverse records. |
| `RenderTemplate` | Core rendering only. Returns the rendered Liquid output for custom handling -- use to extend beyond the standard JSON return format. |
