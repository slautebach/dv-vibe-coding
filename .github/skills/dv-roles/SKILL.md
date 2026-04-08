---
name: dv-roles
description: Design and manage Dataverse security roles and teams following MNP minimum-privilege standards. Generates security role definitions, privilege matrices, and team structures. Use when asked to "create a security role", "design roles", "generate a security matrix", "create teams", "set up role permissions", or "design the security model". Do NOT use for documenting existing roles from live Dataverse (use dv-doc-roles skill).
---

# Dataverse Role Designer

Design Dataverse security roles and teams following the MNP minimum-privilege approach. This skill **creates and designs** roles — for documenting existing roles from live Dataverse, use `dv-doc-roles`.

## Reference Files

Read these before designing anything:

- **`references/security-standards.md`** — MNP naming conventions and composition rules (always read)
- **`references/minimum-privilege-role.md`** — App Opener base role and Member Privilege Inheritance (read when creating roles)
- **`references/privilege-depth-levels.md`** — Access level definitions and MNP depth guidance (read when assigning privileges)
- **`references/role-api.md`** — Web API endpoints and solution XML structure for role creation/staging (read when generating output)

## Core Design Principles

1. **Start from App Opener** — every custom role is a copy of App Opener plus additive privileges
2. **Additive layering** — small focused roles combined per persona (Basic + Approver, not one fat role)
3. **Minimum depth** — default to User (Basic); escalate to BU/Org only when the workflow requires it
4. **Naming**: `{Solution} - {Role}` for roles, `{Solution} - {Team}` for teams

## Workflow

### Step 1 — Gather Context

Ask (or infer from context):
- Solution name / acronym (e.g., `QUARTS`)
- Key personas (e.g., Applicant, Reviewer, Admin)
- Main tables the solution uses
- Any special access requirements (cross-BU reads, approval flows, financial data)

### Step 2 — Design Role Layers

Map each persona to an additive role stack:

| Persona | Role stack |
|---|---|
| Standard user | Basic Role |
| Approver | Basic Role + Approver Role |
| Admin | Basic Role + Admin Role |

### Step 3 — Build the Security Matrix

Use `assets/security-matrix-template.md` as the starting template.

For each role layer, define privileges per table:
- Columns: Entity | Create | Read | Write | Delete | Append | Append To | Assign | Share
- Values: `O` (Org) | `P` (Parent:Child BU) | `BU` (Business Unit) | `U` (User/Basic) | `-` (None)

Check `references/privilege-depth-levels.md` for MNP guidance on appropriate depth per persona type.

### Step 4 — Design Teams

Map teams to role stacks following the standard team patterns in `references/security-standards.md`.

Common teams: `{Solution} - Admin`, `{Solution} - Dev Team`, `{Solution} - Users - Standard`, `{Solution} - Users - Admin`.

### Step 5 — Stage Output

Write proposed definitions to `src/dataverse/roles-authoring/` before any live apply:

```
src/dataverse/roles-authoring/
  {Solution}-roles.md           # Security matrix (human-readable)
  {Solution}-teams.md           # Team matrix (human-readable)
  {Solution}-roles.json         # Structured role definitions for scripting
```

### Step 6 — Generate Deliverables

Produce one or more of:

**A) Markdown security matrix** — ready to paste into wiki or share with stakeholders

**B) Solution XML stubs** — role XML files for inclusion in an unpacked Dataverse solution:
```xml
<Role Name="{Solution} - Basic User" isinherited="1">
  <RolePrivileges>
    <RolePrivilege name="prvReadContact" level="Basic"/>
  </RolePrivileges>
</Role>
```

**C) Web API commands** — POST bodies for programmatic role creation (see `references/role-api.md`)

## Dataverse Skills Integration (Live Apply)

To check existing roles before designing:

```bash
copilot plugin marketplace add microsoft/Dataverse-skills
copilot plugin install dataverse@dataverse-skills
```

Load `dv-overview`, then use `dv-connect` to select the target environment and confirm auth context. Set `CLIENT_ID` + `CLIENT_SECRET` in `.env` for service principal auth.

Then reuse the existing fetch script to read current state:

```bash
python .github/skills/dv-doc-roles/scripts/fetch-role-from-dataverse.py \
  --environment dev --all
```

To apply staged roles, use `.github/scripts/dataverse_client.py` — it inherits the auth context established by `dv-connect`:

```python
from dataverse_client import DataverseClient

client = DataverseClient()   # inherits auth context from dv-connect
```

Always **read before write** — fetch current roles, compare with proposed, apply only the delta.

## Example Requests

- "Design security roles for a Grants solution with Admin, Reviewer, and Applicant personas"
- "Create a security matrix for the QUARTS solution covering Case, Contact, and Account tables"
- "Generate the team definitions for a Benefits solution following MNP naming standards"