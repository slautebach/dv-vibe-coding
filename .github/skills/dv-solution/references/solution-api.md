# Dataverse Web API — Solution Endpoints

All endpoints are relative to `{env_url}/api/data/v9.2/`.

Source: [Microsoft Learn — Web API reference: solution](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/reference/solution)

---

## List Solutions

**GET** `/api/data/v9.2/solutions`

```
GET /api/data/v9.2/solutions?$select=solutionid,uniquename,friendlyname,version,ismanaged,_publisherid_value
```

Filter to unmanaged solutions only (the ones you can modify):

```
GET /api/data/v9.2/solutions?$filter=ismanaged eq false&$select=solutionid,uniquename,friendlyname,version
```

Get a specific solution by unique name:

```
GET /api/data/v9.2/solutions?$filter=uniquename eq 'GrantsManagementCore'&$select=solutionid,uniquename,friendlyname,version,ismanaged,_publisherid_value
```

**Response fields:**

| Field | Description |
|---|---|
| `solutionid` | Unique identifier (GUID) of the solution |
| `uniquename` | Machine-readable unique name (used in all API calls) |
| `friendlyname` | Display name shown in the maker portal |
| `version` | Version string in `major.minor.build.revision` format |
| `ismanaged` | `true` = managed (read-only); `false` = unmanaged |
| `_publisherid_value` | GUID of the associated publisher |

---

## Create Solution

**POST** `/api/data/v9.2/solutions`

```json
{
  "uniquename": "GrantsManagementCore",
  "friendlyname": "Grants Management Core",
  "description": "Core solution for the Grants Management engagement. Contains all custom tables, attributes, and business logic.",
  "version": "1.0.0.0",
  "publisherid@odata.bind": "/publishers({publisherId})"
}
```

**Rules:**
- `uniquename` must be alphanumeric with no spaces or special characters
- `version` must follow `major.minor.build.revision` (e.g., `1.0.0.0`)
- The publisher must exist before creating the solution — use `publisherid@odata.bind` to link it
- Only **unmanaged** solutions can be created via API — managed solutions are produced during export

**Response:** `204 No Content` with `OData-EntityId` header containing the new solution URL.

---

## Update Solution

**PATCH** `/api/data/v9.2/solutions({solutionid})`

Only provide the fields to change:

```json
{
  "version": "1.1.0.0",
  "friendlyname": "Grants Management Core (Updated)",
  "description": "Updated description."
}
```

---

## Delete Solution

**DELETE** `/api/data/v9.2/solutions({solutionid})`

> **Warning:** Deleting an unmanaged solution removes its customizations from the environment if no other solution layer covers them. Always confirm with the user before deleting.

---

## Clone as Patch

Creates a child patch solution from an existing base solution. Used for hotfixes.

**POST** `/api/data/v9.2/CloneAsPatch`

```json
{
  "DisplayName": "Grants Management Core - Patch 1",
  "VersionNumber": "1.0.1.0",
  "SolutionUniqueName": "GrantsManagementCore"
}
```

> Patches can only contain components already present in the base solution.
> After creation, target the patch's unique name in all `AddSolutionComponent` calls.

**Response:** Returns the `solutionid` of the new patch solution.

---

## Clone as Solution

Creates a full copy of a solution as a new independent solution.

**POST** `/api/data/v9.2/CloneAsSolution`

```json
{
  "DisplayName": "Grants Management Core v2",
  "VersionNumber": "2.0.0.0",
  "SolutionUniqueName": "GrantsManagementCore"
}
```

---

## Delete and Promote (Merge Patch)

Merges a patch solution back into its base solution and deletes the patch.

**POST** `/api/data/v9.2/DeleteAndPromote`

```json
{
  "UniqueName": "GrantsManagementCoreHotfix1"
}
```

---

## Query Solution Components

List all components in a solution (by solution ID):

```
GET /api/data/v9.2/solutioncomponents?$filter=_solutionid_value eq {solutionId}&$select=componenttype,objectid,rootcomponentbehavior&$orderby=componenttype asc
```

> `objectid` is the GUID of the underlying component (entity MetadataId, web resource id, etc.).
> Use the component type code to determine which entity set to query for the display name.

**rootcomponentbehavior values:**

| Value | Meaning |
|---|---|
| `0` | Include Subcomponents |
| `1` | Do not include subcomponents |
| `2` | Include As Shell Only |
