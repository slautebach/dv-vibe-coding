# Metadata.json Specification & Reference

This document defines the structure and meaning of metadata.json files generated for Power Automate cloud flows.

> **Automated Extraction:** Metadata is automatically extracted using `scripts/extract-flow-metadata.py`. 
> This document serves as:
> - The specification that the automation script implements
> - A reference for AI to understand metadata fields when reading them
> - A fallback guide if the script cannot be used (manual extraction)
> - Documentation for extending the metadata structure

## Overview

The metadata.json file provides structured data that helps AI quickly understand and evaluate cloud flows without parsing the full flow JSON. It includes source file reference, complexity metrics, trigger information, connector dependencies, and file system metadata.

## JSON Structure

The metadata.json file should be a valid JSON object with the following structure:

```json
{
  "flowName": "string",
  "sourceFile": "string",
  "displayName": "string",
  "analysisDate": "ISO 8601 timestamp",
  "trigger": {
    "type": "string",
    "details": "string"
  },
  "statistics": {
    "totalActions": number,
    "totalConditions": number,
    "totalLoops": number,
    "nestingDepth": number,
    "connectionReferences": ["string"]
  },
  "complexity": {
    "rating": "Simple|Medium|Complex|Very Complex",
    "factors": ["string"]
  },
  "connectors": [
    {
      "id": "string",
      "displayName": "string"
    }
  ],
  "fileInfo": {
    "sizeBytes": number,
    "lastModified": "ISO 8601 timestamp"
  }
}
```

## Field Extraction Guidelines

### flowName (required)
**Source:** Filename without GUID suffix  
**Processing:**
1. Take the filename (e.g., `AutomatedEmailAudit-40A14697-75B0-ED11-83FE-0022483BB7EC.json`)
2. Remove the GUID portion and extension (everything after the last meaningful hyphen)
3. Result: `AutomatedEmailAudit`

**Example:**
```json
"flowName": "AutomatedEmailAudit"
```

### sourceFile (required)
**Source:** Full file path relative to repository root  
**Format:** Should be a relative path that can be used to locate the original JSON file

**Example:**
```json
"sourceFile": "**/IncomeAssistancePowerAutomate/Workflows/AutomatedEmailAudit-40A14697-75B0-ED11-83FE-0022483BB7EC.json"
```

### displayName (required)
**Source:** JSON path `properties.displayName`  
**Fallback:** Use flowName if displayName is not available

**Example:**
```json
"displayName": "Automated Email Audit"
```

### analysisDate (required)
**Source:** Current timestamp when analysis is performed  
**Format:** ISO 8601 format (YYYY-MM-DDTHH:mm:ss.sssZ)

**Example:**
```json
"analysisDate": "2026-02-25T16:23:51.151Z"
```

### trigger (required)
Extract information about what initiates the flow.

#### trigger.type
**Source:** JSON path `properties.definition.triggers[*].type`  
**Common Values:**
- `Recurrence` - Scheduled flow
- `ApiConnection` - Dataverse/SharePoint/etc. trigger
- `Request` - HTTP request trigger
- `manual` - Manual/instant flow

**Example:**
```json
"trigger": {
  "type": "Recurrence",
  "details": "Runs every 20 minutes"
}
```

#### trigger.details
**Source:** Analyze trigger configuration to create human-readable description  
**Guidelines:**
- For Recurrence: Include frequency (e.g., "Runs every 20 minutes", "Daily at 9:00 AM")
- For ApiConnection: Include entity and operation (e.g., "When a record is created or updated: Account")
- For Request: Include method and path if available
- For manual: "Manually triggered by user"

### statistics (required)
Count flow elements to provide quantitative complexity metrics.

#### totalActions
**Source:** Count all actions in `properties.definition.actions`  
**Includes:** All action types (conditions, loops, API calls, compose, etc.)  
**Excludes:** Trigger (counted separately)

#### totalConditions
**Source:** Count actions with type `If` or `Switch`

#### totalLoops
**Source:** Count actions with type `Foreach` or `Until`

#### nestingDepth
**Source:** Calculate maximum nesting level of actions  
**Calculation:** 
- Top-level actions = depth 1
- Actions inside a condition or loop = depth 2
- Actions inside nested structures = depth 3+

**Example:**
```json
"statistics": {
  "totalActions": 12,
  "totalConditions": 3,
  "totalLoops": 2,
  "nestingDepth": 3,
  "connectionReferences": ["shared_commondataserviceforapps", "shared_office365"]
}
```

#### connectionReferences
**Source:** Extract keys from `properties.connectionReferences` object  
**Format:** Array of connection reference IDs

### complexity (required)
Provide an overall complexity assessment.

#### complexity.rating
**Source:** Calculate based on statistics  
**Algorithm:**
```
Simple: totalActions <= 5 AND nestingDepth <= 2
Medium: totalActions 6-15 OR nestingDepth == 3
Complex: totalActions 16-30 OR nestingDepth == 4
Very Complex: totalActions > 30 OR nestingDepth > 4
```

#### complexity.factors
**Source:** List key factors that contribute to complexity  
**Common Factors:**
- "Multiple nested loops"
- "Complex conditions with multiple branches"
- "High action count (30+ actions)"
- "Deep nesting (4+ levels)"
- "Multiple connection dependencies"
- "Large data operations"
- "Complex expressions or formulas"

**Example:**
```json
"complexity": {
  "rating": "Medium",
  "factors": [
    "Multiple nested loops",
    "Complex conditions",
    "Multiple connection dependencies"
  ]
}
```

### connectors (required)
List all external connections used by the flow.

**Source:** `properties.connectionReferences` object  
**Processing:**
1. Extract each connection reference
2. Map connection ID to friendly display name
3. Include both technical ID and human-readable name

**Common Connector Mappings:**
- `shared_commondataserviceforapps` → "Microsoft Dataverse"
- `shared_office365` → "Office 365 Outlook"
- `shared_sharepointonline` → "SharePoint"
- `shared_teams` → "Microsoft Teams"
- `shared_approvals` → "Approvals"
- `shared_onedriveforbusiness` → "OneDrive for Business"

**Example:**
```json
"connectors": [
  {
    "id": "shared_commondataserviceforapps",
    "displayName": "Microsoft Dataverse"
  },
  {
    "id": "shared_office365",
    "displayName": "Office 365 Outlook"
  }
]
```

### fileInfo (required)
Capture file system metadata.

#### sizeBytes
**Source:** File size in bytes from file system  
**Type:** Integer

#### lastModified
**Source:** File modification timestamp from file system  
**Format:** ISO 8601 format

**Example:**
```json
"fileInfo": {
  "sizeBytes": 45678,
  "lastModified": "2026-02-20T14:30:00.000Z"
}
```

## Usage by AI

This metadata enables AI to:

1. **Quick Assessment:** Understand flow complexity without parsing full JSON
2. **Batch Processing:** Compare and analyze multiple flows efficiently
3. **Dependency Analysis:** Track which connectors are used across flows
4. **Change Detection:** Identify when flows have been modified
5. **Context Loading:** Provide relevant context for code review and description generation
6. **Historical Tracking:** Monitor flow evolution over time
7. **Risk Assessment:** Flag high-complexity flows for detailed review

## Automated vs Manual Extraction

### Automated (Recommended)

Use the automation script for fast, accurate metadata extraction:

```bash
python .github/skills/dv-doc-flows/scripts/extract-flow-metadata.py <flow-json-path> [output-dir]
```

The script automatically handles:
- Recursive action counting
- Nesting depth calculation
- Complexity rating
- Connector name mapping
- File system metadata

### Manual (Fallback)

If the automation script cannot be used (permissions, Python unavailable, etc.), follow the field extraction guidelines below to manually create metadata.json.

## Example Complete Metadata File

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

## Error Handling (Manual Extraction Only)

When manually extracting metadata, if any field cannot be extracted:

1. **Required Fields:** Use sensible defaults
   - `flowName`: Use filename without extension
   - `displayName`: Use flowName
   - `trigger.type`: "Unknown"
   - Empty arrays for lists
   - `0` for numeric values
   
2. **Optional Fields:** Omit if not available

3. **Invalid Data:** Log warning but continue with best-effort extraction

## Best Practices

1. **Prefer Automated Extraction:** Use `scripts/extract-flow-metadata.py` for accuracy and speed
2. **Accuracy:** Ensure all extracted data is accurate and reflects the actual flow
3. **Consistency:** Use consistent formatting and naming across all metadata files
4. **Completeness:** Populate all fields whenever possible
5. **Validation:** Ensure generated JSON is valid and parseable
6. **Timestamps:** Always use ISO 8601 format for timestamps
7. **Relative Paths:** Use repository-relative paths for sourceFile to ensure portability

## Extending the Metadata

To add new metadata fields:

1. Update this specification document with the new field definition
2. Update `scripts/extract-flow-metadata.py` to extract the new field
3. Update `scripts/README.md` to document the change
4. Test with representative flows
5. Update version history in main README.md
