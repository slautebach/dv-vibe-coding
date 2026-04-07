---
name: n52-doc
description: Analyze North52 Decision Suite formulas directly from Dynamics 365 Dataverse and generate comprehensive documentation. Use when user asks to document North52 formulas, review formula performance/maintainability, create formula index pages or code-review.md files, or analyze North52 formulas. Triggers on phrases like "analyze North52 formula", "document this formula", "review North52 code", or "fetch North52 formulas".
---

# North52 Formula Analyzer

This skill analyzes North52 Decision Suite formulas by fetching them directly from Dataverse and generates comprehensive documentation to improve formula understanding, maintainability, and performance.

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
  north52/
    <entity>/
      <shortcode>/
        <shortcode>.n52              # Raw formula source
        analysis_metadata.json       # Fresh metadata from Dataverse
        *.fetch.xml                  # FetchXML queries (if any)
```

**Wiki** (committed — final output after AI merge):
```
wiki/Technical-Reference/North52/
  <entity>/
    <shortcode>.md                   # Index page: Overview + Business Analysis
    <shortcode>/
      .order                         # code-review (ADO wiki nav)
      code-review.md                 # Technical analysis and recommendations
      analysis_metadata.json         # Persisted metadata (includes AI timestamps)
      <shortcode>.n52                # Formula source code
      *.fetch.xml                    # FetchXML queries (if any)
      diagram.puml                   # Optional — complex formulas only
      diagram.png                    # Optional — rendered from diagram.puml
      dt_<SheetName>.md              # Optional — one per visible decision table sheet
      dt_index.md                    # Optional — index of all dt_ sheet files
```

> **Why staging?** Wiki pages may contain hand-written content (diagrams, implementation notes, known issues). The fetch script never overwrites these directly — it writes fresh Dataverse output to `.staging/` so the AI merge step can update only what changed. `.staging/` is in `.gitignore` and shared across all `dv-doc-*` skills.

## Output: Wiki Page Sections

| Page | Section | Contents |
|---|---|---|
| `<shortcode>.md` | Overview | Formula name, shortcode, entity, type, event, execution mode, category, stage, complexity summary, last modified |
| `<shortcode>.md` | Business Analysis | **AI-written** — purpose, domain context, key logic, related wiki pages |
| `<shortcode>/code-review.md` | Technical Review | Performance, maintainability, naming, best practices, recommendations |
| `<shortcode>/analysis_metadata.json` | Cached Metadata | Formula structure, function counts, variables, timestamps |
| `<shortcode>/<shortcode>.n52` | Formula Source | Raw North52 formula code |
| `<shortcode>/dt_*.md` | Decision Tables | One file per visible sheet (when applicable) |
| `<shortcode>/diagram.puml` + `.png` | Logic Diagram | PlantUML activity diagram (complex formulas only) |

**Prompt Files** (read before generating each doc type):

- [`prompts/codereview.md`](prompts/codereview.md) - Prompt + rules for generating code-review.md

## Trigger Phrases

Use this skill when user says:

- "analyze North52 formula [shortcode]"
- "fetch North52 formulas from [environment]"
- "document this formula"
- "review North52 code for [entity]"
- "generate formula index page/code-review.md"
- "analyze all North52 formulas"
- "extract all North52 formulas"
- "extract all formulas to Documentation"
- "list North52 formulas in [environment]"
- "rank North52 formulas by complexity"
- "which North52 formulas are most complex"
- "generate complexity ranking"
- "prioritize formulas for AI analysis"

## Workflow

### Step 1: Install Dependencies

```bash
pip install -r .github/skills/n52-doc/scripts/requirements.txt
```

### Step 2: Fetch from Dataverse

1. Load `dv-overview` and confirm the environment using `dv-connect`.
2. Run the fetch script to retrieve the latest formula(s) from Dataverse:

**Single formula by shortcode:**

```bash
python .github/skills/n52-doc/scripts/fetch_north52_from_dataverse.py \
  --environment dev \
  --shortcode PWa \
  --analyze
```

**All formulas for an entity:**

```bash
python .github/skills/n52-doc/scripts/fetch_north52_from_dataverse.py \
  --environment dev \
  --entity mnp_benefitassessment \
  --analyze
```

**All formulas (incremental — skip already documented):**

```bash
python .github/skills/n52-doc/scripts/fetch_north52_from_dataverse.py \
  --environment dev \
  --all \
  --analyze \
  --skip-existing
```

**List available formulas:**

```bash
python .github/skills/n52-doc/scripts/fetch_north52_from_dataverse.py \
  --environment dev \
  --list
```

The script writes to `.staging/north52/<entity>/<shortcode>/`:
- `<shortcode>.n52` — formula source code (plaintext)
- `analysis_metadata.json` — structured formula metadata
- `*.fetch.xml` — FetchXML queries (if any)

**Authentication:** Uses shared `dataverse_sdk_client.py` (from `dataverse@dataverse-skills`). Browser popup by default; tokens cached in OS credential store. Set `CLIENT_ID` + `CLIENT_SECRET` in `.env` for service principal auth.

### Step 3: AI Merge — Apply Staged Output to Wiki Pages

After the script completes, the AI merges staged output into `wiki/Technical-Reference/North52/<entity>/<shortcode>.md` (index page) and the `<shortcode>/` sub-folder.

---

#### 3a. Gather domain context (do this before writing any files)

Search the following locations for references to this formula's entity, shortcode, name, or related business terms:

1. `wiki/Detailed-Application-Design/*.md` — business domain overviews that reference this entity or formula
2. `wiki/Detailed-Application-Design/**/*.md` — sub-pages within each domain
3. `wiki/Technical-Reference/entities/` — entity pages for the formula's source entity (custom fields, relationships)
4. `wiki/Technical-Reference/Cloud-Flows/` — cloud flows that may trigger or depend on this formula
5. `wiki/Technical-Reference/Classic-Workflows/` — classic workflows on the same entity
6. `wiki/Technical-Reference/North52/<entity>/` — sibling formulas on the same entity

Collect: which business domain this formula belongs to, what business process it implements, which fields it reads or writes, and any related formulas or flows.

---

#### 3b. Write/update `<shortcode>.md` (index page)

**Location:** `wiki/Technical-Reference/North52/<entity>/<shortcode>.md`

**Auto-generated sections** (replace entirely from `.staging/north52/<entity>/<shortcode>/analysis_metadata.json`):
- `## Overview` table — formula name, shortcode, entity, type, event, execution mode, category, stage, complexity tier

**AI-written section** (generate fresh on first run; update only if formula changed on re-runs):

Write or update `## Business Analysis` immediately after `## Overview`:

```markdown
## Business Analysis

### Purpose
{1-3 sentences. What business rule or calculation does this formula implement?
What problem does it solve, and what happens if it doesn't run or is bypassed?}

### Domain Context
{Which business domain or process this formula belongs to. Reference specific wiki pages.
Example: "Part of the [Benefit Assessment](/wiki/Detailed-Application-Design/Benefit-Calculation)
domain — runs on the Update event of mnp_benefitassessment to validate eligibility criteria."}

### Key Logic
{Plain-English summary of the formula's main logic — the key conditions, calculations,
or validations it performs. Reference important variables or function patterns if useful.
Focus on business meaning, not technical implementation.}

### Related Formulas
{Bullet links to sibling formulas on the same entity that work together with this one.
Omit if none found.}

### Related Wiki Pages
{Bullet links to the most relevant Detailed-Application-Design pages found in step 3a.}
```

**Preserved sections** (never overwrite — carry forward exactly as-is from existing page):
- Any `##` heading not listed above (ERD diagrams, implementation notes, known issues, etc.)
- If no existing page: omit preserved sections; write Overview + Business Analysis only

---

#### 3c. Write sub-pages (replace entirely — auto-generated, no hand-written content)

| Final path | Source |
|---|---|
| `wiki/Technical-Reference/North52/<entity>/<shortcode>/code-review.md` | AI-generated from `.n52` source using [`prompts/codereview.md`](prompts/codereview.md) |
| `wiki/Technical-Reference/North52/<entity>/<shortcode>/<shortcode>.n52` | Copied from `.staging/north52/<entity>/<shortcode>/` |
| `wiki/Technical-Reference/North52/<entity>/<shortcode>/analysis_metadata.json` | Copied from staging; update `ai_documentation` timestamps |
| `wiki/Technical-Reference/North52/<entity>/<shortcode>/*.fetch.xml` | Copied from staging (if any) |
| `wiki/Technical-Reference/North52/<entity>/<shortcode>/diagram.puml` | AI-generated PlantUML (complex formulas only) |
| `wiki/Technical-Reference/North52/<entity>/<shortcode>/diagram.png` | Rendered via `python .github/skills/n52-doc/scripts/generate_diagram.py <entity> <shortcode>` |
| `wiki/Technical-Reference/North52/<entity>/<shortcode>/dt_*.md` | Generated via `python .github/skills/n52-doc/scripts/extract_decision_tables.py <entity> <shortcode>` |
| `wiki/Technical-Reference/North52/<entity>/<shortcode>/dt_index.md` | Generated alongside `dt_*.md` |

Update `.order` file in the `<shortcode>/` folder to list: `code-review`

---

#### 3d. Clean up staging

Delete `.staging/north52/<entity>/<shortcode>/` after all files are written successfully.

---

### Step 4: Review and Commit

1. Spot-check the Business Analysis section for accuracy.
2. Verify the Overview table matches the formula's actual metadata.
3. Add or enhance any hand-written sections (PlantUML ERDs, implementation notes).
4. Stage changes with `git add` — the user reviews and commits.

---

## Smart Caching

The skill uses smart caching to avoid regenerating unchanged formulas:

**Check status** before generating docs:

```bash
python .github/skills/n52-doc/scripts/ai_evaluate_formulas.py <entity> <shortcode>
```

**Status values:**
- `UP_TO_DATE` — formula unchanged since last AI run; skip doc generation
- `NEEDS_GENERATION` — no docs exist yet; generate all
- `NEEDS_UPDATE` — formula changed since last AI run; regenerate
- `MISSING_METADATA` — run Step 2 (fetch) first

**Force regeneration** (ignore timestamps):

```bash
python .github/skills/n52-doc/scripts/ai_evaluate_formulas.py --force <entity> <shortcode>
```

**After generating docs**, update timestamps:

```bash
python .github/skills/n52-doc/scripts/update_ai_timestamps.py <entity> <shortcode>
```

## Decision Tree

```
User request → Parse intent
│
├─ STEP 2: Fetch from Dataverse
│  ├─ List available environments?
│  │  └─ run_in_terminal: `python config_loader.py --list`
│  │
│  ├─ List all formulas in environment?
│  │  └─ run_in_terminal: `python fetch_north52_from_dataverse.py --environment <env> --list`
│  │
│  ├─ Extract ALL formulas to .staging/?
│  │  ├─ Full extraction:
│  │  │  └─ run_in_terminal: `python fetch_north52_from_dataverse.py --environment <env> --all --analyze`
│  │  └─ Incremental (skip already-extracted formulas):
│  │     └─ run_in_terminal: `python fetch_north52_from_dataverse.py --environment <env> --all --analyze --skip-existing`
│  │
│  ├─ Fetch all formulas for entity with analysis?
│  │  └─ run_in_terminal: `python fetch_north52_from_dataverse.py --environment <env> --entity <name> --analyze`
│  │
│  └─ Fetch specific formula by shortcode with analysis?
│     └─ run_in_terminal: `python fetch_north52_from_dataverse.py --environment <env> --shortcode <code> --analyze`
│
└─ STEP 3: AI Merge (documentation generation)
   ├─ Rank all formulas by complexity (prioritise AI analysis)?
   │  ├─ All formulas:
   │  │  └─ run_in_terminal: `python rank_formula_complexity.py`
   │  ├─ Only formulas needing AI docs:
   │  │  └─ run_in_terminal: `python rank_formula_complexity.py --needs-docs`
   │  ├─ Top N formulas:
   │  │  └─ run_in_terminal: `python rank_formula_complexity.py --top <N>`
   │  └─ Filter to entity:
   │     └─ run_in_terminal: `python rank_formula_complexity.py --entity <entity>`
   │
   ├─ Check which formulas need AI documentation?
   │  └─ run_in_terminal: `python ai_evaluate_formulas.py --all [--list-pending]`
   │
   ├─ Generate docs for specific formula?
   │  └─ Steps:
   │     1. Check status: `python ai_evaluate_formulas.py <entity> <shortcode>`
   │     2. If up-to-date → inform user, offer --force option
   │     3. If needs update → proceed with generation
   │     4. Read .n52 file and analysis_metadata.json from .staging/
   │     5. Generate <shortcode>.md (index page) using SKILL guidelines
   │     6. Generate code-review.md using SKILL guidelines
   │     7. If decision table JSON present in .n52 → run: `python extract_decision_tables.py <entity> <shortcode>`
   │     8. If logic is complex → generate diagram.puml (PlantUML activity diagram)
   │     9. If diagram.puml created → run: `python generate_diagram.py <entity> <shortcode>`
   │    10. Update timestamps: `python update_ai_timestamps.py <entity> <shortcode>`
   │    11. Delete .staging/north52/<entity>/<shortcode>/
   │
   └─ Force regeneration (ignore timestamps)?
      └─ run_in_terminal: `python ai_evaluate_formulas.py --force <entity> <shortcode>`
```

## Critical Requirements

1. **Four-step process** - Install → Fetch → AI Merge → Review/Commit
2. **Staging first** - Fetch writes to `.staging/north52/` never directly to wiki
3. **Smart caching** - Only regenerate AI docs if formula changed or user forces
4. **Timestamp tracking** - Compare `last_formula_modified` with `description_generated`/`codereview_generated`
5. **Dataverse source** - Fetch directly from live environments using Web API
6. **Output path pattern**: `wiki/Technical-Reference/North52/<entity>/<shortcode>/` (create if missing)
7. **Metadata-first approach** - Step 2 (fetch) must complete before Step 3 (AI merge) can run
8. **Update timestamps** - After generating docs, run `update_ai_timestamps.py` to track AI runs
9. **Use forward slashes** - Cross-platform path compatibility
10. **Environment configuration** - Settings loaded from `.env` at the repository root

## Setup Requirements

### 1. Configuration File

Create `.env` from the template:

```bash
cp .env.example .env
# Edit .env with your environment URL, tenant ID, and other settings
```

**Environment Configuration**:

```ini
DATAVERSE_URL=https://dev-org.crm3.dynamics.com
TENANT_ID=your-tenant-id
ENVIRONMENT_NAME=dev
ENVIRONMENT_DESCRIPTION=Development environment
MAKE_ENVIRONMENT_ID=your-make-environment-id
MAKE_SOLUTION_ID=your-make-solution-id
NORTH52_APP_ID=your-north52-app-id
```

### 2. Install Dependencies

```bash
cd .github/skills/n52-doc/scripts
pip install -r requirements.txt
```

**Required packages**:

- `azure-identity` - Azure AD authentication
- `requests` - HTTP client for Dataverse Web API

**Note**: The Dataverse client compatibility layer (`dataverse_sdk_client.py`) and configuration loader (`config_loader.py`) are shared libraries in `.github/scripts/`. They are automatically imported via Python path manipulation in the skill scripts.

### 3. Authentication Setup

**Option A: Interactive Browser Authentication** (Recommended for Development)

No additional setup required! The script will open your browser for Azure AD login.

```bash
python fetch_north52_from_dataverse.py --environment dev --list
```

**Option B: Service Principal Authentication** (Recommended for Production)

Set up app registration in Azure AD and pass client secret:

```bash
# Via CLI argument
python fetch_north52_from_dataverse.py --environment prod --client-secret <secret> --list

# Via environment variable
export DATAVERSE_CLIENT_SECRET=<secret>
python fetch_north52_from_dataverse.py --environment prod --list
```

**Clear cached authentication**:

```bash
python fetch_north52_from_dataverse.py --clear-auth
```

## Tool Integration

### Helper Scripts

Python scripts available in `scripts/` folder for automation:

#### 1. Dataverse Formula Fetcher (Step 2)

**Purpose**: Retrieve North52 formulas directly from Dataverse Web API

**When**: User wants to fetch the latest formulas, analyze specific formulas, or list available formulas

**Script**: `fetch_north52_from_dataverse.py`

**Commands**:

```bash
cd .github/skills/n52-doc/scripts

# List available environments
python config_loader.py --list

# List all formulas in dev environment (default)
python fetch_north52_from_dataverse.py --list

# List formulas in specific environment
python fetch_north52_from_dataverse.py --environment prod --list

# Extract ALL formulas to Documentation folder (full extraction)
python fetch_north52_from_dataverse.py --environment dev --all --analyze

# Extract ALL formulas, skip ones already extracted (incremental update)
python fetch_north52_from_dataverse.py --environment dev --all --analyze --skip-existing

# Fetch and analyze specific formula by shortcode
python fetch_north52_from_dataverse.py --environment dev --shortcode PWa --analyze

# Fetch and analyze all formulas for an entity
python fetch_north52_from_dataverse.py --environment dev --entity account --analyze

# Fetch formula by exact name
python fetch_north52_from_dataverse.py --environment dev --name "Account - Calculate Age" --analyze

# Output as JSON
python fetch_north52_from_dataverse.py --environment dev --entity account --json

# Service principal authentication
python fetch_north52_from_dataverse.py --environment prod --client-secret <secret> --list
```

**Output**:

- When `--analyze` flag is used:
  - `.staging/north52/<entity>/<shortcode>/<shortcode>.n52`
  - `.staging/north52/<entity>/<shortcode>/analysis_metadata.json`
- When `--list` flag is used: Console output of all formulas
- When `--json` flag is used: JSON output to console

**Key Features**:

- Fetches directly from Dataverse using Web API
- Supports multiple authentication methods
- Auto-detects workspace root
- Handles large formula descriptions efficiently
- Cleans up old files when formulas are renamed

#### 2. AI Evaluator (Step 3)

**Purpose**: Check which formulas need AI documentation and generate `<shortcode>.md`/`code-review.md`

**When**: After metadata extraction, to generate or update AI documentation

**Script**: `ai_evaluate_formulas.py`

**Commands**:

```bash
cd .github/skills/n52-doc/scripts

# Check all formulas and show status
python ai_evaluate_formulas.py --all

# List only formulas that need documentation
python ai_evaluate_formulas.py --all --list-pending

# Check specific formula status
python ai_evaluate_formulas.py account PWa

# Force regeneration (ignore timestamps)
python ai_evaluate_formulas.py --force account PWa
```

**Smart Caching**:

- Only regenerates if formula changed or `--force` flag used
- Compares timestamps: `last_formula_modified` vs `description_generated`/`codereview_generated`

**Output**:

- Status report showing which formulas need documentation
- Instructions for GitHub Copilot to generate docs

**Workflow**:

1. Run `ai_evaluate_formulas.py --all --list-pending` to see which formulas need docs
2. For each pending formula, GitHub Copilot generates `<shortcode>.md` and `code-review.md`
3. Run `update_ai_timestamps.py` to update metadata after generation

#### 3. Update AI Timestamps (Step 3 - Post-generation)

**Purpose**: Update metadata timestamps after `<shortcode>.md`/`code-review.md` are generated

**When**: After GitHub Copilot generates documentation

**Script**: `update_ai_timestamps.py`

**Commands**:

```bash
cd .github/skills/n52-doc/scripts

# Update timestamps for specific formula
python update_ai_timestamps.py account PWa

# Update timestamps for all formulas that have markdown files
python update_ai_timestamps.py --all
```

**Output**: Updates `ai_documentation` section in `analysis_metadata.json` with current timestamps

#### 4. Configuration Loader (Utility)

**Purpose**: List available environments and load environment configuration

**When**: User needs to see which environments are configured

**Script**: `config_loader.py`

**Commands**:

```bash
cd .github/skills/n52-doc/scripts

# List all configured environments
python config_loader.py --list
```

**Output**: Configured environment name from `.env` → `ENVIRONMENT_NAME`

#### 5. North52 Function Dictionary Extractor (Maintainer Utility)

**Purpose**: Update `north52_functions.py` dictionary from the latest markdown reference

**When**: New North52 functions are released or the markdown reference is updated

**Script**: `extract_north52_functions.py`

**Command**:

```bash
cd .github/skills/n52-doc/scripts
python extract_north52_functions.py
```

**Output**: Overwrites `north52_functions.py` with latest function metadata

**Note**: This script is for maintainers only and not part of the main documentation workflow.

#### 6. Formula Complexity Ranker

**Purpose**: Scan all `analysis_metadata.json` files and generate a prioritised ranking report so the most complex (highest-value) formulas are analysed by AI first.

**When**: Before starting a batch AI documentation run, or when deciding which formulas to document next.

**Script**: `rank_formula_complexity.py`

**Commands**:

```bash
cd .github/skills/n52-doc/scripts

# Generate full ranking report (all formulas)
python rank_formula_complexity.py

# Only formulas that still need AI documentation
python rank_formula_complexity.py --needs-docs

# Show top 50 formulas only
python rank_formula_complexity.py --top 50

# Filter to a specific entity
python rank_formula_complexity.py --entity mnp_benefitassessment

# Preview in terminal without writing a file
python rank_formula_complexity.py --dry-run

# Custom output path
python rank_formula_complexity.py --output path/to/report.md
```

**Scoring formula**:

| Metric                | Weight |
| --------------------- | ------ |
| Total function calls  | ×1     |
| Variable count        | ×5     |
| FetchXML queries      | ×10    |
| Decision tables       | ×8     |
| Max nesting level     | ×15    |
| Unique function count | ×2     |

**Tiers**: 🔴 CRITICAL (≥500) · 🟠 HIGH (200–499) · 🟡 MEDIUM (50–199) · 🟢 LOW (<50)

**Output**: `wiki/Technical-Reference/North52/FormulaComplexityRanking.md` — a ranked Markdown table with per-tier detail sections, showing AI docs status for each formula.

---

#### 7. Decision Table Extractor

**Purpose**: Parse the decision table spreadsheet JSON embedded as a comment at the end of `.n52` files and generate `dt_<SheetName>.md` files for each visible sheet.

**When**: After Step 2 extraction, when a formula is a Decision Table type. Run before or after generating `<shortcode>.md`/`code-review.md`.

**Script**: `extract_decision_tables.py`

**Commands**:

```bash
cd .github/skills/n52-doc/scripts

# Extract decision tables for a specific formula
python extract_decision_tables.py mnp_writeoff gDt

# Extract decision tables for all formulas (skip already-generated files)
python extract_decision_tables.py --all

# Force overwrite existing dt_ files
python extract_decision_tables.py --all --force
python extract_decision_tables.py mnp_writeoff gDt --force

# Check status only (no files written)
python extract_decision_tables.py --check mnp_writeoff gDt
```

**Output** (per formula folder):

- `dt_<SheetName>.md` — One file per visible decision table sheet
- `dt_index.md` — Summary index linking all sheet files

**Sheet rendering**:

| Column Type             | Badge              |
| ----------------------- | ------------------ |
| Condition               | 🔵 Condition       |
| Condition-Or variants   | 🔵 Condition (OR)  |
| Action-Command (server) | 🟢 Action (Server) |
| Action-Clientside       | 🟡 Action (Client) |
| Calc-Inline             | 🟣 Calc (Inline)   |

- Column headers include: label, type badge, and Dataverse field reference
- Long action cell values (>120 chars) are truncated in the table with full code in collapsible `<details>` blocks
- Global Calculations / Global Actions / Global FetchXml sheets are included when they contain data

---

## Metadata Management

**Purpose**: `analysis_metadata.json` caches formula structure to avoid re-fetching from Dataverse

**Location**: `wiki/Technical-Reference/North52/<entity>/<shortcode>/analysis_metadata.json`

### Required Schema v2.0

**Validation Checklist**:

- ✓ `metadata_version` = "2.0"
- ✓ `source_files` section with paths to .n52 file
- ✓ `formula` section with name, entity, shortcode, type, event
- ✓ `analysis` section with decision_tables, variables, functions
- ✓ `ai_documentation` section with timestamp fields

**Regenerate if**: Missing, wrong version, incomplete schema, or validation fails

### Metadata Workflow

```
1. Fetch formula from Dataverse with --analyze flag
2. Parse formula code and extract metadata
3. Save to .staging/north52/<entity>/<shortcode>/
4. AI merge step copies to wiki/Technical-Reference/North52/<entity>/<shortcode>/
5. Load metadata → Use as guide for AI documentation
6. After generating docs → Update ai_documentation timestamps
7. Save updated metadata
```

---

## Single Formula Analysis Workflow

> For the full workflow, see [Step 2: Fetch from Dataverse](#step-2-fetch-from-dataverse) and [Step 3: AI Merge](#step-3-ai-merge--apply-staged-output-to-wiki-pages) above. This section provides a condensed reference for single-formula analysis.

### STEP 1: Fetch Formula from Dataverse

**Goal**: Retrieve formula from live environment and write to `.staging/north52/<entity>/<shortcode>/`

#### 1.1: List Available Environments

```bash
python .github/skills/n52-doc/scripts/config_loader.py --list
```

**Output**: Shows configured environments (dev, test, prod, etc.)

#### 1.2: Fetch and Analyze Formula

**By shortcode (recommended)**:

```bash
python .github/skills/n52-doc/scripts/fetch_north52_from_dataverse.py --environment dev --shortcode PWa --analyze
```

**By entity and shortcode**:

```bash
python .github/skills/n52-doc/scripts/fetch_north52_from_dataverse.py --environment dev --entity account --shortcode PWa --analyze
```

**All formulas for an entity**:

```bash
python .github/skills/n52-doc/scripts/fetch_north52_from_dataverse.py --environment dev --entity account --analyze
```

**What it does**:

1. Connects to Dataverse environment using config
2. Fetches formula(s) from `north52_formula` entity
3. Analyzes formula code → Functions, variables, complexity
4. Writes `<shortcode>.n52` → Formula code
5. Writes `analysis_metadata.json` → Structured metadata

**Output**: `.staging/north52/<entity>/<shortcode>/`

- `analysis_metadata.json`
- `<shortcode>.n52`

---

### STEP 2: Generate AI Documentation

**Goal**: Create `<shortcode>.md` (index page) and `code-review.md` using AI analysis

#### 2.1: Check if Documentation is Needed

**Command**:

```bash
python .github/skills/n52-doc/scripts/ai_evaluate_formulas.py account PWa
```

**What it checks**:

- Does `analysis_metadata.json` exist? (If no → run Step 1 first)
- Do `<shortcode>.md` and `code-review.md` exist?
- Compare `last_formula_modified` vs `description_generated`/`codereview_generated`
- Status: UP_TO_DATE, NEEDS_GENERATION, or NEEDS_UPDATE

**Example output**:

```
FORMULA STATUS: account/PWa
Status: ✅ UP_TO_DATE
Reason: AI analysis up to date (last run: 2026-02-19T10:30:00)

Formula: Account - Calculate Age
Type: ClientSide - Calculation
Event: Create, Update
```

#### 2.2: Generate Documentation (if needed)

**Skip if**: Status is UP_TO_DATE (unless user requests --force regeneration)

**Process**:

1. Load `analysis_metadata.json` from `.staging/`
2. Read `<shortcode>.n52` file from `.staging/`
3. Gather domain context (step 3a above)
4. Generate `<shortcode>.md` — Overview + Business Analysis (index page)
5. Generate `code-review.md` (technical analysis)
6. If logic is complex → generate diagram.puml and render PNG
7. Update timestamps

#### 2.3: Generate `<shortcode>.md` (index page)

Follow the rules in [3b above](#3b-writeupdate-shortcodemd-index-page): auto-generated Overview table + AI-written Business Analysis section.

#### 2.4: Generate `code-review.md`

**Prompt file**: [`prompts/codereview.md`](prompts/codereview.md)

Read `prompts/codereview.md` for the full prompt, required sections, and style guidelines before generating this document.

#### 2.5: Generate PlantUML Diagram (if logic is complex)

If the formula has significant branching, multiple decision points, or multi-step calculations, generate a PlantUML activity diagram.

**Create** `wiki/Technical-Reference/North52/<entity>/<shortcode>/diagram.puml` using PlantUML activity diagram syntax (use `@startuml` / `@enduml`, `start`/`stop`, `:Activity;`, `if/else/endif`).

**Then render to PNG**:

```bash
cd .github/skills/n52-doc/scripts
python generate_diagram.py account PWa
```

**Requirements**:

- Java Runtime Environment (JRE 8+): https://www.java.com/download/
- `plantuml.jar` placed at `.github/tools/plantuml.jar`: https://plantuml.com/download

**Embed in `<shortcode>.md`** (add a Logic Flow Diagram section):

```markdown
## Logic Flow Diagram

![Logic Flow](diagram.png)
```

#### 2.6: Update Timestamps

**After generating all files**:

```bash
python .github/skills/n52-doc/scripts/update_ai_timestamps.py account PWa
```

**What it does**:

- Updates `description_generated` timestamp
- Updates `codereview_generated` timestamp
- Saves updated `analysis_metadata.json`

---

## Best Practices

### Formula Fetching

1. **Use shortcode when possible** - Shortcodes are unique identifiers
2. **Specify environment** - Always know which environment you're analyzing
3. **Use --analyze flag** - Generates complete metadata in one step
4. **Check before fetching** - Use `--list` to see available formulas first

### Documentation Generation

1. **Check status first** - Use `ai_evaluate_formulas.py` before generating
2. **Respect timestamps** - Don't regenerate unless formula changed
3. **Use --force sparingly** - Only when you need to override cache
4. **Update timestamps** - Always run `update_ai_timestamps.py` after generation

### Environment Management

1. **Keep .env secure** - Contains environment URLs and tenant IDs (git-ignored)
2. **Use service principals for automation** - More secure than interactive auth
3. **Clear auth when switching accounts** - Use `--clear-auth` flag
4. **Test in dev first** - Always validate in lower environments

---

## North52 Knowledge Base

Reference when analyzing functions and making recommendations:

- **Functions**: https://support.north52.com/knowledgebase/functions/
- **Advanced View**: https://support.north52.com/knowledgebase/advanced-view/
- **Business Process Activities**: https://support.north52.com/knowledgebase/business-process-activities/

**Local references** (see `references/` folder):

- [north52-functions.md](references/north52-functions.md) - Complete function list
- [north52-functions-complete.md](references/north52-functions-complete.md) - Detailed function info
- [north52-business-process-activities.md](references/north52-business-process-activities.md)

---

## Not This Skill

Don't use this skill for:

- ❌ Modifying formulas (use D365 solution development workflows)
- ❌ Deploying formulas (use deployment pipelines)
- ❌ Debugging runtime errors (use Dynamics 365 troubleshooting)
- ❌ Creating new formulas from scratch (use North52 development guides)

---

## Appendices

### Appendix A: Full Metadata Schema Example

**Location**: `wiki/Technical-Reference/North52/<entity>/<shortcode>/analysis_metadata.json`

```json
{
  "metadata_version": "2.0",
  "generated": "2026-02-24T12:48:27.463505",
  "source_files": {
    "formula_path": "wiki/Technical-Reference/North52/mnp_benefitassessment/oIY",
    "n52f_file": "oIY.n52",
    "yml_file": "",
    "fetch_xml_files": []
  },
  "formula": {
    "name": "PCHB - Benefit Assessment - ClientSide - Calculation",
    "source_entity": "mnp_benefitassessment",
    "shortcode": "oIY",
    "formula_type": "ClientSide - Calculation",
    "event": "Create, Update",
    "category": "PCHB",
    "mode": "Client Side",
    "stage": "Pre-Operation"
  },
  "analysis": {
    "decision_tables": 3,
    "variables": ["IncomeThreshold", "TotalANI", "BenefitAmount"],
    "variable_count": 3,
    "functions": {
      "FindValueFD": 4,
      "SetVar": 21,
      "GetVar": 46,
      "If": 10
    },
    "function_count": 4,
    "total_function_calls": 81,
    "fetch_count": 0,
    "fetch_files": [],
    "complexity_indicators": {
      "has_loops": false,
      "max_nesting_level": 3,
      "uses_client_side": true,
      "uses_server_side": false
    }
  },
  "ai_documentation": {
    "description_generated": null,
    "codereview_generated": null,
    "last_formula_modified": "2026-02-24T10:00:00.000000"
  }
}
```

### Appendix B: Example Output Structure

```
wiki/Technical-Reference/North52/
└── mnp_benefitassessment/
│   ├── oIY.md                     ← index page
│   └── oIY/
│       ├── oIY.n52
│       ├── analysis_metadata.json
│       ├── code-review.md
│       ├── diagram.puml           ← optional
│       └── diagram.png            ← optional
└── mnp_writeoff/
    ├── gDt.md                     ← index page
    └── gDt/
        ├── gDt.n52
        ├── analysis_metadata.json
        ├── code-review.md
        ├── dt_DecisionTable.md
        └── dt_index.md
```

**File Descriptions**:

- **`.n52`**: North52 formula code (plaintext, no HTML encoding)
- **`analysis_metadata.json`**: Structured metadata with formula analysis
- **`<shortcode>.md`**: Index page — Overview table (auto-generated) + Business Analysis (AI-written)
- **`code-review.md`**: Technical analysis and recommendations
- **`diagram.puml`**: PlantUML activity diagram source (generated by Copilot for complex formulas)
- **`diagram.png`**: Rendered PNG from `diagram.puml` (generated via `generate_diagram.py`)
- **`dt_<SheetName>.md`**: Decision table sheet documentation (one per visible sheet, generated via `extract_decision_tables.py`)
- **`dt_index.md`**: Index file linking all `dt_*.md` sheet files

### Appendix C: Troubleshooting

**Problem**: "Required dependencies not installed!"

**Solution**:

```bash
cd .github/skills/n52-doc/scripts
pip install -r requirements.txt
```

---

**Problem**: ".env file not found"

**Solution**:

```bash
cp .env.example .env
# Edit .env with your environment details
```

---

**Problem**: "Formula not found with shortcode: XXX"

**Solution**:

1. Verify shortcode is correct: `python fetch_north52_from_dataverse.py --list`
2. Check environment: Make sure you're using the right `--environment` flag
3. Verify formula is active (not deactivated in Dataverse)

---

**Problem**: Authentication fails with "Access denied"

**Solution**:

1. Clear cached auth: `python fetch_north52_from_dataverse.py --clear-auth`
2. Verify you have correct permissions in Dataverse
3. Check TENANT_ID in .env is correct
4. For service principal: Verify app_id and client_secret

---

**Problem**: "Analysis modules not available"

**Solution**:

- The `--analyze` flag requires `analyze_formula.py` and `metadata_builder.py` to be present
- Verify all required scripts are in the scripts/ folder
- Check for Python syntax errors in those files

---

**Problem**: `generate_diagram.py` reports "plantuml.jar not found"

**Solution**:

1. Download `plantuml.jar` from https://plantuml.com/download
2. Place it at `.github/tools/plantuml.jar` in the repository root
3. Verify Java is installed: `java -version`

---

**Problem**: `generate_diagram.py` reports "Java Runtime Environment not found"

**Solution**:

1. Install Java from https://www.java.com/download/
2. Ensure `java` is on your PATH: `java -version`
