---
name: dv-doc-xaml-workflows
description: Analyze classic XAML-based workflows from live Dataverse and generate comprehensive documentation. Use when user asks to document classic workflows, analyze XAML workflows, review D365 background/real-time workflow logic, or create workflow documentation from D365 solutions. Triggers on phrases like "analyze classic workflow", "document XAML workflow", "review workflow logic", "analyze workflows from solution", or "document classic D365 workflows". Do NOT use for Power Automate cloud flows (use dv-doc-flows skill instead).
---

# Dataverse Analyze XAML Workflows

Analyze classic XAML-based Dynamics 365 workflows retrieved directly from live Dataverse and generate comprehensive documentation including descriptions, PlantUML diagrams, and code reviews.

## Dataverse Skills Dependency

This skill depends on the Dataverse-skills plugin for live Dataverse access.

Install it with:

```bash
copilot plugin marketplace add microsoft/Dataverse-skills
copilot plugin install dataverse@dataverse-skills
```

- Load `dv-overview` first.
- Use `dv-connect` to confirm the target environment and authentication before fetching.

## Required References

Before parsing any workflow XAML, load the authoritative schema reference from the **dataverse-solution-parser** skill:

```
.github/skills/dataverse-solution-parser/references/workflow-schema.md
```

This file is the primary guide for understanding every XAML element, activity type, expression syntax, control flow pattern, and variable type encountered in workflow files. Read it before Step 3.

For project-specific conventions and `AssemblyQualifiedName` patterns used in this codebase, see [references/xaml-project-patterns.md](references/xaml-project-patterns.md).

## Output Structure

**Staging** (repo root, never committed — shared across all skills):
```
.staging/classic-workflows/<WorkflowName>-<GUID>/
  <WorkflowName>-<GUID>.xaml          # Workflow XAML logic
  <WorkflowName>-<GUID>.xaml.data.xml # Workflow metadata
  <WorkflowName>-<GUID>.dataverse.json # Raw API payload for traceability
```

**Wiki** (committed — final output after AI merge):
```
wiki/Technical-Reference/classic-workflows/
├── <WorkflowName>.md       # Business-focused overview with embedded diagram
└── <WorkflowName>/
    ├── .order              # code-review
    ├── logic-diagram.puml  # PlantUML activity diagram source
    ├── logic-diagram.png   # Rendered PNG image
    ├── code-review.md      # Technical review and recommendations (was CodeReview.md)
    └── metadata.json       # Extracted workflow metadata
```

> **Why staging?** Wiki pages may contain hand-written content — business context, diagrams, notes. The script never overwrites these directly. It writes fresh Dataverse output to `.staging/` so the AI merge step can apply only what changed. `.staging/` is in `.gitignore` and shared across all `dv-doc-*` skills.

## Workflow

### Step 1: Fetch Workflow from Dataverse

1. Load `dv-overview` and confirm the environment with `dv-connect`.
2. Run the fetch script to retrieve the latest classic workflow from Dataverse:

```bash
python .github/skills/dv-doc-xaml-workflows/scripts/fetch-workflow-from-dataverse.py \
  --environment dev \
  --name "SIS - Close Case"
```

Or fetch by GUID:

```bash
python .github/skills/dv-doc-xaml-workflows/scripts/fetch-workflow-from-dataverse.py \
  --environment dev \
  --workflow-id E9581E0B-F5C7-49CD-81B7-7EAF5D668B3A
```

The script writes to `.staging/classic-workflows/<WorkflowName>-<GUID>/`:

- `<WorkflowName>-<GUID>.xaml` — workflow XAML logic
- `<WorkflowName>-<GUID>.xaml.data.xml` — workflow metadata
- `<WorkflowName>-<GUID>.dataverse.json` — raw API payload for traceability

Use the generated `.xaml` + `.xaml.data.xml` pair as input for the remaining steps.

**Example pair:**

```
SIS-CloseCase-E9581E0B-F5C7-49CD-81B7-7EAF5D668B3A.xaml
SIS-CloseCase-E9581E0B-F5C7-49CD-81B7-7EAF5D668B3A.xaml.data.xml
```

### Step 2: AI Merge — Apply Staged Output to Wiki Pages

After the script completes, the AI merges staged output into `wiki/Technical-Reference/Classic-Workflows/<WorkflowName>.md` (index page) and sub-pages under `wiki/Technical-Reference/Classic-Workflows/<WorkflowName>/`.

---

#### 2a. Gather domain context (do this before writing any files)

Search the following locations for references to this workflow's name, primary entity, or related business process:

1. `wiki/Detailed-Application-Design/*.md` — business domain overviews that describe the process this workflow automates
2. `wiki/Detailed-Application-Design/**/*.md` — sub-pages within each domain
3. `wiki/Technical-Reference/entities/` — entity page for the `PrimaryEntity` this workflow is bound to
4. `wiki/Technical-Reference/Cloud-Flows/` — cloud flows that may share the same trigger entity or overlap in business responsibility

Collect: which business process this workflow automates, what the trigger entity represents, whether related flows or workflows cover adjacent steps, and any documented business rules it enforces.

---

#### 2b. Write/update `<WorkflowName>.md` (index page)

**Auto-generated sections** (replace entirely from `.staging/classic-workflows/<WorkflowName>-<GUID>/<WorkflowName>-<GUID>.xaml.data.xml` and parsed XAML):
- `## Overview` table — workflow metadata: `Name`, `WorkflowId`, `Category`, `Mode` (Background/Real-time), `PrimaryEntity`, `StateCode`, trigger conditions (`TriggerOnCreate`, `TriggerOnDelete`, `TriggerOnUpdateAttributeList`)
- `## Workflow Diagram` — embedded PlantUML activity diagram (`![Workflow Logic Diagram](./<WorkflowName>/logic-diagram.png)`)

**AI-written section** (generate fresh on first run; update only if facts changed on re-runs):

Write or update `## Business Analysis` immediately after `## Workflow Diagram`:

```markdown
## Business Analysis

### Purpose
{1-3 sentences. What business process does this classic workflow automate in the Income Assistance
system? What outcome does it achieve and what triggers it to run?}

### Domain Context
{Which business domain or process this workflow belongs to. Reference specific wiki pages.
Example: "Part of the [Case Management](/wiki/Detailed-Application-Design/Case-Management)
domain — fires when a case is closed to complete follow-up tasks automatically."}

### Trigger and Type
{Whether this is a Background (async) or Real-time (sync) workflow, the primary entity it is
bound to, and the exact trigger condition (on create, on delete, on field change — list the
specific fields from TriggerOnUpdateAttributeList). Note if it is on-demand.}

### Key Steps and Decision Points
{Bullet summary of the main logical steps and any conditions/branches in the workflow — what
it checks, what it sets, what it creates or updates, and what business rules it enforces.
Reference XAML DisplayName values for the most important activities.}

### Related Wiki Pages
{Bullet links to the most relevant Detailed-Application-Design pages found in step 2a.}
```

**Preserved sections** (never overwrite — carry forward exactly as-is from existing page):
- Any `##` heading not listed above (diagrams, implementation notes, known issues, etc.)
- If no existing page: omit preserved sections; write Overview + Workflow Diagram + Business Analysis only

---

#### 2c. Write sub-pages (replace entirely — auto-generated, no hand-written content)

| Final path | Source |
|---|---|
| `wiki/Technical-Reference/Classic-Workflows/<WorkflowName>/logic-diagram.puml` | Generated PlantUML activity diagram (see Step 5) |
| `wiki/Technical-Reference/Classic-Workflows/<WorkflowName>/logic-diagram.png` | Rendered from `logic-diagram.puml` via `plantuml -tpng` |
| `wiki/Technical-Reference/Classic-Workflows/<WorkflowName>/code-review.md` | Generated from review heuristics (see Step 6) |
| `wiki/Technical-Reference/Classic-Workflows/<WorkflowName>/metadata.json` | Extracted workflow metadata (see Step 7) |

---

#### 2d. Clean up staging

Delete `.staging/classic-workflows/<WorkflowName>-<GUID>/` after all files are written successfully.

---

### Step 3: Extract Metadata from .data.xml

Use the automation script for reliable metadata extraction:

```bash
python .github/skills/dv-doc-xaml-workflows/scripts/extract-workflow-metadata.py <xaml-path> [output-dir]
```

The script parses both files and generates `metadata.json`.

**Key fields from `.data.xml`:**

| Field                          | Description                                      |
| ------------------------------ | ------------------------------------------------ |
| `Name`                         | Human-readable workflow name                     |
| `WorkflowId`                   | GUID identifier                                  |
| `Category`                     | 0=Workflow, 3=Action, 4=Business Process Flow    |
| `Mode`                         | 0=Background (async), 1=Real-time (sync)         |
| `OnDemand`                     | 1=on-demand trigger                              |
| `TriggerOnCreate`              | 1=fires on record create                         |
| `TriggerOnDelete`              | 1=fires on record delete                         |
| `TriggerOnUpdateAttributeList` | Comma-separated fields that trigger the workflow |
| `PrimaryEntity`                | The entity (table) this workflow is bound to     |
| `StateCode`                    | 0=Draft, 1=Activated                             |

### Step 4: Parse XAML Logic

**Load first:** Read `.github/skills/dataverse-solution-parser/references/workflow-schema.md` for the complete XAML element reference — activity types, control flow, expressions, variable types, and common patterns.

Use the **dataverse-solution-parser** skill when you need to:

- Look up an unfamiliar activity element or attribute
- Understand field type context (`mxs:Money`, `mxs:EntityReference`, etc.)
- Cross-reference `PrimaryEntity` against an entity's field definitions

**Parsing strategy** (from workflow-schema.md § Parsing Strategy):

1. Extract trigger and mode from `<mxswa:Workflow>` attributes or `.data.xml`
2. Walk `ActivityReference` elements — the `DisplayName` is the primary signal for what each step does
3. Map data flow: `GetEntityProperty` → variables → `SetEntityProperty` → `UpdateEntity`/`CreateEntity`
4. Identify decision points: `ConditionSequence` / `EvaluateCondition` + `If` blocks
5. Flag custom plugin activities by `AssemblyQualifiedName` not containing `Microsoft.Crm` or `Microsoft.Xrm`

**See also:** [references/xaml-project-patterns.md](references/xaml-project-patterns.md) for MNP-specific plugin names, DisplayName conventions, and option set value mappings used in this project.

### Step 5: Generate `<WorkflowName>.md`

Read `prompts/README.md` for full criteria, then generate `<WorkflowName>.md`.

**Location:** `wiki/Technical-Reference/Classic-Workflows/<WorkflowName>.md`

Steps:

1. Read prompts/README.md for structure and evaluation criteria
2. Analyze workflow logic and metadata
3. Create `logic-diagram.puml` with PlantUML activity diagram
4. Generate PNG: `plantuml -tpng logic-diagram.puml`
5. Write `<WorkflowName>.md` with embedded diagram: `![Workflow Logic Diagram](./<WorkflowName>/logic-diagram.png)`

**See:** [prompts/README.md](prompts/README.md) for complete criteria.

### Step 6: Generate `code-review.md`

Read `prompts/CodeReview.md` for full criteria, then generate the technical review.

**Location:** `wiki/Technical-Reference/Classic-Workflows/<WorkflowName>/code-review.md`

**See:** [prompts/CodeReview.md](prompts/CodeReview.md) for complete criteria.

### Step 7: Generate metadata.json

Run the metadata script from Step 3. It produces `metadata.json` automatically.

If the script is unavailable, manually extract the fields listed in Step 3 from the `.data.xml` file and combine with step counts from the XAML.

### Step 8: Handle Multiple Workflows

When analyzing multiple workflows:

1. Process sequentially for quality
2. Report progress after each: `[checkmark] WorkflowName - Documentation generated`
3. Skip workflows that fail to parse; report errors
4. Provide a summary count at the end

## Naming Convention

Extract clean workflow name from filename by removing the GUID suffix:

```
Filename:  SIS-CloseCase-E9581E0B-F5C7-49CD-81B7-7EAF5D668B3A.xaml
Name:      SIS-CloseCase
Index Page: wiki/Technical-Reference/Classic-Workflows/SIS-CloseCase.md
Sub-pages:  wiki/Technical-Reference/Classic-Workflows/SIS-CloseCase/
```

Prefer the `Name` attribute from `.data.xml` for the document title (e.g. "SIS - Close Case").

## Integration with Other Skills

### dataverse-solution-parser (required for parsing)

Invoke this skill to:

- Load `references/workflow-schema.md` — authoritative XAML element reference for all activity types, control flow, expressions, and variable types
- Understand entity field definitions when a workflow reads/writes fields on `PrimaryEntity`
- Cross-reference entity logical names (e.g. `incident` = Case, `invoice` = Invoice) against `Entity.xml`

**Usage:**

```
Before parsing the XAML, invoke the dataverse-solution-parser skill and read
.github/skills/dataverse-solution-parser/references/workflow-schema.md
```

### plantuml

Use for diagram generation guidance if the standard `plantuml -tpng` command is unavailable.

### git-commit

Commit generated documentation after analysis with a message like:

```
docs: add classic workflow documentation for SIS-CloseCase
```
