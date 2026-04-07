---
name: dv-doc-entity
description: Retrieve and document Dynamics 365 / Dataverse entities by fetching live metadata directly from Dataverse. Generates wiki pages at wiki/Technical-Reference/entities/{entity}.md (overview, attributes, option sets, relationships), {entity}/forms.md, and {entity}/views.md. Supports a single entity (--entity) or all entities in a solution (--solution). Use when asked to "document entity", "generate entity docs", "create entity wiki page", "fetch entity metadata", "document solution components", "inspect live solution", or "generate wiki pages for all entities in a solution". Do NOT use for North52 formula documentation (use n52-doc skill) or for parsing solution XML files (use dataverse-solution-parser skill).
---

# Dataverse Entity Documentation Generator

Fetches live entity metadata from Dataverse and generates structured ADO wiki pages under `wiki/Technical-Reference/entities/`.

## Dataverse Skills Dependency

This skill requires the Dataverse-skills plugin for environment setup and authentication.

Install it with:

```bash
copilot plugin marketplace add microsoft/Dataverse-skills
copilot plugin install dataverse@dataverse-skills
```

Before running any live retrieval:

1. Load `dv-overview`.
2. Use `dv-connect` to confirm the target environment and auth context.
3. Then run the fetch script below.

## Output Structure

**Staging** (repo root, never committed — shared across all skills):
```
.staging/
  entities/
    {entity}.json               # Raw structured Dataverse data
    {entity}.md                 # Lean index page (overview + pages links)
    {entity}/
      attributes.md             # Custom + OOTB fields, local option sets
      relationships.md          # 1:N, N:1, N:N relationships
      forms.md
      views.md
```

**Wiki** (committed — final output after AI merge):
```
wiki/Technical-Reference/entities/
  .manifest.json                # Change-tracking: first-seen dates per entity and attribute
  .order                        # ADO wiki nav (alphabetical, always overwritten)
  {entity}.md                   # Index: overview + Business Analysis (AI-written)
  {entity}/
    .order                      # Always overwritten (attributes, relationships, forms, views)
    attributes.md               # Custom + OOTB fields, local option sets
    relationships.md            # All relationships
    forms.md                    # Active forms
    views.md                    # Saved queries
```

> **Why staging?** Final wiki pages may contain hand-written content (Business Analysis, ERD diagrams, custom notes). The script writes fresh Dataverse output to `.staging/` so the AI merge step can update auto-generated sections without overwriting preserved content. `.staging/` is gitignored and shared across all `dv-doc-*` skills.

## Output: Wiki Page Sections

| Page | Section | Contents |
|---|---|---|
| `{entity}.md` | Overview | Logical name, schema name, entity set, OTC, primary key, ownership, is custom, attribute/relationship counts, first documented |
| `{entity}.md` | Pages | Links to all sub-pages |
| `{entity}.md` | Business Analysis | **AI-written** — purpose, domain context, key custom fields explained, key relationships, wiki references |
| `attributes.md` | Preamble | Count summary: editable custom fields, OOTB fields, and virtual/shadow fields |
| `attributes.md` | Custom Fields | Editable `IsCustomAttribute = true` fields only (virtual/shadow fields excluded); includes **Introduced Version** column |
| `attributes.md` | Standard (OOTB) Fields | Editable standard fields (virtual/shadow fields excluded); includes **Introduced Version** column |
| `attributes.md` | Local Option Sets | One table per local picklist/multi-select with value/label pairs and option set description |
| `attributes.md` | Virtual / Shadow Fields | All virtual and logical label-cache fields (no display name); system-managed, not directly editable |
| `relationships.md` | Preamble | Count summary (1:N / N:1 / N:N breakdown) and column guide |
| `relationships.md` | Custom Relationships | All `IsCustomRelationship = true` — schema name, direction, related entity, attribute, **menu label**, **on-delete cascade** |
| `relationships.md` | Standard (OOTB) Relationships | All standard relationships with same columns |
| `forms.md` | Preamble | Count of active forms and how many have field-level detail available |
| `forms.md` | Form Summary | Summary table of all active forms: name, type (corrected labels), is-default, customizable |
| `forms.md` | Per-Form Detail | Fields grouped by **tab → section** (from `formjson` or `formxml`); flat list fallback if structure unavailable |
| `views.md` | Preamble | Count of views and note on data sources |
| `views.md` | View Summary | Summary table of all views: name, type, is-default, customizable |
| `views.md` | Per-View Detail | Columns with **display names**, **filter conditions** (from FetchXML), **order-by**, and raw FetchXML attributes |

## Workflow

### Step 1: Install Dependencies

```bash
pip install -r .github/skills/dv-doc-entity/scripts/requirements.txt
```

### Step 2: Fetch and Generate

**Single entity:**

```bash
python .github/skills/dv-doc-entity/scripts/fetch_entity_metadata.py \
  --entity mnp_application \
  --environment dev
```

**All entities in a solution:**

```bash
python .github/skills/dv-doc-entity/scripts/fetch_entity_metadata.py \
  --solution IncomeAssistanceCore \
  --environment dev
```

**Service principal auth:**

```bash
python .github/skills/dv-doc-entity/scripts/fetch_entity_metadata.py \
  --entity account --app-id <app-id> --client-secret <secret>
```

**Arguments:**

| Argument          | Default                             | Description                                              |
| ----------------- | ----------------------------------- | -------------------------------------------------------- |
| `--entity`        | _(mutually exclusive with --solution)_ | Entity logical name, e.g. `account`, `mnp_application` |
| `--solution`      | _(mutually exclusive with --entity)_   | Solution unique name — fetch all entities               |
| `--environment`   | `dev`                               | Accepted for backward compatibility; config is loaded from `.env`  |
| `--app-id`        | _(from config)_                     | App ID for service principal auth                        |
| `--client-secret` | _(interactive)_                     | Client secret; omit for browser auth                     |
| `--output-dir`    | `wiki/Technical-Reference/entities` | Override output path                                     |

**Authentication:** Uses `dataverse_sdk_client.py` (delegates to `.github/scripts/auth.py` from `dataverse@dataverse-skills`). Browser popup by default (`AUTH_METHOD=browser` in `.env`); tokens cached in OS credential store. Set `CLIENT_ID` + `CLIENT_SECRET` in `.env` for service principal auth.

### Step 3: AI Merge and Analysis

After the script completes, staged files in `.staging/entities/` must be merged into the final wiki pages. The AI handles this step — updating auto-generated content, preserving hand-written sections, and generating a Business Analysis grounded in wiki domain documentation.

---

#### 3a. Gather domain context (do this before writing any files)

Search the following locations for references to this entity's logical name, display name, or closely related business terms:

1. `wiki/Detailed-Application-Design/*.md` — business domain overviews (benefit calculation, case management, client payments, finance, etc.)
2. `wiki/Detailed-Application-Design/**/*.md` — sub-pages within each domain
3. `wiki/Technical-Reference/North52/` — any North52 formulas referencing this entity (field-level business rules)
4. `wiki/Technical-Reference/Cloud-Flows/` — cloud flows that read/write this entity
5. `wiki/Technical-Reference/Classic-Workflows/` — classic workflows on this entity
6. `wiki/Technical-Reference/entities/` — other entity pages with relationships to this one

Collect: domain names where this entity appears, key business processes it participates in, any business rules or calculations referencing its fields.

---

#### 3b. Write/update `{entity}.md` (index page)

**Auto-generated sections** (replace entirely from `.staging/entities/{entity}.md`):
- `## Overview` table
- `## Pages` links

**AI-written section** (generate fresh on first run; update only if facts changed on re-runs):

Write or update `## Business Analysis` immediately after `## Pages`:

```markdown
## Business Analysis

### Purpose
{1-3 sentences. What does this entity represent in the Income Assistance system?
For custom entities: what business concept does it model?
For standard entities (account, contact): how is it used in this solution specifically?}

### Domain Context
{Which business domains use this entity and how. Reference specific wiki pages.
Example: "Used in [Benefit Calculation](/wiki/Detailed-Application-Design/Benefit-Calculation)
to track approved service providers for invoicing."}

### Key Custom Fields
{Table or bullets for the most significant custom (mnp_*) fields — explain their business
purpose beyond the technical description. Focus on fields that drive business logic,
status flows, or integration with other entities.}

### Key Relationships
{Bullet list of the most important relationships (especially custom ones) — what they
connect and why. Skip virtual/name shadow fields and generic system relationships.}

### Related Wiki Pages
{Bullet links to the most relevant Detailed-Application-Design pages found in step 3a.}
```

**Preserved sections** (never overwrite — carry forward exactly as-is from existing page):
- Any `##` heading not listed above (ERD diagrams, implementation notes, known issues, etc.)
- If no existing page: omit preserved sections; write Overview + Pages + Business Analysis only

---

#### 3c. Write sub-pages (replace entirely — auto-generated, no hand-written content)

| Final path | Source |
|---|---|
| `wiki/Technical-Reference/entities/{entity}/attributes.md` | `.staging/entities/{entity}/attributes.md` |
| `wiki/Technical-Reference/entities/{entity}/relationships.md` | `.staging/entities/{entity}/relationships.md` |
| `wiki/Technical-Reference/entities/{entity}/forms.md` | `.staging/entities/{entity}/forms.md` |
| `wiki/Technical-Reference/entities/{entity}/views.md` | `.staging/entities/{entity}/views.md` |

---

#### 3d. Clean up staging

Delete `.staging/entities/{entity}.json`, `.staging/entities/{entity}.md`, and `.staging/entities/{entity}/` after all files are written successfully.

---

### Step 4: Review and Commit

1. Spot-check the Business Analysis section for accuracy and completeness.
2. Verify a few custom fields in `attributes.md` are correct.
3. Add or enhance any hand-written sections (PlantUML ERDs, implementation notes).
4. Stage changes with `git add` — the user reviews and commits.

## Comparison with Related Skills

| Skill | Source | Scope | Includes Forms/Views |
|---|---|---|---|
| `dv-doc-entity` | Live Dataverse | Single entity or full solution | Yes — forms.md + views.md |
| `dataverse-solution-parser` | Unpacked XML files | Solution XML files | Reads FormXml XML |

## API Endpoint Reference

See [references/api-endpoints.md](references/api-endpoints.md) for complete Dataverse Web API endpoint reference including solution components, entity metadata, attributes, forms, and views.

## Example Requests

- "Document the mnp_application entity from Dataverse."
- "Generate wiki pages for all entities in IncomeAssistanceCore."
- "Fetch live metadata for mnp_benefitassessment including forms and views."
- "Inspect the IncomeAssistance solution and create entity wiki pages."

## Error Handling

- If a solution is not found, the script exits with a clear message.
- If an individual entity fails during bulk fetch, it is skipped and reported; others continue.
- If `formjson` is not returned by the API, the forms page notes this limitation and still lists form names and types.
- If the `wiki/Technical-Reference/entities/` folder does not exist, the script creates it.

## Notes

- Only **local option sets** are included in the Option Sets section. Global option sets are referenced inline in the Attributes table under "Notes".
- **Virtual / Shadow Fields**: Fields with `AttributeType = Virtual` and no display name (picklist companion `*name` fields) plus logical attributes with no display name (lookup `*idname` / `*yominame` fields) are moved to the "Virtual / Shadow Fields" section at the bottom of `attributes.md`. This keeps the Custom Fields and OOTB Fields sections focused on directly editable fields.
- **Relationships**: The `Menu Label` column is populated from `AssociatedMenuConfiguration.Label` when the relationship is visible in the form nav (Behavior ≠ DoNotDisplay). The `On Delete` column shows the cascade behaviour from `CascadeConfiguration.Delete` for 1:N relationships only.
- **Forms**: `formjson` is tried first; if unavailable, `formxml` is fetched as a fallback. When structural data is available, fields are rendered grouped by tab and section. Form type labels use the corrected Dataverse type map (e.g., type 2 = Main, type 7 = Quick Create, type 10 = Main (Interactive), type 11 = Card).
- **Views**: The Columns table now includes a "Display Name" column resolved from the entity's attribute metadata. FetchXML is parsed to extract filter conditions and order-by clauses, displayed as readable bullet lists above the raw FetchXML Attributes table.
- Output directories are created automatically if they do not exist.
- The `.order` file in `wiki/Technical-Reference/entities/` is updated alphabetically by the script on each run.
- **Change tracking**: `.manifest.json` records when each **custom** entity and attribute was first seen. Re-running the script on an existing entity will add any new custom attributes but will never overwrite existing dates. The "Added" column in attribute tables and the date row in the entity overview are populated from this file.
- **Date sourcing**: For custom attributes, the date priority is: (1) `solutioncomponent.createdon` — earliest date the component appears in any solution layer, giving "when it arrived in this environment"; (2) `AttributeMetadata.CreatedOn` — used as a fallback when no solution component record exists, filtered for placeholder `1900-01-01` values; (3) today's date — last resort when neither source has a usable value. Custom attributes are batch-queried in groups of 20 for solution component dates. OOTB attributes always show `"-"` in the Added column (platform dates are unreliable for platform-owned fields).
- **Introduced Version column**: All attributes (custom and OOTB) include an `Introduced Version` column sourced from `AttributeMetadata.IntroducedVersion` (e.g., `1.0.0.0` for solution-added fields, `9.2.0.0` for platform fields). This is not a date but correlates to the solution or product version that first defined the column.
- **Date Added for OOTB components**: OOTB entities display `"-"` for the date row in the entity overview (instead of a date). OOTB attributes always show `"-"` in the "Added" column. Date tracking applies to custom entities and custom attributes only.

