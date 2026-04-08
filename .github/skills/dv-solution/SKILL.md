---
name: dv-solution
description: Create and manage Dataverse solutions, publishers, and solution components via the Web API. Use when asked to "create a solution", "add a component to a solution", "remove from solution", "list solution components", "create a publisher", "clone as patch", "check solution layers", or "what's in this solution?". Manages the full solution lifecycle through the Dataverse Web API — no pac CLI.
---

# Dataverse Solution Manager

Creates, updates, and manages Dataverse solutions, publishers, and solution component membership entirely through the Dataverse Web API. Never uses pac CLI for solution operations.

## Dataverse Skills Dependency

Requires the Dataverse-skills plugin for live operations:

```bash
copilot plugin marketplace add microsoft/Dataverse-skills
copilot plugin install dataverse@dataverse-skills
```

Before any live operation:
1. Load `dv-overview`
2. Use `dv-connect` to select the target environment and confirm auth context

**Authentication:** Uses `dataverse_sdk_client.py` (from `dataverse@dataverse-skills`). Browser popup by default; tokens cached in OS credential store. Set `CLIENT_ID` + `CLIENT_SECRET` in `.env` for service principal auth.

## Core Workflow

### Step 1: Resolve Solution Context

Before any operation, resolve the target solution:

```python
from dataverse_client import DataverseClient

client = DataverseClient()   # inherits auth context from dv-connect

# Query solution by unique name
response = client.get(
    "solutions",
    filter=f"uniquename eq '{unique_name}'",
    select="solutionid,uniquename,friendlyname,version,ismanaged,_publisherid_value"
)
```

- If the solution exists: check `ismanaged` — **never write to a managed solution**
- If the solution doesn't exist and the operation is **create**: proceed to Step 2
- If the solution doesn't exist and the operation is **add/remove/query components**: stop and report to user

### Step 2: Publisher Resolution

All solutions require a publisher. Resolve the publisher before creating a solution:

```python
# Look up publisher by customization prefix
response = client.get(
    "publishers",
    filter=f"customizationprefix eq '{prefix}'",
    select="publisherid,uniquename,friendlyname,customizationprefix"
)
```

- If found: use the returned `publisherid`
- If not found: offer to create the publisher (see [Publisher Management](#publisher-management))

See [references/publisher-api.md](references/publisher-api.md) for publisher creation payloads.

### Step 3: Solution CRUD

Only after confirming solution context and publisher, perform create/update/delete.

**Create solution:**

```python
payload = {
    "uniquename": "GrantsManagementCore",
    "friendlyname": "Grants Management Core",
    "description": "Core solution for the Grants Management engagement.",
    "version": "1.0.0.0",
    "publisherid@odata.bind": f"/publishers({publisher_id})"
}
response = client.post("solutions", payload)
solution_id = response.headers.get("OData-EntityId")
```

**Update solution (e.g., version bump):**

```python
client.patch(f"solutions({solution_id})", {"version": "1.1.0.0"})
```

**Delete solution:** Warn the user before deleting — deleting an unmanaged solution removes its customizations from the environment unless another solution layer covers them.

See [references/solution-api.md](references/solution-api.md) for full payloads and patch/clone operations.

### Step 4: Manage Solution Components

Use `AddSolutionComponent` and `RemoveSolutionComponent` for all component membership changes.

**Resolve the component ID before adding:**

| Component Type | Resolution Query |
|---|---|
| Entity | `GET /EntityDefinitions?$filter=LogicalName eq '{logicalname}'&$select=MetadataId` |
| Attribute | `GET /EntityDefinitions(LogicalName='{entity}')/Attributes?$filter=LogicalName eq '{attr}'&$select=MetadataId` |
| Web Resource | `GET /webresourceset?$filter=name eq '{name}'&$select=webresourceid` |
| Plugin Assembly | `GET /pluginassemblies?$filter=name eq '{name}'&$select=pluginassemblyid` |
| SDK Message Processing Step | `GET /sdkmessageprocessingsteps?$filter=name eq '{name}'&$select=sdkmessageprocessingstepid` |
| Workflow / Cloud Flow | `GET /workflows?$filter=name eq '{name}'&$select=workflowid` |
| Saved Query (View) | `GET /savedqueries?$filter=name eq '{name}'&$select=savedqueryid` |
| System Form | `GET /systemforms?$filter=name eq '{name}'&$select=formid` |
| Canvas App | `GET /canvasapps?$filter=name eq '{name}'&$select=canvasappid` |
| Environment Variable Definition | `GET /environmentvariabledefinitions?$filter=schemaname eq '{name}'&$select=environmentvariabledefinitionid` |

**Add component:**

```python
response = client.post("AddSolutionComponent", {
    "ComponentId": component_id,
    "ComponentType": component_type_code,   # see solution-component-types.md
    "SolutionUniqueName": solution_unique_name,
    "AddRequiredComponents": True,
    "DoNotIncludeSubcomponents": False,
    "IncludedComponentSettingsValues": None
})
```

**Remove component:**

First, look up the `solutioncomponentid` for the component within the solution:

```python
sc = client.get(
    "solutioncomponents",
    filter=f"_solutionid_value eq {solution_id} and objectid eq {component_id} and componenttype eq {component_type_code}",
    select="solutioncomponentid"
)
solution_component_id = sc['value'][0]['solutioncomponentid']

client.post("RemoveSolutionComponent", {
    "SolutionComponent": {
        "@odata.type": "Microsoft.Dynamics.CRM.solutioncomponent",
        "solutioncomponentid": solution_component_id
    },
    "ComponentType": component_type_code,
    "SolutionUniqueName": solution_unique_name
})
```

See [references/solution-component-types.md](references/solution-component-types.md) for the full component type code table.
See [references/component-operations-api.md](references/component-operations-api.md) for complete payload examples per component type.

### Step 5: Query Solution Components

List all components in a solution, grouped by type:

```python
# Get solution ID first, then query all components
components = client.get(
    "solutioncomponents",
    filter=f"_solutionid_value eq {solution_id}",
    select="componenttype,objectid,rootcomponentbehavior",
    orderby="componenttype asc"
)
```

Group results by component type (using type code → name mapping from `solution-component-types.md`) and display as a markdown table.

### Step 6: Output Summary

After any write operation, output a confirmation table:

```markdown
## Solution: GrantsManagementCore

| Property | Value |
|---|---|
| Unique Name | GrantsManagementCore |
| Display Name | Grants Management Core |
| Version | 1.0.0.0 |
| Publisher | MNP Digital (mnp) |
| Managed | No |

### Components Added

| Component Type | Name / Logical Name | Component ID |
|---|---|---|
| Entity | mnp_application | {guid} |
| Attribute | mnp_submittedon | {guid} |
| Web Resource | mnp_Common.FormHelpers.js | {guid} |
```

## Inspect Mode

When asked "What's in this solution?" or "List the components in solution X":

1. Resolve the solution ID (Step 1)
2. Query all solution components (Step 5)
3. For each component, resolve the display name where possible (entity logical name, web resource name, etc.)
4. Group by component type name and display as a table
5. **Read-only** — do not stage or modify anything

## Patch Mode

When asked to "create a patch" or "clone as patch for a hotfix":

```python
client.post("CloneAsPatch", {
    "DisplayName": "Grants Management Core - Patch 1",
    "VersionNumber": "1.0.1.0",
    "SolutionUniqueName": "GrantsManagementCore"
})
```

> **Important:** Patches can only contain components already present in the base solution. After creating the patch, all subsequent `AddSolutionComponent` calls should target the patch solution unique name, not the base solution.

When asked to "promote a patch" or "merge patch back into solution":

```python
client.post("DeleteAndPromote", {
    "UniqueName": "GrantsManagementCoreHotfix1"
})
```

## Publisher Management

When no publisher exists for a given prefix, offer to create one before creating the solution:

```python
client.post("publishers", {
    "uniquename": "mnpdigital",
    "friendlyname": "MNP Digital",
    "description": "MNP Digital publisher for Dynamics 365 solutions.",
    "customizationprefix": "mnp",
    "customizationoptionvalueprefix": 12345,
    "address1_addresstypecode": 1
})
```

> `customizationoptionvalueprefix` must be a unique integer between 10000 and 99999. Use a project-specific number to avoid collisions.

See [references/publisher-api.md](references/publisher-api.md) for full publisher payloads.

## Example Prompts

- "Create a new unmanaged solution called GrantsManagementCore using the mnp publisher"
- "Add the mnp_application entity and all its attributes to the GrantsManagementCore solution"
- "What components are currently in the CCX solution?"
- "Remove the mnp_legacyfield attribute from the GrantsManagementCore solution"
- "Clone the GrantsManagementCore solution as a patch for version 1.0.1"
- "Create an MNP Digital publisher with prefix mnp"
- "Check which solution owns the mnp_application entity"

## Reference Files

| File | When to read |
|---|---|
| [references/solution-api.md](references/solution-api.md) | When creating, updating, cloning, or querying solutions — full Web API payloads |
| [references/solution-component-types.md](references/solution-component-types.md) | Always when adding or removing components — component type code reference |
| [references/component-operations-api.md](references/component-operations-api.md) | When building AddSolutionComponent / RemoveSolutionComponent / UpdateSolutionComponent payloads |
| [references/publisher-api.md](references/publisher-api.md) | When creating or querying publishers |
