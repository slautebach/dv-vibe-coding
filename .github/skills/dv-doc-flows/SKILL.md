---
name: dv-doc-flows
description: Analyze Power Automate cloud flows from live Dataverse and generate comprehensive documentation. Use when user asks to document cloud flows, analyze Power Automate flows, review flow logic, or create flow documentation from D365 solutions. Triggers on phrases like "analyze cloud flow", "document Power Automate", "review flow", or "analyze flows from solution".
---

# Dataverse Analyze Flows

Analyze Power Automate cloud flows retrieved directly from live Dataverse and generate comprehensive documentation including descriptions, PlantUML diagrams, and code reviews.

## Dataverse Skills Dependency

This skill depends on the Dataverse-skills plugin for live environment access.

Install it with:

```bash
copilot plugin marketplace add microsoft/Dataverse-skills
copilot plugin install dataverse@dataverse-skills
```

- Load `dv-overview` first for tool-routing and environment safety rules.
- Use `dv-connect` to verify the target environment and authentication before fetching.

## When to Use

Trigger this skill when:

- User mentions "analyze cloud flow", "document Power Automate", "review flow"
- User asks to "analyze flows from solution" or "document flows"
- User wants to understand flow logic or create flow documentation
- User mentions "cloud flow analysis", "flow documentation", or "Power Automate review"

## Overview

This skill retrieves the latest cloud flow definition directly from Dataverse, then generates structured documentation. Documentation is saved to `wiki/Technical-Reference/Cloud-Flows/<FlowName>.md` (index page) and `wiki/Technical-Reference/Cloud-Flows/<FlowName>/` (sub-pages) including PlantUML diagrams (both .puml source and .png images) and metadata.

**Output Structure:**

**Dataverse JSON** (committed to source control):
```
src/dataverse/cloud-flows/
├── <FlowName>/
│   ├── <FlowName>-<GUID>.json          # Normalized flow JSON for analysis
│   └── <FlowName>-<GUID>.dataverse.json # Raw Dataverse record for traceability
```

**Wiki** (committed — final output after AI merge):
```
wiki/Technical-Reference/cloud-flows/
├── <FlowName>.md           # High-level flow overview with embedded diagram
└── <FlowName>/
    ├── .order              # code-review
    ├── logic-diagram.puml  # PlantUML source for flow diagram
    ├── logic-diagram.png   # Generated PNG image from PlantUML
    ├── code-review.md      # Technical review and recommendations (was CodeReview.md)
    └── metadata.json       # Extracted flow metadata
```

> `src/dataverse/` is committed to source control as the canonical JSON snapshot extracted from the live environment. This gives a diff-friendly audit trail of environment changes and allows wiki generation to run from local files without re-fetching from Dataverse.

## Workflow

### Step 1: Fetch Cloud Flow from Dataverse

1. Load `dv-overview` and confirm the environment using `dv-connect`.
2. Run the fetch script to retrieve the latest flow from Dataverse:

```bash
python .github/skills/dv-doc-flows/scripts/fetch-flow-from-dataverse.py \
  --environment dev \
  --name "UpdateInvoiceDetails"
```

Or fetch by GUID:

```bash
python .github/skills/dv-doc-flows/scripts/fetch-flow-from-dataverse.py \
  --environment dev \
  --flow-id FF7B08CD-132F-EF11-8E4F-6045BD5D6396
```

The script writes to `src/dataverse/cloud-flows/<FlowName>/`:

- `<FlowName>-<GUID>.json` — normalized flow JSON for analysis
- `<FlowName>-<GUID>.dataverse.json` — raw Dataverse record for traceability

### Step 2: AI Merge — Apply Staged Output to Wiki Pages

After the script completes, the AI merges staged output into `wiki/Technical-Reference/Cloud-Flows/<FlowName>.md` (index page) and sub-pages under `wiki/Technical-Reference/Cloud-Flows/<FlowName>/`.

---

#### 2a. Gather domain context (do this before writing any files)

Search the following locations for references to this flow's name, trigger entity, or related business process:

1. `wiki/Detailed-Application-Design/*.md` — business domain overviews that reference this flow or its trigger event
2. `wiki/Detailed-Application-Design/**/*.md` — sub-pages within each domain
3. `wiki/Technical-Reference/entities/` — entity pages for Dataverse tables the flow reads or writes
4. `wiki/Technical-Reference/Classic-Workflows/` — classic workflows that may share the same trigger entity or business process

Collect: which business process this flow automates, which entities it touches, who or what initiates it, and any related flows or workflows.

---

#### 2b. Write/update `<FlowName>.md` (index page)

**Auto-generated sections** (replace entirely from `src/dataverse/cloud-flows/<FlowName>/<FlowName>-<GUID>.json`):
- `## Overview` table — flow metadata: `displayName`, trigger type and details, connection references, action/condition/loop counts, complexity rating
- `## Flow Diagram` — embedded PlantUML activity diagram (`![Flow Logic Diagram](./<FlowName>/logic-diagram.png)`)

**AI-written section** (generate fresh on first run; update only if facts changed on re-runs):

Write or update `## Business Analysis` immediately after `## Flow Diagram`:

```markdown
## Business Analysis

### Purpose
{1-3 sentences. What business process does this flow automate in the Income Assistance system?
What problem does it solve, and what happens if it doesn't run?}

### Domain Context
{Which business domain or process this flow belongs to. Reference specific wiki pages.
Example: "Part of the [Invoice Processing](/wiki/Detailed-Application-Design/Finance-and-Payments)
domain — runs when an invoice is approved to trigger payment notifications."}

### Trigger
{What initiates this flow — the trigger type (Dataverse record event, Recurrence, HTTP, etc.),
the entity or schedule, and any filter conditions. Explain the business event that starts it.}

### Key Entities
{Bullet list of the Dataverse tables this flow reads or writes, and what it does with each.
Focus on tables where the flow performs create/update/delete, not just lookups.}

### Related Wiki Pages
{Bullet links to the most relevant Detailed-Application-Design pages found in step 2a.}
```

**Preserved sections** (never overwrite — carry forward exactly as-is from existing page):
- Any `##` heading not listed above (diagrams, implementation notes, known issues, etc.)
- If no existing page: omit preserved sections; write Overview + Flow Diagram + Business Analysis only

---

#### 2c. Write sub-pages (replace entirely — auto-generated, no hand-written content)

| Final path | Source |
|---|---|
| `wiki/Technical-Reference/Cloud-Flows/<FlowName>/logic-diagram.puml` | Generated PlantUML activity diagram (see Step 5) |
| `wiki/Technical-Reference/Cloud-Flows/<FlowName>/logic-diagram.png` | Rendered from `logic-diagram.puml` via `plantuml -tpng` |
| `wiki/Technical-Reference/Cloud-Flows/<FlowName>/code-review.md` | Generated from review heuristics (see Step 6) |
| `wiki/Technical-Reference/Cloud-Flows/<FlowName>/metadata.json` | Extracted flow metadata (see Step 7) |

---

#### 2d. Commit source data

Commit `src/dataverse/cloud-flows/<FlowName>/` to source control — this JSON is the canonical record of what was extracted from Dataverse.

---

### Step 3: Parse Cloud Flow JSON

Use the flow JSON written by the fetch script in Step 1. Parse the flow structure:

**Key JSON Structure:**

```json
{
  "properties": {
    "displayName": "Flow Display Name",
    "connectionReferences": {
      /* connectors used */
    },
    "definition": {
      "triggers": {
        /* when flow runs */
      },
      "actions": {
        /* what flow does */
      }
    }
  }
}
```

**Important Elements:**

- `properties.displayName` - User-friendly flow name
- `properties.definition.triggers` - What initiates the flow (Recurrence, Dataverse trigger, HTTP, etc.)
- `properties.definition.actions` - Flow logic steps (conditions, loops, API calls)
- `properties.connectionReferences` - External connections (Dataverse, SharePoint, etc.)

**Using the Automation Script:**

For faster metadata extraction, use the provided Python script:

```bash
python .github/skills/dv-doc-flows/scripts/extract-flow-metadata.py <flow-json-path> [output-dir]
```

This script automatically:

- Extracts flow name from filename
- Counts actions, conditions, loops recursively
- Calculates nesting depth
- Determines complexity rating
- Maps connector IDs to friendly names
- Captures file system metadata

📘 **See:** [scripts/README.md](scripts/README.md) for detailed script usage.

### Step 4: Extract Flow Name

Extract a clean flow name from the filename for the documentation folder:

**Naming Convention:**

```
Filename: AutomatedEmailAudit-40A14697-75B0-ED11-83FE-0022483BB7EC.json
Flow Name: AutomatedEmailAudit
Index Page: /wiki/Technical-Reference/Cloud-Flows/AutomatedEmailAudit.md
Sub-pages:  /wiki/Technical-Reference/Cloud-Flows/AutomatedEmailAudit/
```

**Rules:**

- Remove GUID suffix (everything after last hyphen before .json)
- Preserve original casing and formatting
- Use flow name from JSON `displayName` if significantly different

### Step 5: Generate `<FlowName>.md`

Create a high-level overview document using the criteria defined in `prompts/README.md`.

**Location:** `/wiki/Technical-Reference/Cloud-Flows/<FlowName>.md`

**Process:**

1. Read the prompt template from `prompts/README.md`
2. Analyze the cloud flow JSON according to the template criteria
3. Generate a PlantUML activity diagram file (`logic-diagram.puml`) visualizing the flow's logic
4. Generate the PNG image from the PlantUML file using: `plantuml -tpng logic-diagram.puml`
5. Generate the `<FlowName>.md` file following the template structure with the diagram embedded as `![Flow Logic Diagram](./<FlowName>/logic-diagram.png)`
6. Save `<FlowName>.md` to the area root (`wiki/Technical-Reference/Cloud-Flows/`); save logic-diagram.puml and logic-diagram.png to the flow's sub-page folder

📘 **See:** [prompts/README.md](prompts/README.md) for the complete evaluation criteria.

### Step 6: Generate `code-review.md`

Create a technical review document using the criteria defined in `prompts/CodeReview.md`.

**Location:** `/wiki/Technical-Reference/Cloud-Flows/<FlowName>/code-review.md`

**Process:**

1. Read the prompt template from `prompts/CodeReview.md`
2. Perform technical analysis of the flow according to the template criteria
3. Generate the `code-review.md` file following the template structure
4. Save to the flow's documentation folder

📘 **See:** [prompts/CodeReview.md](prompts/CodeReview.md) for the complete evaluation criteria.

### Step 7: Generate metadata.json

Create a metadata file containing source information and extracted flow characteristics to help AI understand and evaluate the flow.

**Location:** `/wiki/Technical-Reference/cloud-flows/<FlowName>/metadata.json`

**Process:**

1. Extract key metadata from the flow JSON and file system
2. Generate a JSON file with structured metadata
3. Save to the flow's documentation folder

**Automated Extraction:**

The easiest way to generate metadata is using the provided automation script:

```bash
python .github/skills/dv-doc-flows/scripts/extract-flow-metadata.py <flow-json-path> <output-dir>
```

The script handles all metadata extraction automatically and generates properly formatted JSON.

**Manual Extraction:**

If manual extraction is needed, follow the guidelines in `prompts/Metadata.md`.

📘 **See:** [prompts/Metadata.md](prompts/Metadata.md) for the complete metadata extraction guidelines.
📘 **See:** [scripts/README.md](scripts/README.md) for automation script usage.

**Required Metadata Fields:**

```json
{
  "flowName": "AutomatedEmailAudit",
  "sourceFile": "**/IncomeAssistancePowerAutomate/Workflows/AutomatedEmailAudit-40A14697-75B0-ED11-83FE-0022483BB7EC.json",
  "displayName": "Automated Email Audit",
  "analysisDate": "2026-02-25T16:23:51.151Z",
  "trigger": {
    "type": "Recurrence",
    "details": "Runs every 20 minutes"
  },
  "statistics": {
    "totalActions": 12,
    "totalConditions": 3,
    "totalLoops": 2,
    "nestingDepth": 3,
    "connectionReferences": [
      "shared_commondataserviceforapps",
      "shared_office365"
    ]
  },
  "complexity": {
    "rating": "Medium",
    "factors": [
      "Multiple nested loops",
      "Complex conditions",
      "Multiple connection dependencies"
    ]
  },
  "connectors": [
    {
      "id": "shared_commondataserviceforapps",
      "displayName": "Microsoft Dataverse"
    },
    {
      "id": "shared_office365",
      "displayName": "Office 365 Outlook"
    }
  ],
  "fileInfo": {
    "sizeBytes": 45678,
    "lastModified": "2026-02-20T14:30:00.000Z"
  }
}
```

**Metadata Extraction Guidelines:**

1. **flowName**: Extract from filename (remove GUID suffix)
2. **sourceFile**: Full relative path from repository root
3. **displayName**: From JSON `properties.displayName`
4. **analysisDate**: Current timestamp in ISO 8601 format
5. **trigger.type**: Extract from `properties.definition.triggers` (first trigger's type)
6. **trigger.details**: Human-readable description of trigger conditions
7. **statistics**: Count actions, conditions, loops, and measure nesting depth
8. **complexity.rating**: Simple (1-5 actions) | Medium (6-15 actions) | Complex (16+ actions) | Very Complex (30+ actions or depth > 3)
9. **connectors**: List all connection references with friendly names
10. **fileInfo**: File system metadata (size, last modified)

**Purpose:**

This metadata file enables:

- Quick flow assessment without parsing full JSON
- Batch analysis and reporting
- AI context for faster evaluation
- Historical tracking of flow changes
- Dependency mapping across solutions

### Step 8: Handle Multiple Flows

When analyzing multiple flows:

1. **Sequential Processing:** Analyze flows one at a time to ensure quality
2. **Progress Tracking:** Report progress after each flow is documented
3. **Error Handling:** Skip flows that fail to parse and report errors
4. **Summary:** Provide a summary of all flows analyzed

**Example:**

```
Analyzing 5 flows from IncomeAssistancePowerAutomate...
✓ AutomatedEmailAudit - Documentation generated (AutomatedEmailAudit.md, logic-diagram.puml, logic-diagram.png, code-review.md, metadata.json)
✓ AutomatedLetterCreation - Documentation generated (AutomatedLetterCreation.md, logic-diagram.puml, logic-diagram.png, code-review.md, metadata.json)
✗ InvalidFlow - Skipped (parse error)
✓ AssociateTeamMembers - Documentation generated (AssociateTeamMembers.md, logic-diagram.puml, logic-diagram.png, code-review.md, metadata.json)
✓ AttachSharePointFiles - Documentation generated (AttachSharePointFiles.md, logic-diagram.puml, logic-diagram.png, code-review.md, metadata.json)

Summary: 4 of 5 flows documented successfully
```

## Usage Examples

### Example 1: Analyze a Single Flow

**User Request:** "Analyze the AutomatedEmailAudit cloud flow"

**Steps:**

1. Load `dv-overview` and confirm the environment with `dv-connect`.
2. Run: `python .github/skills/dv-doc-flows/scripts/fetch-flow-from-dataverse.py --environment dev --name "AutomatedEmailAudit"`
3. Read the output JSON from `src/dataverse/cloud-flows/AutomatedEmailAudit/`
4. Extract flow name: "AutomatedEmailAudit"
5. Generate `<FlowName>.md` using `prompts/README.md` criteria
6. Generate logic-diagram.puml with PlantUML activity diagram
7. Generate logic-diagram.png using PlantUML: `plantuml -tpng logic-diagram.puml`
8. Generate `code-review.md` using `prompts/CodeReview.md` criteria
9. Generate metadata.json with extracted metadata
10. Report completion with file paths

### Example 2: Analyze All Flows in a Solution

**User Request:** "Document all Power Automate flows in IncomeAssistancePowerAutomate"

**Steps:**

1. Load `dv-overview` and confirm the environment with `dv-connect`.
2. Run: `python .github/skills/dv-doc-flows/scripts/fetch-flow-from-dataverse.py --environment dev --name-contains ""`
3. For each flow:
   - Read the output JSON
   - Extract flow name and metadata
   - Generate documentation (`<FlowName>.md`, logic-diagram.puml, logic-diagram.png, code-review.md, metadata.json)
   - Track progress
4. Report summary of all flows processed

### Example 3: Update Existing Documentation

**User Request:** "Regenerate the documentation for AutomatedLetterCreation flow"

**Steps:**

1. Load `dv-overview` and confirm the environment with `dv-connect`.
2. Run: `python .github/skills/dv-doc-flows/scripts/fetch-flow-from-dataverse.py --environment dev --name "AutomatedLetterCreation"`
3. Read the output JSON
4. Regenerate logic-diagram.puml and logic-diagram.png
5. Overwrite existing `<FlowName>.md`, `code-review.md`, and metadata.json
6. Report updated files

## Prompt Templates

The evaluation criteria for each documentation type are defined in separate prompt files under `prompts/`:

### prompts/README.md

Defines how to create high-level flow descriptions including:

- Flow purpose and business context
- Trigger conditions
- High-level logic flow
- **PlantUML activity diagram** - Visual representation saved as .puml file and rendered as .png image
- Inputs and outputs
- Dependencies
- Frequency and performance notes
- Business value

### prompts/CodeReview.md

Defines how to perform technical reviews including:

- Code quality assessment
- Performance considerations
- Error handling evaluation
- Security review
- Best practices compliance
- Recommendations for improvement

**Maintaining Criteria:**

To update evaluation criteria, edit the corresponding prompt file in `prompts/`. This makes it easier to refine documentation standards without modifying the core skill logic.

## Output Structure

Each analyzed flow generates a dedicated documentation folder (final wiki output after AI merge):

```
wiki/Technical-Reference/cloud-flows/
├── AutomatedEmailAudit.md
├── AutomatedEmailAudit/
│   ├── logic-diagram.puml
│   ├── logic-diagram.png
│   ├── code-review.md
│   └── metadata.json
├── AutomatedLetterCreation.md
├── AutomatedLetterCreation/
│   ├── logic-diagram.puml
│   ├── logic-diagram.png
│   ├── code-review.md
│   └── metadata.json
├── AssociateTeamMembers.md
└── AssociateTeamMembers/
    ├── logic-diagram.puml
    ├── logic-diagram.png
    ├── code-review.md
    └── metadata.json
```

## Error Handling

**Common Issues:**

1. **File Not Found**
   - Verify solution has been exported and unpacked
   - Check solution name and path
   - Use `find` to locate flow files

2. **Invalid JSON**
   - Report parse errors clearly
   - Skip invalid flows
   - Continue with remaining flows

3. **Missing Documentation Folder**
   - Create `/wiki/Technical-Reference/cloud-flows/` if it doesn't exist
   - Create flow-specific subfolders as needed

4. **Existing Documentation**
   - Ask user whether to overwrite or skip
   - Default behavior: overwrite with confirmation

## Integration with Other Skills

### dataverse-solution-parser

This skill leverages the dataverse-solution-parser skill for:

- Understanding solution structure
- Parsing JSON files
- Extracting metadata

**Usage:**

```
When analyzing flows, invoke the dataverse-solution-parser skill if you need help understanding the JSON structure or extracting specific metadata.
```

### git-commit

After generating documentation, use the git-commit skill to:

- Create conventional commits
- Group related documentation changes
- Generate meaningful commit messages

**Usage:**

```
After documenting multiple flows, use git-commit to commit the changes with a message like:
"docs: add Power Automate flow documentation for AutomatedEmailAudit and AutomatedLetterCreation"
```

## Best Practices

1. **Accuracy:** Ensure flow names match between filename and JSON displayName
2. **Completeness:** Always generate both `<FlowName>.md` and `code-review.md`
3. **Consistency:** Follow the prompt templates exactly for uniform documentation
4. **Context:** Include business context when available (from flow description or comments)
5. **Updates:** When regenerating documentation, preserve any manual edits if requested
6. **Performance:** Process flows sequentially to maintain quality and provide progress updates
