# Dataverse Web API — Publisher Endpoints

All endpoints are relative to `{env_url}/api/data/v9.2/`.

Publishers own solutions and define the customization prefix applied to all custom components.

---

## List Publishers

**GET** `/api/data/v9.2/publishers`

```
GET /api/data/v9.2/publishers?$select=publisherid,uniquename,friendlyname,customizationprefix,customizationoptionvalueprefix&$filter=isreadonly eq false
```

Filter to a specific prefix:

```
GET /api/data/v9.2/publishers?$filter=customizationprefix eq 'mnp'&$select=publisherid,uniquename,friendlyname,customizationprefix
```

**Key fields:**

| Field | Description |
|---|---|
| `publisherid` | Unique identifier (GUID) — used in solution creation |
| `uniquename` | Machine-readable unique name (no spaces) |
| `friendlyname` | Display name |
| `customizationprefix` | 2–8 character prefix applied to all custom components (e.g., `mnp`) |
| `customizationoptionvalueprefix` | Integer prefix for option set values (10000–99999) |
| `isreadonly` | `true` = system publisher (cannot modify) |

---

## Create Publisher

**POST** `/api/data/v9.2/publishers`

```json
{
  "uniquename": "mnpdigital",
  "friendlyname": "MNP Digital",
  "description": "MNP Digital publisher for Dynamics 365 / Power Platform solutions.",
  "customizationprefix": "mnp",
  "customizationoptionvalueprefix": 12345,
  "address1_addresstypecode": 1,
  "address1_city": "Toronto"
}
```

**Rules:**
- `customizationprefix` must be 2–8 lowercase alphanumeric characters, must start with a letter, and must be unique across publishers in the environment
- `customizationoptionvalueprefix` must be a unique integer between 10000 and 99999 — use a project-specific number to avoid collisions with other publishers in multi-publisher environments
- `uniquename` must be alphanumeric with no spaces

**Response:** `204 No Content` with `OData-EntityId` header containing the new publisher URL.

---

## Update Publisher

**PATCH** `/api/data/v9.2/publishers({publisherid})`

```json
{
  "friendlyname": "MNP Digital (Updated)",
  "description": "Updated publisher description."
}
```

> **Note:** The `customizationprefix` cannot be changed after any component has been created using it.

---

## Get the Default Publisher

The default publisher is created automatically for each environment. Avoid using the default publisher for project solutions — always create a dedicated publisher.

```
GET /api/data/v9.2/publishers?$filter=uniquename eq 'default'&$select=publisherid,customizationprefix
```

---

## Publisher in Solution Creation

When creating a solution, bind the publisher using the `@odata.bind` pattern:

```json
{
  "uniquename": "GrantsManagementCore",
  "friendlyname": "Grants Management Core",
  "version": "1.0.0.0",
  "publisherid@odata.bind": "/publishers({publisherId})"
}
```

Retrieve the `publisherId` GUID from the publisher list query above.
