# Dataverse Analyze Flows - Scripts

Automation scripts for analyzing Power Automate cloud flows.

## extract-flow-metadata.py

Python script to extract metadata from Power Automate flow JSON files and generate metadata.json.

### Requirements

- Python 3.7+
- No external dependencies (uses standard library only)

### Usage

```bash
# Basic usage - outputs to wiki/Technical-Reference/cloud-flows/<FlowName>/
python extract-flow-metadata.py <path-to-flow-json>

# Specify custom output directory
python extract-flow-metadata.py <path-to-flow-json> <output-directory>
```

### Examples

```bash
# Analyze a single flow
python extract-flow-metadata.py **/IncomeAssistancePowerAutomate/Workflows/AutomatedEmailAudit-40A14697-75B0-ED11-83FE-0022483BB7EC.json

# Specify custom output directory
python extract-flow-metadata.py **/IncomeAssistancePowerAutomate/Workflows/AutomatedEmailAudit-*.json ./output/

# Process all flows in a solution (using bash loop)
for file in **/IncomeAssistancePowerAutomate/Workflows/*.json; do
    python extract-flow-metadata.py "$file"
done
```

### Output

The script generates a `metadata.json` file in the specified output directory with the following structure:

```json
{
  "flowName": "AutomatedEmailAudit",
  "sourceFile": "**/...",
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
    "connectionReferences": [...]
  },
  "complexity": {
    "rating": "Medium",
    "factors": [...]
  },
  "connectors": [...],
  "fileInfo": {
    "sizeBytes": 45678,
    "lastModified": "2026-02-20T14:30:00.000Z"
  }
}
```

### Features

- **Flow Name Extraction**: Automatically removes GUID suffix from filename
- **Recursive Analysis**: Counts actions, conditions, and loops including nested structures
- **Nesting Depth Calculation**: Measures maximum nesting depth for complexity analysis
- **Complexity Rating**: Automatically rates flow as Simple, Medium, Complex, or Very Complex
- **Trigger Analysis**: Extracts and describes trigger type and configuration
- **Connector Mapping**: Maps connection IDs to friendly display names
- **File System Metadata**: Includes file size and last modified timestamp

### Complexity Ratings

The script calculates complexity based on multiple factors:

- **Simple**: ≤5 actions AND ≤2 nesting levels
- **Medium**: 6-15 actions OR 3 nesting levels
- **Complex**: 16-30 actions OR 4 nesting levels
- **Very Complex**: >30 actions OR >4 nesting levels

### Error Handling

- Invalid JSON files are caught and reported
- Missing files return error code 1
- Stack traces provided for debugging

### Integration with AI Workflow

When the AI analyzes flows using the `dv-doc-flows` skill, it can:

1. Locate flow JSON files
2. Run this script to extract metadata
3. Use the metadata to inform README.md and CodeReview.md generation
4. Save all three files together in the documentation folder

### Connector Mappings

The script includes mappings for common connectors:

- Microsoft Dataverse
- Office 365 Outlook
- SharePoint
- Microsoft Teams
- Approvals
- OneDrive for Business
- SQL Server
- Azure services (Blob, Queue, Table, Service Bus, Key Vault)
- Popular SaaS (SendGrid, Twilio, Slack, etc.)

Unknown connectors are formatted from their technical ID (e.g., `shared_custom_api` → `Custom Api`).

## find-solution-flows.py

Python script to search D365 solution folders for Power Automate cloud flow JSON files and display a summary table.

### Requirements

- Python 3.7+
- No external dependencies (uses standard library only)

### Usage

```bash
# List all flows across all solutions
python find-solution-flows.py

# List flows in a specific solution
python find-solution-flows.py IncomeAssistancePowerAutomate

# Filter flows by name (case-insensitive substring)
python find-solution-flows.py --filter "CreateTask"

# Search from a custom repository root
python find-solution-flows.py --root C:/dev/myproject

# Output as JSON for scripting or AI consumption
python find-solution-flows.py --json

# Discover flows and extract metadata for each
python find-solution-flows.py IncomeAssistancePowerAutomate --extract
```

### Output

The default table output includes flow name, solution, trigger type, top-level action count, and file size:

```
Found 154 cloud flow(s)

Flow Name                       Solution                        Trigger      Actions  Size(KB)
-----------------------------------------------------------------------------------------------
AutomatedEmailAudit             IncomeAssistancePowerAutomate   Scheduled         12      45.7
CreateTask-OnDemand             IncomeAssistancePowerAutomate   Automated         14      18.9
...

By solution:
  IncomeAssistancePowerAutomate: 117 flow(s)
  IncomeAssistancePowerAutomateUnmanaged: 33 flow(s)
  MNPPowerTools: 3 flow(s)
  IncomeAssistanceDataCleanupPhase2: 1 flow(s)
```

With `--json`, each flow entry includes:

```json
{
  "flowName": "CreateTask-OnDemand",
  "solution": "IncomeAssistancePowerAutomate",
  "trigger": "Automated",
  "topLevelActions": 14,
  "fileSizeKb": 18.9,
  "filePath": "C:/dev/.../Workflows/CreateTask-OnDemand-<GUID>.json"
}
```

### Features

- **Cloud Flow Detection**: Only returns Power Automate cloud flows (JSON with `properties.definition.triggers`), skipping classic workflows
- **GUID Stripping**: Removes GUID suffix from filenames to produce clean flow names
- **Trigger Classification**: Categorises triggers as Scheduled, Automated, HTTP/Manual, or Manual
- **Solution Grouping**: Summary count by solution when searching all solutions
- **Name Filtering**: `--filter` flag for quick substring search across flow names
- **Metadata Extraction**: `--extract` flag chains into `extract-flow-metadata.py` for each discovered flow
- **JSON Output**: `--json` flag for machine-readable output suitable for scripting or AI prompts

### Integration with AI Workflow

When the AI analyzes flows using the `dv-doc-flows` skill, it can:

1. Run this script to discover all flows in a solution
2. Use the output to select which flow(s) to document
3. Use `filePath` values to locate the JSON for deeper analysis
4. Optionally pass `--extract` to generate `metadata.json` files for all flows at once

## Future Scripts

Potential additions:

- **compare-flows.py**: Compare metadata between two flow versions
- **generate-report.py**: Create summary report of all flows
- **validate-metadata.py**: Validate existing metadata.json files
- **export-catalog.py**: Export flow catalog to CSV/Excel

## Contributing

When adding new scripts:

1. Use Python 3.7+ standard library when possible
2. Include clear docstrings and help text
3. Follow the same error handling patterns
4. Update this README with usage examples
5. Make scripts executable with `chmod +x`
