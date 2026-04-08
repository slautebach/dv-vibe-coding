# Dataverse Privilege Access Levels (Depth)

> Source: https://learn.microsoft.com/en-us/power-platform/admin/security-roles-privileges

Each privilege on a table has an **access level** (depth) that defines the scope of records it applies to within the business unit hierarchy.

## Access Level Reference

| Level | Mask value | Description | When to use |
|---|---|---|---|
| **Organization** | 8 | User can access **all records** in the environment regardless of business unit | System admins, org-wide reporting roles, configuration tables |
| **Parent: Child Business Unit** | 4 | User can access records in their BU **and all subordinate BUs** | Regional managers, supervisors overseeing sub-units |
| **Business Unit** | 2 | User can access records owned by **their own business unit** | Managers within a single department |
| **User (Basic)** | 1 | User can access records they **own** or that are shared with them or their team | Standard end users, front-line workers |
| **None** | 0 | No access | Explicitly removing a privilege inherited from another role |

> **Accumulative model:** Privileges are additive across all assigned roles. The highest access level granted by any role wins. You cannot restrict access granted by another role — assign roles carefully.

## Privilege Types on a Table

| Privilege | Description |
|---|---|
| **Create** | Make a new record |
| **Read** | Open and view a record |
| **Write** | Modify an existing record |
| **Delete** | Permanently remove a record |
| **Append** | Attach another record to this one (e.g., note on a case) |
| **Append To** | Allow another record to be attached to this one |
| **Assign** | Transfer ownership to another user or team |
| **Share** | Grant another user access while retaining your own |

## Privilege Depth Masks

The `privilegedepthmask` field in Dataverse stores the access level as a bitmask:

| Depth | Numeric value |
|---|---|
| None | 0 |
| User (Basic) | 1 |
| Business Unit | 2 |
| Parent: Child BU | 4 |
| Organization | 8 |

## MNP Guidance

| Persona type | Recommended Read depth | Recommended Write depth |
|---|---|---|
| Standard user | User (1) on own data; BU (2) on shared lookup tables | User (1) |
| Approver | BU (2) or Org (8) for read (needs to see others' submissions) | User (1) on their own approvals |
| Admin | Organization (8) | Organization (8) — restrict carefully |
| Dev Team | Organization (8) read | User (1) write in non-prod only |

> Prefer **User (Basic)** depth as default. Escalate to BU or Org only when the business workflow requires it.
