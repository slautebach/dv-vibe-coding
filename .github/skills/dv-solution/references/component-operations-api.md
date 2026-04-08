# Dataverse Web API — Solution Component Operations

All endpoints are relative to `{env_url}/api/data/v9.2/`.

Source: [Microsoft Learn — AddSolutionComponent](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/reference/addsolutioncomponent)  
Source: [Microsoft Learn — RemoveSolutionComponent](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/reference/removesolutioncomponent)

---

## AddSolutionComponent

**POST** `/api/data/v9.2/AddSolutionComponent`

Adds a component to an **unmanaged** solution.

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `ComponentId` | Guid | Yes | ID of the component (MetadataId for metadata types; record GUID for data types) |
| `ComponentType` | Int32 | Yes | Component type code — see `solution-component-types.md` |
| `SolutionUniqueName` | String | Yes | Unique name of the target solution |
| `AddRequiredComponents` | Boolean | Yes | If `true`, also adds any components this component depends on |
| `DoNotIncludeSubcomponents` | Boolean | No | If `true`, adds only the root component without child components (e.g., entity without attributes) |
| `IncludedComponentSettingsValues` | String[] | No | Optional settings; pass `null` for default behaviour |

### Common Patterns

**Add an entity with all subcomponents (recommended):**

```json
{
  "ComponentId": "{entity-metadata-id}",
  "ComponentType": 1,
  "SolutionUniqueName": "GrantsManagementCore",
  "AddRequiredComponents": true,
  "DoNotIncludeSubcomponents": false,
  "IncludedComponentSettingsValues": null
}
```

**Add entity as shell only (no attributes, forms, views):**

```json
{
  "ComponentId": "{entity-metadata-id}",
  "ComponentType": 1,
  "SolutionUniqueName": "GrantsManagementCore",
  "AddRequiredComponents": false,
  "DoNotIncludeSubcomponents": true,
  "IncludedComponentSettingsValues": null
}
```

**Add a single attribute:**

```json
{
  "ComponentId": "{attribute-metadata-id}",
  "ComponentType": 2,
  "SolutionUniqueName": "GrantsManagementCore",
  "AddRequiredComponents": false,
  "DoNotIncludeSubcomponents": false,
  "IncludedComponentSettingsValues": null
}
```

**Add a web resource:**

```json
{
  "ComponentId": "{webresourceid}",
  "ComponentType": 61,
  "SolutionUniqueName": "GrantsManagementCore",
  "AddRequiredComponents": false,
  "DoNotIncludeSubcomponents": false,
  "IncludedComponentSettingsValues": null
}
```

**Add a plugin assembly with all steps:**

```json
{
  "ComponentId": "{pluginassemblyid}",
  "ComponentType": 91,
  "SolutionUniqueName": "GrantsManagementCore",
  "AddRequiredComponents": true,
  "DoNotIncludeSubcomponents": false,
  "IncludedComponentSettingsValues": null
}
```

**Add a security role:**

```json
{
  "ComponentId": "{roleid}",
  "ComponentType": 20,
  "SolutionUniqueName": "GrantsManagementCore",
  "AddRequiredComponents": false,
  "DoNotIncludeSubcomponents": false,
  "IncludedComponentSettingsValues": null
}
```

**Add a canvas app:**

```json
{
  "ComponentId": "{canvasappid}",
  "ComponentType": 300,
  "SolutionUniqueName": "GrantsManagementCore",
  "AddRequiredComponents": true,
  "DoNotIncludeSubcomponents": false,
  "IncludedComponentSettingsValues": null
}
```

**Add an environment variable definition:**

```json
{
  "ComponentId": "{environmentvariabledefinitionid}",
  "ComponentType": 380,
  "SolutionUniqueName": "GrantsManagementCore",
  "AddRequiredComponents": true,
  "DoNotIncludeSubcomponents": false,
  "IncludedComponentSettingsValues": null
}
```

### Response

`AddSolutionComponentResponse` — contains the `id` of the created `solutioncomponent` record.

---

## RemoveSolutionComponent

**POST** `/api/data/v9.2/RemoveSolutionComponent`

Removes a component from an **unmanaged** solution. Requires the `solutioncomponentid` — the ID of the join record, not the component itself.

### Step 1: Resolve the solutioncomponentid

```
GET /api/data/v9.2/solutioncomponents?$filter=_solutionid_value eq {solutionId} and objectid eq {componentId} and componenttype eq {componentTypeCode}&$select=solutioncomponentid
```

### Step 2: Call RemoveSolutionComponent

```json
{
  "SolutionComponent": {
    "@odata.type": "Microsoft.Dynamics.CRM.solutioncomponent",
    "solutioncomponentid": "{solutioncomponentid}"
  },
  "ComponentType": 1,
  "SolutionUniqueName": "GrantsManagementCore"
}
```

> Removing a component from a solution does **not** delete the component from the environment — it only removes it from this solution layer.

---

## UpdateSolutionComponent

**POST** `/api/data/v9.2/UpdateSolutionComponent`

Updates the include behaviour of an existing component in a solution (e.g., switch from shell-only to include-subcomponents).

```json
{
  "ComponentId": "{componentId}",
  "ComponentType": 1,
  "SolutionUniqueName": "GrantsManagementCore",
  "DoNotIncludeSubcomponents": false,
  "IncludedComponentSettingsValues": null
}
```

---

## IsComponentCustomizable

Check whether a component can be customized (useful before attempting a write operation):

**POST** `/api/data/v9.2/IsComponentCustomizable`

```json
{
  "ComponentId": "{componentId}",
  "ComponentType": 1
}
```

**Response:** Returns `IsCustomizable` (boolean) and `IsReadOnly` (boolean).

---

## Batch Add Pattern

When adding multiple components to the same solution, use OData `$batch` to reduce round trips:

```http
POST /api/data/v9.2/$batch
Content-Type: multipart/mixed; boundary=batch_boundary

--batch_boundary
Content-Type: application/http
Content-Transfer-Encoding: binary

POST /api/data/v9.2/AddSolutionComponent HTTP/1.1
Content-Type: application/json

{ "ComponentId": "{id1}", "ComponentType": 1, "SolutionUniqueName": "GrantsManagementCore", "AddRequiredComponents": true, "DoNotIncludeSubcomponents": false, "IncludedComponentSettingsValues": null }

--batch_boundary
Content-Type: application/http
Content-Transfer-Encoding: binary

POST /api/data/v9.2/AddSolutionComponent HTTP/1.1
Content-Type: application/json

{ "ComponentId": "{id2}", "ComponentType": 61, "SolutionUniqueName": "GrantsManagementCore", "AddRequiredComponents": false, "DoNotIncludeSubcomponents": false, "IncludedComponentSettingsValues": null }

--batch_boundary--
```
