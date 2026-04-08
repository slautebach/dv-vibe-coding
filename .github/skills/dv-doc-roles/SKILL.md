---
name: dv-doc-roles
description: Analyze Dynamics 365 Dataverse security role components from live Dataverse and generate structured role documentation. Use when reviewing role privileges, comparing role definitions, auditing access levels, or creating security role documentation.
---

# Dataverse Analyze Roles

Analyze Dataverse security roles retrieved directly from live Dataverse and generate role-by-role documentation focused on privileges, access levels, and risk-sensitive permissions.

## Dataverse Skills Dependency

This skill depends on the Dataverse-skills plugin for any live Dataverse access.

Install it with:

```bash
copilot plugin marketplace add microsoft/Dataverse-skills
copilot plugin install dataverse@dataverse-skills
```

- Load `dv-overview` first.
- Use `dv-connect` to confirm the target environment before fetching roles.

## Output Structure

**Dataverse JSON** (committed to source control):
```
src/dataverse/roles/<RoleName>/
  <RoleName>.role.json      # Merged role metadata + privileges
  <RoleName>.dataverse.json # Raw Dataverse records for traceability
```

**Wiki** (committed — final output after AI merge):
```text
wiki/Technical-Reference/roles/
  <RoleName>.md                   ← index page (was README.md)
  <RoleName>/
    metadata.json
```

> `src/dataverse/` is committed to source control as the canonical JSON snapshot extracted from the live environment. This gives a diff-friendly audit trail of environment changes and allows wiki generation to run from local files without re-fetching from Dataverse.

## Workflow

### Step 1: Fetch Role from Dataverse

1. Load `dv-overview` and confirm the environment with `dv-connect`.
2. Run the fetch script to retrieve the latest role definition and privileges:

```bash
python .github/skills/dv-doc-roles/scripts/fetch-role-from-dataverse.py \
  --environment dev \
  --name "SIS Worker"
```

Or by GUID or all roles:

```bash
python .github/skills/dv-doc-roles/scripts/fetch-role-from-dataverse.py \
  --environment dev \
  --role-id 5f3a1e2d-4b6c-4e8a-9d0e-1f2a3b4c5d6e

python .github/skills/dv-doc-roles/scripts/fetch-role-from-dataverse.py \
  --environment dev \
  --all
```

The script writes to `src/dataverse/roles/<RoleName>/`:

- `<RoleName>.role.json` — `{"role": {...metadata...}, "privileges": [{name, accessright, privilegedepthmask}, ...]}`
- `<RoleName>.dataverse.json` — raw Dataverse records for traceability

### Step 2: AI Merge — Apply Staged Output to Wiki Pages

After the script completes, the AI merges staged output into `wiki/Technical-Reference/roles/<RoleName>.md` (index page) and `wiki/Technical-Reference/roles/<RoleName>/` (metadata).

---

#### 2a. Gather domain context (do this before writing any files)

Search the following locations for references to this role's name, the persona it serves, or the business domains it covers:

1. `wiki/Detailed-Application-Design/Security-and-Auditing.md` — primary source for role intent, persona mapping, and access design decisions
2. `wiki/Detailed-Application-Design/*.md` — other domain overviews that reference this role by name
3. `wiki/Detailed-Application-Design/**/*.md` — sub-pages that describe role-restricted features or workflows
4. `wiki/Technical-Reference/app-modules/` — app module pages to understand which apps this role's persona uses

Collect: the job function or persona this role supports, which business domains it grants access to, and any documented access-design decisions or restrictions.

---

#### 2b. Write/update `<RoleName>.md` (index page)

**Auto-generated sections** (replace entirely from `src/dataverse/roles/<RoleName>/<RoleName>.role.json`):
- `## Overview` table — role metadata: `roleid`, `name`, `description`, `modifiedon`, `ismanaged`
- `## Privilege Summary` — privilege distribution table grouped by action (Read/Create/Write/Delete/etc.) and access level (Global/Deep/Local/Basic)
- `## Elevated Permissions` — list of high-impact privileges (system-level admin or broad Global write/delete on custom tables)

**AI-written section** (generate fresh on first run; update only if facts changed on re-runs):

Write or update `## Business Analysis` immediately after `## Elevated Permissions`:

```markdown
## Business Analysis

### Purpose
{1-3 sentences. Which job function or persona is this role designed for in the Income Assistance
system? What level of access does it grant at a high level — administrative, case worker,
read-only reviewer, etc.?}

### Domain Context
{Which business domains or modules this role grants access to. Reference specific wiki pages.
Example: "Grants working access to the [Case Management](/wiki/Detailed-Application-Design/Case-Management)
and [Benefit Assessment](/wiki/Detailed-Application-Design/Benefit-Calculation) domains."}

### Access Summary
{High-level description of what this role can do — create/edit records, approve transactions,
run reports, configure the system, etc. Distinguish between full CRUD vs read-only vs approve-only
patterns observed in the privilege set.}

### Notable Privileges
{Bullet list of any elevated, sensitive, or unusual privileges — Global-level write/delete on
sensitive custom tables, system administration privileges, bulk delete, or cross-BU access.
Flag any that represent a least-privilege concern.}

### Related Wiki Pages
{Bullet links to the most relevant Detailed-Application-Design pages found in step 2a.}
```

**Preserved sections** (never overwrite — carry forward exactly as-is from existing page):
- Any `##` heading not listed above (diagrams, implementation notes, known issues, etc.)
- If no existing page: omit preserved sections; write Overview + Privilege Summary + Elevated Permissions + Business Analysis only

---

#### 2c. Write sub-pages (replace entirely — auto-generated, no hand-written content)

| Final path | Source |
|---|---|
| `wiki/Technical-Reference/roles/<RoleName>/metadata.json` | Privilege counts by level and verb, elevated-permission flags (see Step 4) |

---

#### 2d. Commit source data

Commit `src/dataverse/roles/<RoleName>/` to source control — this JSON is the canonical record of what was extracted from Dataverse.

---

### Step 3: Parse Role Data

Input: `src/dataverse/roles/<RoleName>/<RoleName>.role.json`

- Parse `role` fields: `roleid`, `name`, `description`, `modifiedon`, `ismanaged`
- Parse `privileges` array: group by action type and access level

Group privileges by action and table:
- Read/Create/Write/Delete/Append/AppendTo/Assign/Share
- Global/Deep/Local/Basic access levels (from `privilegedepthmask`)

### Step 4: Generate Documentation

1. Highlight high-impact privileges:
   - System-level administration privileges
   - Broad Global write/delete on sensitive custom tables
2. Create `<RoleName>.md`:
   - Role purpose summary
   - Privilege distribution table
   - Key business entities impacted
   - Notable elevated permissions
   - Least-privilege observations and recommendations
3. Create `metadata.json`:
   - privilege counts by level and verb
   - flags for elevated permissions

## Use Review Heuristics

- Flag roles with high counts of `Global` privileges.
- Flag roles granting both approval and payment-style capabilities.
- Compare same role names fetched across multiple environments and report differences.
- Prefer explicit findings over generic warnings.

## Example Requests

- "Document all roles under IncomeAssistanceSecurity."
- "Compare SIS Worker role between environments."
- "Create a security review for SAID roles."

## Integrate with Other Skills

- Use `doc-coauthoring` if stakeholders ask for consolidated executive summaries.

## Handle Errors

- If a role record has missing data, document what is available and note the gaps.
- If duplicate role names exist across business units, include business unit in output folder or metadata.
- If no roles are returned, report a clear "no roles found" result with the filter used.
