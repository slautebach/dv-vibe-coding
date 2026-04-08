---
name: dv-doc-appmodules
description: Analyze Dynamics 365 Dataverse model-driven app modules and related site maps from live Dataverse, then generate app navigation and component documentation. Use when documenting AppModules, app navigation, sitemap structure, app component coverage, or model-driven app composition.
---

# Dataverse Analyze Appmodules

Analyze model-driven app definitions retrieved directly from live Dataverse and produce documentation for app composition, navigation structure, and component dependencies.

## Dataverse Skills Dependency

This skill depends on the Dataverse-skills plugin for live Dataverse access.

Install it with:

```bash
copilot plugin marketplace add microsoft/Dataverse-skills
copilot plugin install dataverse@dataverse-skills
```

- Load `dv-overview` first.
- Use `dv-connect` to confirm the target environment and auth state before fetching.

## Output Structure

**Dataverse JSON** (committed to source control):
```
src/dataverse/app-modules/<AppUniqueName>/
  <AppUniqueName>.appmodule.json   # Merged app module + sitemap data
  <AppUniqueName>.dataverse.json   # Raw Dataverse records for traceability
```

**Wiki** (committed — final output after AI merge):
```
wiki/Technical-Reference/app-modules/
  <AppUniqueName>.md              ← index page (was README.md)
  <AppUniqueName>/
    .order                        ← navigation, code-review
    navigation.md
    code-review.md                ← was CodeReview.md
    metadata.json
```

> `src/dataverse/` is committed to source control as the canonical JSON snapshot extracted from the live environment. This gives a diff-friendly audit trail of environment changes and allows wiki generation to run from local files without re-fetching from Dataverse.

## Workflow

### Step 1: Fetch App Module from Dataverse

1. Load `dv-overview` and confirm the environment using `dv-connect`.
2. Run the fetch script to retrieve the latest app module and sitemap:

```bash
python .github/skills/dv-doc-appmodules/scripts/fetch-appmodule-from-dataverse.py \
  --environment dev \
  --name "SIS App"
```

Or by unique name or GUID:

```bash
python .github/skills/dv-doc-appmodules/scripts/fetch-appmodule-from-dataverse.py \
  --environment dev \
  --unique-name mnp_sisapp

python .github/skills/dv-doc-appmodules/scripts/fetch-appmodule-from-dataverse.py \
  --environment dev \
  --app-id-guid 3a7c1e2d-5f4b-4e6a-9c8d-1b2e3f4a5b6c
```

The script writes to `src/dataverse/app-modules/<AppUniqueName>/`:

- `<AppUniqueName>.appmodule.json` — merged `{"appmodule": {...}, "sitemap": {...}}`
- `<AppUniqueName>.dataverse.json` — raw Dataverse records for traceability

### Step 2: AI Merge — Apply Staged Output to Wiki Pages

After the script completes, the AI merges staged output into `wiki/Technical-Reference/app-modules/<AppUniqueName>.md` (index page) and sub-pages under `wiki/Technical-Reference/app-modules/<AppUniqueName>/`.

---

#### 2a. Gather domain context (do this before writing any files)

Search the following locations for references to this app module's name, display name, or related navigation areas:

1. `wiki/Detailed-Application-Design/*.md` — business domain overviews that reference this app's areas or entities
2. `wiki/Detailed-Application-Design/**/*.md` — sub-pages within each domain
3. `wiki/Technical-Reference/entities/` — entity pages for entities listed in the app's sitemap subareas
4. `wiki/Technical-Reference/roles/` — security role pages that mention this app or its intended user persona

Collect: which business domains this app serves, key processes it supports, and any relevant user role or access context.

---

#### 2b. Write/update `<AppUniqueName>.md` (index page)

**Auto-generated sections** (replace entirely from `src/dataverse/app-modules/<AppUniqueName>/<AppUniqueName>.appmodule.json`):
- `## Overview` table — app metadata: `UniqueName`, `name`, `formfactor`, `clienttype`, `appmoduleversion`, `statecode`
- `## Navigation Areas` — summary of top-level sitemap areas (Area titles only)

**AI-written section** (generate fresh on first run; update only if facts changed on re-runs):

Write or update `## Business Analysis` immediately after `## Navigation Areas`:

```markdown
## Business Analysis

### Purpose
{1-3 sentences. What is this model-driven app module used for in the Income Assistance system?
Which user persona or team uses it, and what primary workflow does it support?}

### Domain Context
{Which business domains or processes are covered by this app. Reference specific wiki pages.
Example: "Covers [Benefit Assessment](/wiki/Detailed-Application-Design/Benefit-Calculation)
and [Case Management](/wiki/Detailed-Application-Design/Case-Management) processes."}

### Key Navigation Areas
{Bullet list of the most significant sitemap areas and what they expose — entity-backed subareas,
key views or dashboards. Focus on what a new user needs to understand to navigate the app effectively.}

### Intended User Roles
{Which security roles are expected to use this app. Note any admin-only vs front-line worker
distinction if evident from the entities or privileges surfaced in the sitemap.}

### Related Wiki Pages
{Bullet links to the most relevant Detailed-Application-Design pages found in step 2a.}
```

**Preserved sections** (never overwrite — carry forward exactly as-is from existing page):
- Any `##` heading not listed above (diagrams, implementation notes, known issues, etc.)
- If no existing page: omit preserved sections; write Overview + Navigation Areas + Business Analysis only

---

#### 2c. Write sub-pages (replace entirely — auto-generated, no hand-written content)

| Final path | Source |
|---|---|
| `wiki/Technical-Reference/app-modules/<AppUniqueName>/navigation.md` | Parsed sitemap from `src/dataverse/app-modules/<AppUniqueName>/<AppUniqueName>.appmodule.json` (see Step 3) |
| `wiki/Technical-Reference/app-modules/<AppUniqueName>/code-review.md` | Generated from review heuristics (see Step 4) |
| `wiki/Technical-Reference/app-modules/<AppUniqueName>/metadata.json` | Component counts, sitemap depth, source record IDs |

---

#### 2d. Commit source data

Commit `src/dataverse/app-modules/<AppUniqueName>/` to source control — this JSON is the canonical record of what was extracted from Dataverse.

---

### Step 3: Parse App Module Metadata

From `<AppUniqueName>.appmodule.json`, extract `appmodule` fields:

- `UniqueName`, `name`, `formfactor`, `clienttype`, `appmoduleversion`, `statecode`

Parse `sitemap.sitemapxml` for navigation hierarchy:

- `Area` → `Group` → `SubArea`
- entity-backed vs URL-backed subareas

### Step 4: Generate Documentation

1. Create `<AppUniqueName>.md`:
   - app purpose summary
   - component inventory summary
   - top-level navigation areas
2. Create `navigation.md`:
   - detailed area/group/subarea tree
   - linked entities and labels
3. Create `code-review.md`:
   - navigation usability concerns
   - orphaned or duplicated entries
   - component sprawl or missing critical entities
4. Create `metadata.json`:
   - component counts
   - sitemap structure depth
   - source record IDs

## Use Review Heuristics

- Flag apps with large component counts and shallow navigation.
- Flag subareas referencing entities not listed in app components.
- Flag duplicate labels pointing to different entities.

## Example Requests

- "Document all model-driven apps from IncomeAssistancePowerApps."
- "Compare SIS app navigation between versions."
- "Review sitemap structure for SEI app."

## Integrate with Other Skills

- Use `dataverse-solution-parser` for XML interpretation and component type context.
- Use `plantuml` if a diagram of navigation hierarchy is requested.

## Handle Errors

- If the app module has no associated sitemap, document partial coverage.
- If labels are missing, fall back to IDs and unique names.
- If records are malformed, skip and report paths and parser errors.
