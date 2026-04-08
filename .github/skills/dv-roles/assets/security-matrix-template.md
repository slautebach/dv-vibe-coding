# Security Matrix Template

Copy this template and fill in one row per entity. Use `X` for assigned privileges, or replace with the depth level: `U` (User/Basic), `BU` (Business Unit), `P` (Parent:Child BU), `O` (Organization).

## {Solution} — Security Role Matrix

**Legend:** `O` = Organization | `P` = Parent:Child BU | `BU` = Business Unit | `U` = User/Basic | `-` = None

### {Solution} - Basic Role

| Entity | Create | Read | Write | Delete | Append | Append To | Assign | Share | Notes |
|---|---|---|---|---|---|---|---|---|---|
| Contact | - | U | - | - | U | U | - | - | Read own contacts |
| Account | - | BU | - | - | - | - | - | - | Read all accounts in BU |
| {Custom Entity} | U | U | U | - | U | U | - | - | Own records CRUD |
| Task | U | U | U | U | - | - | - | - | Own tasks full access |
| Email | U | U | U | - | U | U | - | - | |
| Note | U | U | U | U | U | U | - | - | |

### {Solution} - Approver Role

*Additive to Basic Role — assign both roles to approvers*

| Entity | Create | Read | Write | Delete | Append | Append To | Assign | Share | Notes |
|---|---|---|---|---|---|---|---|---|---|
| {Custom Entity} | - | BU | U | - | - | - | - | - | Read all submissions in BU |
| {Approval Entity} | U | BU | U | - | U | U | U | - | Create/update approvals |

### {Solution} - Admin Role

*Additive to Basic Role — assign both roles to admins*

| Entity | Create | Read | Write | Delete | Append | Append To | Assign | Share | Notes |
|---|---|---|---|---|---|---|---|---|---|
| Contact | O | O | O | O | O | O | O | O | Full org access |
| Account | O | O | O | O | O | O | O | O | Full org access |
| {Custom Entity} | O | O | O | O | O | O | O | O | Full org access |
| System Job | - | O | - | O | - | - | - | - | Monitor/cancel jobs |

---

## {Solution} — Team Matrix

| Team | Roles Assigned | Notes |
|---|---|---|
| `{Solution} - Admin` | `{Solution} - Basic Role` + `{Solution} - Admin Role` | Solution administrators |
| `{Solution} - Dev Team` | `{Solution} - Basic Role` + `{Solution} - Admin Role` | Development team (non-prod only) |
| `{Solution} - Users - Standard` | `{Solution} - Basic Role` | Standard end users |
| `{Solution} - Users - Admin` | `{Solution} - Basic Role` + `{Solution} - Approver Role` | Power users / business admins |

---

## Common Entities Quick Reference

| Entity logical name | Display name | Typical depth |
|---|---|---|
| `contact` | Contact | BU Read, U Write |
| `account` | Account | BU Read |
| `task` | Task | U full CRUD |
| `email` | Email | U Read/Write |
| `annotation` | Note | U full CRUD |
| `systemuser` | User | BU Read (for lookups) |
| `team` | Team | BU Read (for lookups) |
| `businessunit` | Business Unit | O Read (for lookups) |
| `workflow` | Process (Flow) | O Read (to run flows) |
