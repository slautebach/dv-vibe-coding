---
name: dv-doc-canvasapps
description: Analyze Dynamics 365 Dataverse canvas app components from live Dataverse and generate documentation for app metadata, dependencies, and integrations. Use when documenting canvas apps, reviewing app metadata, mapping connector usage, or auditing embedded command/dialog apps in D365 solutions.
---

# Dataverse Analyze Canvasapps

Analyze Dataverse canvas app exports retrieved directly from live Dataverse and generate documentation covering app purpose, dependencies, and maintainability.

## Dataverse Skills Dependency

This skill depends on the Dataverse-skills plugin for environment setup and direct Dataverse access.

Install it with:

```bash
copilot plugin marketplace add microsoft/Dataverse-skills
copilot plugin install dataverse@dataverse-skills
```

- Load `dv-overview` first.
- Use `dv-connect` to confirm the target environment and auth context before fetching.

## Output Structure

**Dataverse JSON** (committed to source control):
```
src/dataverse/canvas-apps/<AppName>/source/
  <AppName>.meta.xml          # Normalized metadata for analysis
  <AppName>.dataverse.json    # Raw Dataverse record for traceability
```

**Wiki** (committed — final output after AI merge):
```
wiki/Technical-Reference/canvas-apps/
  <AppName>.md                    ← index page (was README.md)
  <AppName>/
    .order                        ← dependencies, code-review
    dependencies.md
    code-review.md                ← was CodeReview.md
    metadata.json
```

> `src/dataverse/` is committed to source control as the canonical JSON snapshot extracted from the live environment. This gives a diff-friendly audit trail of environment changes and allows wiki generation to run from local files without re-fetching from Dataverse.

## Workflow

### Step 1: Fetch Canvas App from Dataverse

1. Load `dv-overview` and confirm the environment using `dv-connect`.
2. Run the fetch script to retrieve the latest canvas app payload:

```bash
python .github/skills/dv-doc-canvasapps/scripts/fetch-canvasapp-from-dataverse.py \
  --environment dev \
  --name mnp_emaildialog_8c1d7
```

Or by canvas app GUID:

```bash
python .github/skills/dv-doc-canvasapps/scripts/fetch-canvasapp-from-dataverse.py \
  --environment dev \
  --app-id e7274ede-a366-4cd5-8728-e909c7aeb04a
```

The script writes to `src/dataverse/canvas-apps/<AppName>/source/`:

- `<AppName>.meta.xml` — app metadata for analysis
- `<AppName>.dataverse.json` — raw Dataverse record for traceability

### Step 2: AI Merge — Apply Staged Output to Wiki Pages

After the script completes, the AI merges staged output into `wiki/Technical-Reference/canvas-apps/<AppName>.md` (index page) and sub-pages under `wiki/Technical-Reference/canvas-apps/<AppName>/`.

---

#### 2a. Gather domain context (do this before writing any files)

Search the following locations for references to this canvas app's name, display name, or related business terms:

1. `wiki/Detailed-Application-Design/*.md` — business domain overviews that reference this app or its business process
2. `wiki/Detailed-Application-Design/**/*.md` — sub-pages within each domain
3. `wiki/Technical-Reference/entities/` — entity pages for Dataverse tables referenced in `CdsDependencies`
4. `wiki/Technical-Reference/Cloud-Flows/` — cloud flow pages for flows listed in `ConnectionReferences`

Collect: which business process this app supports, the entities and connectors it depends on, and the intended user context.

---

#### 2b. Write/update `<AppName>.md` (index page)

**Auto-generated sections** (replace entirely from `src/dataverse/canvas-apps/<AppName>/source/<AppName>.meta.xml`):
- `## Overview` table — app metadata: `Name`, `DisplayName`, `AppVersion`, `Status`, `CreatedByClientVersion`, `MinClientVersion`
- `## Connectors` — list of all `ConnectionReferences` with connector IDs and types
- `## Dataverse Dependencies` — list of `CdsDependencies` (tables/flows referenced)

**AI-written section** (generate fresh on first run; update only if facts changed on re-runs):

Write or update `## Business Analysis` immediately after `## Dataverse Dependencies`:

```markdown
## Business Analysis

### Purpose
{1-3 sentences. What does this canvas app do in the Income Assistance system?
What user action or business task does it enable or support?}

### Domain Context
{Which business process or domain this app belongs to. Reference specific wiki pages.
Example: "Supports the [Email Communication](/wiki/Detailed-Application-Design/Communications)
process by providing a dialog for composing templated emails from a case record."}

### Connector Summary
{Brief description of the key connectors and what they are used for — e.g. Dataverse (read/write
records), Office 365 (send email), SharePoint (document storage). Focus on integrations that drive
the app's business value.}

### Referenced Entities
{Bullet list of the most important Dataverse tables this app reads or writes, and what data
it accesses or modifies on each. Skip purely lookup/reference tables.}

### Related Wiki Pages
{Bullet links to the most relevant Detailed-Application-Design pages found in step 2a.}
```

**Preserved sections** (never overwrite — carry forward exactly as-is from existing page):
- Any `##` heading not listed above (diagrams, implementation notes, known issues, etc.)
- If no existing page: omit preserved sections; write Overview + Connectors + Dataverse Dependencies + Business Analysis only

---

#### 2c. Write sub-pages (replace entirely — auto-generated, no hand-written content)

| Final path | Source |
|---|---|
| `wiki/Technical-Reference/canvas-apps/<AppName>/dependencies.md` | Connector inventory, flow references, dependent Dataverse components (see Steps 3–4) |
| `wiki/Technical-Reference/canvas-apps/<AppName>/code-review.md` | Generated from review heuristics (see Step 5) |
| `wiki/Technical-Reference/canvas-apps/<AppName>/metadata.json` | Normalized machine-readable extracts |

---

#### 2d. Commit source data

Commit `src/dataverse/canvas-apps/<AppName>/` to source control — this JSON is the canonical record of what was extracted from Dataverse.

---

### Step 3: Parse App Metadata

Use the fetched `<AppName>.meta.xml` as the authoritative source. Extract:

- `Name`, `DisplayName`, `AppVersion`, `Status`
- `CreatedByClientVersion`, `MinClientVersion`
- `DocumentUri`, `BackgroundImageUri`

Parse JSON-heavy fields safely:
- `ConnectionReferences`
- `CdsDependencies`
- `Tags`

### Step 4: Identify External Dependencies

- Dataverse references
- Flow/workflow references in connector hints

### Step 5: Generate Output

Write documentation to `wiki/Technical-Reference/canvas-apps/<AppName>/`:

- `<AppName>.md` — app purpose summary, key metadata, primary connectors (saved to `wiki/Technical-Reference/canvas-apps/<AppName>.md`)
- `dependencies.md` — connector inventory, referenced flows/workflows, dependent Dataverse components
- `code-review.md` — versioning concerns, connector sprawl, maintainability risks
- `metadata.json` — normalized machine-readable extracts

## Use Review Heuristics

- Flag apps with many connector dependencies and no description.
- Flag apps pinned to old minimum client versions.
- Flag references to flows that cannot be located in solutions.

## Example Requests

- "Document all canvas apps in IncomeAssistancePowerApps."
- "Review dependencies for mnp_emaildialog_8c1d7."
- "Create a connector inventory across canvas apps."

## Integrate with Other Skills

- Use `dataverse-solution-parser` for XML parsing and component cross-references.
- Use `dv-doc-flows` when canvas apps depend on Power Automate flows.

## Handle Errors

- If a `.meta.xml` file has invalid embedded JSON, report field-level errors and continue with remaining metadata.
- If binary `.msapp` files cannot be inspected, document that limitation explicitly and proceed with metadata-based analysis.
