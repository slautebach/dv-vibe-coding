# Dataverse Analyze Flows - References

This directory contains reference documentation for understanding Power Automate cloud flow structure and the Azure Logic Apps workflow definition schema that cloud flows are built upon.

## Power Automate Cloud Flow Structure

Power Automate cloud flows are exported as JSON files in the Dataverse solution with the following structure:

### File Location
```
**/<SolutionName>/Workflows/<FlowName>-<GUID>.json
```

### JSON Schema

```json
{
  "properties": {
    "displayName": "Human-readable flow name",
    "definition": {
      "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
      "contentVersion": "1.0.0.0",
      "parameters": {
        "$connections": {},
        "$authentication": {}
      },
      "triggers": {
        "TriggerName": {
          "type": "Recurrence|Request|ApiConnection",
          // Trigger-specific properties
        }
      },
      "actions": {
        "ActionName": {
          "type": "If|Foreach|ApiConnection|Compose|...",
          "runAfter": {
            "PreviousAction": ["Succeeded"]
          },
          // Action-specific properties
        }
      }
    },
    "connectionReferences": {
      "connector_name": {
        "runtimeSource": "embedded",
        "connection": {
          "connectionReferenceLogicalName": "mnp_ConnectionRef"
        },
        "api": {
          "name": "shared_commondataserviceforapps"
        }
      }
    }
  }
}
```

## Key Components

### Triggers
Define when the flow runs:
- **Recurrence**: Scheduled flows (runs on a timer)
- **Request**: HTTP-triggered flows (webhooks, HTTP requests)
- **ApiConnection**: Connector-triggered flows (e.g., Dataverse record created/updated)
- **Manual**: Instant flows (triggered manually by users)

### Actions
Define what the flow does:
- **Condition (If)**: Branching logic
- **Foreach**: Iteration over arrays
- **Scope**: Grouping actions (used for Try-Catch)
- **Compose**: Variable composition and data transformation
- **ApiConnection**: Calls to connectors (Dataverse, SharePoint, etc.)
- **OpenApiConnection**: Calls to OpenAPI-based connectors
- **Response**: HTTP response for Request-triggered flows

### Connection References
Map logical connection names to environment-specific connections:
- Enables deployment across environments
- References environment variables for connection strings
- Common connectors: Dataverse, SharePoint, Office 365, SQL Server

## Common Patterns

### Try-Catch Error Handling
```json
{
  "Try": {
    "type": "Scope",
    "actions": {
      // Main flow logic
    }
  },
  "Catch": {
    "type": "Scope",
    "runAfter": {
      "Try": ["Failed", "Skipped", "TimedOut"]
    },
    "actions": {
      // Error handling logic
    }
  }
}
```

### Apply to Each (Foreach Loop)
```json
{
  "Apply_to_each": {
    "type": "Foreach",
    "foreach": "@outputs('GetRecords')?['body/value']",
    "actions": {
      "ProcessItem": {
        // Action performed on each item
      }
    }
  }
}
```

### Conditional Logic
```json
{
  "Condition": {
    "type": "If",
    "expression": {
      "and": [
        {
          "equals": [
            "@variables('status')",
            "Active"
          ]
        }
      ]
    },
    "actions": {
      // True branch
    },
    "else": {
      "actions": {
        // False branch
      }
    }
  }
}
```

## Dataverse Actions

### List Records
```json
{
  "type": "OpenApiConnection",
  "inputs": {
    "host": {
      "connectionName": "shared_commondataserviceforapps",
      "operationId": "ListRecords"
    },
    "parameters": {
      "entityName": "accounts",
      "$filter": "statecode eq 0",
      "$top": 100,
      "$select": "accountid,name,emailaddress1"
    }
  }
}
```

### Update Record
```json
{
  "type": "OpenApiConnection",
  "inputs": {
    "host": {
      "connectionName": "shared_commondataserviceforapps",
      "operationId": "UpdateRecord"
    },
    "parameters": {
      "entityName": "accounts",
      "recordId": "@items('Apply_to_each')?['accountid']",
      "item/name": "Updated Name"
    }
  }
}
```

## Expression Language

Power Automate uses Workflow Definition Language (WDL) for expressions:

### Common Functions
- `@variables('variableName')` - Access variable
- `@parameters('paramName')` - Access parameter
- `@outputs('ActionName')` - Access action output
- `@items('ForEachName')` - Current item in loop
- `@triggerBody()` - Trigger payload
- `@contains(string, substring)` - String contains check
- `@equals(value1, value2)` - Equality comparison
- `@length(array)` - Array length
- `@concat(string1, string2)` - String concatenation

### Accessing JSON Properties
```javascript
@outputs('GetRecord')?['body/name']           // Safe navigation
@items('Apply_to_each')?['properties/email']  // Nested property access
```

## Useful Links

- [Azure Logic Apps Workflow Definition Language](https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-workflow-definition-language)
- [Power Automate Functions Reference](https://learn.microsoft.com/en-us/power-automate/workflow-functions)
- [Dataverse Connector Reference](https://learn.microsoft.com/en-us/connectors/commondataserviceforapps/)
- [Power Automate Best Practices](https://learn.microsoft.com/en-us/power-automate/guidance/planning/best-practices)

## Related Skills

- **dataverse-solution-parser**: Parse and analyze Dataverse solution XML files
- **n52-doc**: Analyze North52 Decision Suite formulas
- **plantuml**: Create PlantUML diagrams and images to visualize cloud flow logic
