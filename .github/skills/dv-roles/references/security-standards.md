# MNP Security Standards

> Extracted from `wiki/Welcome/Platform-Delivery-Playbook/Implementation-Standards/Security-Standards.md`

## Guiding Principle

Apply **minimum privilege** — grant only the access a user needs to complete their role. Start from the App Opener base role and add permissions additively.

## Security Role Design

### Naming Convention

Format: `{Solution} - {Role}`

| Placeholder | Meaning | Examples |
|---|---|---|
| `{Solution}` | Solution name or acronym | `QUARTS`, `ROCS`, `OHAS`, `PATH` |
| `{Role}` | Role within the solution | `Basic User`, `Admin`, `Approver`, `Financial` |

**Examples:** `QUARTS - Basic User`, `QUARTS - Admin`, `ROCS - Approver`

### Role Composition (Additive)

Create small, focused roles and combine them per persona. Do **not** create one large monolithic role per user type.

| Layer | Example | Purpose |
|---|---|---|
| Base | `{Solution} - Basic Role` | Minimum access to run the app |
| Functional | `{Solution} - Approver Role` | Approval workflow privileges |
| Elevated | `{Solution} - Financial Role` | Financial data access |

A user needing financial access gets: `{Solution} - Basic Role` + `{Solution} - Financial Role`.

### Starting Point

Always begin with the **App Opener** predefined role (available in all Dataverse environments). Copy it, rename it following the convention above, then add only the privileges required.

> Do **not** use the deprecated `min prv apps use` download. Use the built-in **App Opener** role.

## Team Design

### Naming Convention

Format: `{Solution} - {Team}`

| Placeholder | Meaning |
|---|---|
| `{Solution}` | Solution name or acronym |
| `{Team}` | Team function within the solution |

### Standard Teams

| Team name pattern | Purpose |
|---|---|
| `{Solution} - Admin` | Solution administrators |
| `{Solution} - Dev Team` | Developers during delivery |
| `{Solution} - Users - Standard` | Regular end users |
| `{Solution} - Users - Admin` | Power users / business admins |

### Security Group Matrix

Create a **Security Group Matrix** worksheet mapping each security role to table CRUD permissions.

Create a **Security Team Matrix** assigning teams to their security roles.
