# MNP Action Standards

## Design Guidance

### Purpose
Use **Actions** to centralize feature logic, validations, and rules that are called from multiple tables or workflows (polymorphism).

**Example**: An email notification called from multiple CRUD workflows should be centralized in ONE action. When the email template changes, only one action needs updating.

### Naming Convention
- Pattern: `{Action} - Action - MNP`
- Note: Omit `{Table}` — actions are intended to be polymorphic, not table-scoped.
- Examples: `Send Notification - Action - MNP`, `Validate Application - Action - MNP`

### Parameters
- When passing entities into an Action, use **EntityReference** (not Entity) as the parameter type.

### Ownership
- All Actions must be owned by the **Service Account**, not individual users.

### When to Use Actions vs Workflow Activities

| Use | When |
|---|---|
| Action | Reusable logic called from multiple workflows or client-side code |
| Workflow Activity (CodeActivity) | Low-level computation not available in declarative tools |
| Plugin (IPlugin) | Synchronous pipeline enforcement, pre/post image validation |

### Invoking Actions from Plugins

Actions can be invoked from plugin code using `OrganizationRequest`:

```csharp
var request = new OrganizationRequest("mnp_ActionLogicalName");
request["InputParam"] = new EntityReference("mnp_entity", recordId);
var response = service.Execute(request);
var output = response["OutputParam"] as string;
```

### Invoking Actions from Client-Side JavaScript

```javascript
Xrm.WebApi.online.execute({
    getMetadata: () => ({
        boundParameter: null,
        parameterTypes: {
            "InputParam": { typeName: "Microsoft.Dynamics.CRM.EntityReference", structuralProperty: 5 }
        },
        operationType: 0,
        operationName: "mnp_ActionLogicalName"
    }),
    InputParam: { entityType: "mnp_entity", id: recordId }
});
```
