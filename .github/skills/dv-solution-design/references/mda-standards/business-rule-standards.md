# MDA Standards: Business Rules

## WHY?

- Protect form data from inappropriate changes
- Enforce business rules on form data
- Consistent naming increases clarity and speed when locating rules

## Standard Business Rules to Create

| Rule | Scope | Purpose |
|---|---|---|
| `{Table} - Lock Fields` | Form | Lock fields that should always be read-only |
| `{Table} - Lock After Create` | Form | Lock fields after the record is created to protect data integrity |
| `{Table} - Default` | Form | Default values when a new form record is created |

> Always set scope to **Form** for lock rules -- Entity-scoped rules execute like workflow processes.

## Naming Convention

`{Table} - {Action} - {Target}`

Examples:
- `Registration - Lock Fields`
- `Registration - Lock After Create`
- `Registration - Show Hide - Contact`

## Scope Guidelines

| Rule Type | Scope |
|---|---|
| Show/Hide rules | All Forms, or the specific Information form |
| Lock/Default rules | Specific form (to avoid restricting Workflows/Actions) |
| Entity-scoped | Only when process-level enforcement (like a background workflow) is needed |

## Important Note on Field Locking

**DO NOT lock fields directly on the form.** Always lock via Business Rules:
- Allows Workflows/Actions to still update the field
- Allows admins to temporarily unlock by deactivating the rule (no form republish needed)
