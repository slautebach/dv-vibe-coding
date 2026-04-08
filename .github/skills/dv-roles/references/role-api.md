# Dataverse Web API — Security Role & Team Endpoints

All endpoints are relative to `{env_url}/api/data/v9.2/`.

All role operations use `.github/scripts/dataverse_client.py` — no pac CLI.

---

## Roles

### List Roles

```
GET /api/data/v9.2/roles?$select=roleid,name,businessunitid&$filter=_businessunitid_value eq {businessUnitId}
```

Get the root business unit ID first:

```
GET /api/data/v9.2/businessunits?$filter=parentbusinessunitid eq null&$select=businessunitid,name
```

### Create Role

```python
payload = {
    "name": "GrantsManagement - Basic User",
    "businessunitid@odata.bind": f"/businessunits({business_unit_id})"
}
response = client.post("roles", payload)
role_id = response.headers.get("OData-EntityId").split("(")[1].rstrip(")")
```

### Assign Privilege to Role

Privileges are assigned via the `roleprivileges_association` collection:

```python
# Get privilege ID first
priv = client.get(
    "privileges",
    filter="name eq 'prvReadContact'",
    select="privilegeid,name"
)
privilege_id = priv['value'][0]['privilegeid']

# Assign to role
client.post(
    f"roles({role_id})/roleprivileges_association/$ref",
    {"@odata.id": f"{client.base_url}/privileges({privilege_id})"}
)
```

> **Note:** The Web API does not expose a single-call endpoint to set privilege depth (User/BU/Org). Use the `AddPrivilegesRole` action for full control:

```python
client.post("AddPrivilegesRole", {
    "RoleId": role_id,
    "Privileges": [
        {
            "Depth": "Basic",        # Basic | Local | Deep | Global
            "PrivilegeId": privilege_id,
            "BusinessUnitId": business_unit_id
        }
    ]
})
```

**Depth values:**

| Value | Access Level | MNP Label |
|---|---|---|
| `Basic` | User-owned records | U |
| `Local` | Business Unit | BU |
| `Deep` | BU + child BUs | P |
| `Global` | Organisation-wide | O |

### Copy Role (Start from App Opener)

```python
# Get App Opener role ID
app_opener = client.get(
    "roles",
    filter="name eq 'App Opener'",
    select="roleid"
)
app_opener_id = app_opener['value'][0]['roleid']

# Clone it
client.post("CloneAsSolution", {  # Not available — must manually copy privileges
})
```

> **Important:** The Web API does not have a native "copy role" action. To clone App Opener:
> 1. Create the new role (POST `/roles`)
> 2. Fetch all privileges from App Opener: `GET /roleprivileges_association?$select=privilegeid,depth`
> 3. Apply each to the new role via `AddPrivilegesRole`

---

## Teams

### Create Team

```python
client.post("teams", {
    "name": "GrantsManagement - Admin",
    "teamtype": 0,    # 0 = Owner, 1 = Access
    "businessunitid@odata.bind": f"/businessunits({business_unit_id})"
})
```

**teamtype values:** `0` = Owner team, `1` = Access team

### Assign Role to Team

```python
client.post(
    f"teams({team_id})/teamroles_association/$ref",
    {"@odata.id": f"{client.base_url}/roles({role_id})"}
)
```

---

## Solution XML Stubs

Security roles can also be defined directly in unpacked solution XML for source-controlled deployments:

```xml
<!-- {SolutionRoot}/Roles/{roleName}/RolePrivileges.xml -->
<Role Name="GrantsManagement - Basic User" isinherited="1">
  <RolePrivileges>
    <RolePrivilege name="prvReadContact" level="Basic"/>
    <RolePrivilege name="prvReadAccount" level="Basic"/>
    <RolePrivilege name="prvReadmnp_application" level="Basic"/>
    <RolePrivilege name="prvWritemnp_application" level="Basic"/>
    <RolePrivilege name="prvCreatemnp_application" level="Basic"/>
  </RolePrivileges>
</Role>
```

**level values in XML:** `None` | `Basic` | `Local` | `Deep` | `Global`

Add the role to the solution using `AddSolutionComponent` (ComponentType = 20) after importing — see `dv-solution` skill.

---

## Staging Pattern

Write proposed definitions to `.staging/roles-authoring/` before applying:

```
.staging/roles-authoring/
  {Solution}-security-matrix.md       # Human-readable privilege matrix
  {Solution}-teams.md                 # Team structure
  {Solution}-roles.json               # Structured role definitions for API scripting
```

Present the security matrix to the user for confirmation before calling any write endpoints.
