# Table Permissions Standards

Wiki source: `wiki/Welcome/Platform-Delivery-Playbook/Implementation-Standards/Using-PowerPages/Table-Permissions-Standards.md`

> **Note:** This standards page is currently a stub in the wiki. Guidance below is synthesized from MNP Power Pages conventions and Microsoft Power Pages documentation.

## WHY?
Table Permissions control what portal users can read, write, create, and delete for each Dataverse table. Without table permissions, portal users cannot access any records — all queries return empty results.

## Scope Types

| Scope | When to Use |
|---|---|
| **Global** | All records in the table (e.g., read-only reference data) |
| **Contact** | Records where a field references the authenticated Contact (e.g., `regardingcontactid = user.id`) |
| **Account** | Records belonging to the user's Account (e.g., for B2B portals) |
| **Self** | The Contact record representing the authenticated user |
| **Parental** | Records related to a parent record for which the user already has permission (for child tables) |

## Privilege Types

| Privilege | Description |
|---|---|
| **Read** | View record data |
| **Write** | Update existing records |
| **Create** | Create new records |
| **Delete** | Delete records |
| **Append** | Associate this record to another |
| **Append To** | Allow other records to be associated to this record |

## Web Roles

- Assign Table Permissions to **Web Roles** (not directly to users)
- Common web roles:
  - **Authenticated Users** — all logged-in portal users
  - **Anonymous Users** — unauthenticated users (use with caution; read-only reference data only)
  - **{Solution} Applicant** — solution-specific role for program applicants

## Design Pattern: Typical Submission Portal

```
Web Role: QUARTS Applicant
  Table Permission: mnp_application
    Scope: Contact (regardingcontactid = user.id)
    Privileges: Read, Write, Create

  Table Permission: mnp_application_document (child)
    Scope: Parental (parent = mnp_application)
    Privileges: Read, Write, Create, Delete

  Table Permission: mnp_program (reference data)
    Scope: Global
    Privileges: Read
```

## Naming Convention

`{Solution} - {Table} - {Scope} - {Description}`

**Examples:**
- `QUARTS - Application - Contact - Applicant Access`
- `QUARTS - Program - Global - Read Reference Data`

## Important Notes

- Table Permissions are **additive** — a user with multiple web roles gets the union of all permissions
- For **anonymous flows**, use Global scope with Read-only permissions; never grant Write/Create globally
- Entity Lists and Sub-Grids will return empty results if the appropriate Table Permission is not configured for the web role

## References
- [Table permissions in Power Pages](https://learn.microsoft.com/en-us/power-pages/security/table-permissions)
- [Web roles overview](https://learn.microsoft.com/en-us/power-pages/security/create-web-roles)

## Related
- [Entity List and Sub-Grid Standards](entity-list-subgrid-standards.md)
- [Basic Form Standards](basic-form-standards.md)
- [Pattern - Portal Authentication](../patterns/portal-authentication.md)
