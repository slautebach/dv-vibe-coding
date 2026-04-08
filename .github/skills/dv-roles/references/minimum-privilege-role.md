# App Opener — Minimum Privilege Role

> Source: https://learn.microsoft.com/en-us/power-platform/admin/create-edit-security-role#minimum-privileges-for-common-tasks

## What It Is

The **App Opener** is a predefined Dataverse security role that contains the minimum set of privileges a user needs to open and run a model-driven app. It is the mandatory starting point for every custom security role.

## How to Use It

1. In Power Platform Admin Center, go to **Settings > Users + permissions > Security roles**.
2. Select **App Opener**, then choose **Copy security role**.
3. Name the copy using the MNP convention: `{Solution} - {Role}`.
4. Add only the table privileges required for the persona.

> Never assign App Opener directly to end users — it is a template to copy from.

## What App Opener Includes

App Opener grants the minimum system privileges required to:

- Sign in to Dataverse and load model-driven apps
- Read navigation, saved views, and user settings
- Execute system-supplied flows (organization-level Read on process table)

## Predefined Roles Reference

| Role | Use for |
|---|---|
| **App Opener** | Copy as base for all new custom roles; minimum to run a model-driven app |
| **Basic User** | Includes App Opener privileges + access to core business tables |
| **System Administrator** | Full access; never copy this as a starting point for custom roles |
| **System Customizer** | Customization access; do not assign to end users |

## Recommended Workflow

```
App Opener (copy)
  └─ {Solution} - Basic Role        ← add table Read for main entities
       └─ {Solution} - Approver Role ← add Append/Write for approval tables
            └─ {Solution} - Admin    ← add Create/Delete, system config
```

## Member's Privilege Inheritance

When assigning a role to a team, set **Member's privilege inheritance**:

| Setting | Behaviour |
|---|---|
| **Direct User (Basic) access level and Team privileges** *(default)* | Role behaves as if assigned directly to the user; user can own records |
| **Team privileges only** | User inherits privileges only via team membership; team owns records |

Use **Direct User** for standard personas. Use **Team privileges only** when records must be owned by the team (e.g., shared queues).
