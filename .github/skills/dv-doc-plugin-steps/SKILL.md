---
name: dv-doc-plugin-steps
description: Analyze Dynamics 365 Dataverse plugin assemblies and SDK message processing steps from live Dataverse and generate execution pipeline documentation. Use when reviewing plugin registrations, stage/mode configuration, filtering attributes, assembly coverage, or documenting plugin assemblies and SDK message processing steps.
---

# Dataverse Analyze Plugin Steps

Analyze plugin assemblies and registered processing steps retrieved directly from live Dataverse to document execution behavior, deployment patterns, risk points, and supporting plugin-code context.

## Dataverse Skills Dependency

This skill depends on the Dataverse-skills plugin for any live Dataverse inspection.

Install it with:

```bash
copilot plugin marketplace add microsoft/Dataverse-skills
copilot plugin install dataverse@dataverse-skills
```

- Load `dv-overview` first.
- Use `dv-connect` to confirm the target environment before fetching plugin metadata.

## Output Structure

**Dataverse JSON** (committed to source control):
```
src/dataverse/plugin-steps/<AssemblyName>/
  <AssemblyName>.plugin-steps.json  # Grouped assembly + steps
  <AssemblyName>.dataverse.json     # Raw FetchXML records for traceability
```

**Wiki** (committed — final output after AI merge):
```text
wiki/Technical-Reference/plugin-steps/
  <AssemblyName>.md               ← index page (was README.md)
  <AssemblyName>/
    .order                        ← step-inventory, code-review
    step-inventory.md
    code-review.md                ← was CodeReview.md
    metadata.json
```

> `src/dataverse/` is committed to source control as the canonical JSON snapshot extracted from the live environment. This gives a diff-friendly audit trail of environment changes and allows wiki generation to run from local files without re-fetching from Dataverse.

## Workflow

### Step 1: Fetch Plugin Steps from Dataverse

1. Load `dv-overview` and confirm the environment with `dv-connect`.
2. Run the fetch script to retrieve the latest plugin registrations:

```bash
python .github/skills/dv-doc-plugin-steps/scripts/fetch-plugin-steps-from-dataverse.py \
  --environment dev \
  --assembly "MNP.IA.Plugins"
```

Or filter by entity or fetch all custom steps:

```bash
python .github/skills/dv-doc-plugin-steps/scripts/fetch-plugin-steps-from-dataverse.py \
  --environment dev \
  --entity contact

python .github/skills/dv-doc-plugin-steps/scripts/fetch-plugin-steps-from-dataverse.py \
  --environment dev \
  --all
```

The script writes to `src/dataverse/plugin-steps/<AssemblyName>/`:

- `<AssemblyName>.plugin-steps.json` — `{"assembly": "...", "steps": [...]}`
- `<AssemblyName>.dataverse.json` — raw FetchXML records for traceability

### Step 2: AI Merge — Apply Staged Output to Wiki Pages

After the script completes, the AI merges staged output into `wiki/Technical-Reference/plugin-steps/<AssemblyName>.md` (index page) and sub-pages under `wiki/Technical-Reference/plugin-steps/<AssemblyName>/`.

---

#### 2a. Gather domain context (do this before writing any files)

Search the following locations for references to this assembly's name, registered entities, or related business rules:

1. `wiki/Detailed-Application-Design/*.md` — business domain overviews that reference these entities or describe the business rules enforced
2. `wiki/Detailed-Application-Design/**/*.md` — sub-pages within each domain
3. `wiki/Technical-Reference/entities/` — entity pages for each entity/message pair registered in this assembly
4. `Source/MNP.CRM.EntityBounds/` — early-bound C# classes for entity context and field names used in plugin logic
5. `wiki/Technical-Reference/Classic-Workflows/` — workflows that may overlap in trigger entity and business responsibility

Collect: which business rules this assembly enforces, what entities it governs, and why a plugin was chosen over a workflow or formula.

---

#### 2b. Write/update `<AssemblyName>.md` (index page)

**Auto-generated sections** (replace entirely from `src/dataverse/plugin-steps/<AssemblyName>/<AssemblyName>.plugin-steps.json`):
- `## Overview` table — assembly metadata: name, version, isolation mode, `pluginassemblyid`, step count
- `## Processing Pipeline Summary` — steps grouped by entity/message with stage, mode, and rank

**AI-written section** (generate fresh on first run; update only if facts changed on re-runs):

Write or update `## Business Analysis` immediately after `## Processing Pipeline Summary`:

```markdown
## Business Analysis

### Purpose
{1-3 sentences. What business rules or enforcement logic does this plugin assembly provide
in the Income Assistance system? Why does this logic exist as a plugin rather than a workflow
or North52 formula?}

### Domain Context
{Which business domains or processes rely on this plugin for correctness or enforcement.
Reference specific wiki pages.
Example: "Enforces validation rules for the [Benefit Assessment](/wiki/Detailed-Application-Design/Benefit-Calculation)
process — prevents submission if required fields are incomplete."}

### Execution Profile
{Summary of execution stages (Pre-Validation, Pre-Operation, Post-Operation), sync vs async modes,
and any notable rank ordering or image dependencies. Highlight any steps that are synchronous
real-time operations (highest risk to performance and user experience).}

### Key Entities and Messages
{Bullet list of the entity/message pairs this assembly handles, what each step does at a
business level, and any filtering attributes that limit when steps fire.}

### Related Wiki Pages
{Bullet links to the most relevant Detailed-Application-Design pages found in step 2a.}
```

**Preserved sections** (never overwrite — carry forward exactly as-is from existing page):
- Any `##` heading not listed above (diagrams, implementation notes, known issues, etc.)
- If no existing page: omit preserved sections; write Overview + Processing Pipeline Summary + Business Analysis only

---

#### 2c. Write sub-pages (replace entirely — auto-generated, no hand-written content)

| Final path | Source |
|---|---|
| `wiki/Technical-Reference/plugin-steps/<AssemblyName>/step-inventory.md` | Tabular step list with stage, mode, rank, and filter attributes (see Step 4) |
| `wiki/Technical-Reference/plugin-steps/<AssemblyName>/code-review.md` | Generated from review heuristics (see Step 4) |
| `wiki/Technical-Reference/plugin-steps/<AssemblyName>/metadata.json` | Counts by entity/stage/mode, code-context coverage, unresolved mappings |

---

#### 2d. Commit source data

Commit `src/dataverse/plugin-steps/<AssemblyName>/` to source control — this JSON is the canonical record of what was extracted from Dataverse.

---

### Step 3: Cross-Reference Plugin Source Code

When plugin source folders are present, extract class-level context from C# files to improve registration analysis:

```text
Source\Integrations\MNP.IA.SSIS.CRM.Integrations\MNP.IA.Plugins\**\*.cs
Source\Integrations\MNP.IA.SSIS.CRM.Integrations\MNP.SEI.Plugins\**\*.cs
Source\Integrations\MNP.IA.SSIS.CRM.Integrations\MNP.ProgramType\ProgramTypeMSS\**\*.cs
```

Extract from each plugin class:
- plugin class name and namespace
- likely Dataverse message/entity intent from class names, constants, or request handling
- referenced services/helpers (`IOrganizationService`, tracing, repositories, validators)
- notable guardrails (depth checks, filtering logic, input validation)

### Step 4: Generate Documentation

Input: `wiki/Technical-Reference/plugin-steps/<AssemblyName>/<AssemblyName>.plugin-steps.json`

1. Parse assembly and step data from the JSON.
2. Join steps to plugin types and assemblies by plugin type name.
3. Cross-reference `plugintype_typename` with source plugin classes.
4. Create `<AssemblyName>.md`:
   - assembly overview
   - processing pipeline summary by entity/message
   - plugin implementation context summary when source code is available
5. Create `step-inventory.md`:
   - tabular list of all steps with stage, mode, rank, and filters
6. Create `code-review.md`:
   - ordering conflicts (same stage/entity/message with unclear rank strategy)
   - missing filtering attributes on update steps
   - risk from broad registrations
   - code-level risks observed in plugin handlers
7. Create `metadata.json`:
   - counts by assembly/entity/stage/mode
   - code-context coverage
   - unresolved mappings

## Use Review Heuristics

- Flag update steps without `filteringattributes`.
- Flag many steps on the same entity/stage with overlapping responsibilities.
- Flag steps missing pre/post images when business logic likely depends on old/new values.
- Flag assembly registrations that appear stale or unreferenced.
- Flag steps whose plugin type cannot be mapped to source classes in known plugin folders.
- Flag plugin implementations with minimal tracing or unclear validation paths.

## Example Requests

- "Document all plugin registrations in IncomeAssistanceProcesses."
- "Review step ordering and filtering on contact update plugins."
- "Generate a plugin pipeline inventory by entity."

## Integrate with Other Skills

- Use `dataverse-solution-parser` for XML schema interpretation and cross-component context.
- Use `microsoft-docs` for plugin pipeline stage semantics when clarification is required.

## Handle Errors

- If a step references a plugin type not found in extracted assemblies, keep the step and mark mapping as unresolved.
- If plugin source folders are missing or inaccessible, continue step analysis and mark code-context extraction as unavailable.
