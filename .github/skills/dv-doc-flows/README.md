# Dataverse Analyze Flows Skill

A GitHub Copilot skill for analyzing Power Automate cloud flows from Dynamics 365 Dataverse solutions and generating comprehensive documentation.

## Quick Start

**User invocation examples:**
- "Analyze the AutomatedEmailAudit cloud flow"
- "Document all Power Automate flows in IncomeAssistancePowerAutomate"
- "Review the AutomatedLetterCreation flow"
- "Generate flow documentation for all cloud flows"

**Automatic triggers:**
- User mentions "analyze cloud flow", "document Power Automate", "review flow"
- User references files in `**/*/Workflows/*.json`

## What This Skill Does

1. **Locates** Power Automate cloud flow JSON files in unpacked Dataverse solutions
2. **Parses** flow definition JSON to extract triggers, actions, connections, and logic
3. **Generates** documentation files per flow:
   - **README.md** - Business-focused overview with embedded diagram
   - **logic-diagram.puml** - PlantUML source code for flow visualization
   - **logic-diagram.png** - Generated PNG image from PlantUML diagram
   - **CodeReview.md** - Technical analysis with recommendations
   - **metadata.json** - Source file reference and extracted flow metadata
4. **Outputs** documentation to `/wiki/Technical-Reference/cloud-flows/<FlowName>/`

## Skill Structure

```
dv-doc-flows/
├── SKILL.md                          # Main skill definition (instructions for AI)
├── prompts/                          # Evaluation criteria templates
│   ├── README.md                # How to generate README.md
│   ├── CodeReview.md                 # How to generate CodeReview.md
│   ├── Metadata.md                   # How to generate metadata.json
│   └── flow.puml-block.txt    # PlantUML template for diagrams
├── references/                       # Supporting documentation
│   ├── README.md                     # Power Automate structure reference
│   └── flow-analysis-guide.md        # Common issues & best practices
└── scripts/                          # (Reserved for future automation scripts)
```

## Key Features

### Separated Evaluation Criteria
Evaluation logic is **separated from the main skill** into prompt templates:
- **prompts/README.md** - Defines structure and criteria for business documentation
- **prompts/CodeReview.md** - Defines structure and criteria for technical review
- **prompts/Metadata.md** - Defines metadata extraction and JSON structure
- **metadata.json** - Structured data file with source reference and extracted flow characteristics

**Benefits:**
- Easy to update evaluation criteria without touching core skill logic
- Version control for documentation standards
- Clear separation between "how to analyze" and "what to document"
- Machine-readable metadata enables batch processing and AI-assisted analysis

### Comprehensive Technical Analysis
The CodeReview includes:
- Architecture & design assessment
- Performance analysis (N+1 queries, pagination, concurrency)
- Error handling evaluation
- Security review
- Code quality & maintainability
- Best practices compliance checklist
- Prioritized, actionable recommendations

### Business-Focused Descriptions
The Description includes:
- Flow purpose and business context
- Trigger conditions and schedule
- High-level logic (what it does, not how)
- **PlantUML activity diagram** - Separate .puml file and rendered .png image
- Inputs and outputs
- Dependencies
- Frequency and performance notes
- Business value and impact

## Maintaining This Skill

### Automation Scripts

The `scripts/` directory contains automation tools:

- **extract-flow-metadata.py** - Python script to extract metadata from flow JSON files
  - No external dependencies (uses Python standard library)
  - Handles recursive action counting and complexity calculation
  - Maps connector IDs to friendly display names
  - Can be run by AI during flow analysis workflow

**Usage:**
```bash
# Extract metadata for a single flow
python .github/skills/dv-doc-flows/scripts/extract-flow-metadata.py <flow-json-path>

# Process all flows in a solution
for file in **/IncomeAssistancePowerAutomate/Workflows/*.json; do
    python .github/skills/dv-doc-flows/scripts/extract-flow-metadata.py "$file"
done
```

📘 **See:** [scripts/README.md](scripts/README.md) for detailed documentation.

### Updating Documentation Standards

To change how flows are documented:

1. **For business documentation changes:**
   - Edit `prompts/README.md`
   - Update section structure, tone, or content requirements
   - AI will automatically follow the new template

2. **For technical review changes:**
   - Edit `prompts/CodeReview.md`
   - Add/remove evaluation criteria
   - Update rating scales or metrics
   - AI will automatically follow the new template

### Adding New Analysis Types

To add a new documentation type (e.g., "SecurityAudit.md"):

1. Create `prompts/SecurityAudit.md` with evaluation criteria
2. Update `SKILL.md` to reference the new analysis type
3. Add workflow step for generating the new document

### Updating Reference Material

To improve flow analysis accuracy:

1. Add common patterns to `references/flow-analysis-guide.md`
2. Update JSON structure examples in `references/README.md`
3. Document new anti-patterns or best practices as they're discovered

## Example Usage

### Single Flow Analysis (with automation script)
```
User: "Analyze the AutomatedEmailAudit flow"

AI Process:
1. Locates **/*/Workflows/*AutomatedEmailAudit*.json
2. Runs extract-flow-metadata.py script to generate metadata.json
3. Parses JSON structure using metadata
4. Reads prompts/README.md criteria
5. Creates logic-diagram.puml with PlantUML activity diagram
6. Generates logic-diagram.png using: plantuml -tpng logic-diagram.puml
7. Generates /wiki/Technical-Reference/cloud-flows/AutomatedEmailAudit/README.md (with embedded diagram)
8. Reads prompts/CodeReview.md criteria
9. Generates /wiki/Technical-Reference/cloud-flows/AutomatedEmailAudit/CodeReview.md
10. Reports completion (metadata.json already created in step 2)
```

### Single Flow Analysis (manual extraction)
```
User: "Analyze the AutomatedEmailAudit flow"

AI Process:
1. Locates **/*/Workflows/*AutomatedEmailAudit*.json
2. Parses JSON structure manually
3. Reads prompts/README.md criteria
4. Creates logic-diagram.puml with PlantUML activity diagram
5. Generates logic-diagram.png using: plantuml -tpng logic-diagram.puml
6. Generates /wiki/Technical-Reference/cloud-flows/AutomatedEmailAudit/README.md (with embedded diagram)
7. Reads prompts/CodeReview.md criteria
8. Generates /wiki/Technical-Reference/cloud-flows/AutomatedEmailAudit/CodeReview.md
9. Extracts metadata manually and generates /wiki/Technical-Reference/cloud-flows/AutomatedEmailAudit/metadata.json
10. Reports completion
```

### Bulk Flow Analysis
```
User: "Document all flows in IncomeAssistancePowerAutomate"

AI Process:
1. Finds all JSON files in **/IncomeAssistancePowerAutomate/Workflows/
2. For each flow:
   - Run extract-flow-metadata.py to generate metadata.json (fast)
   - Parse JSON using generated metadata
   - Create logic-diagram.puml with PlantUML activity diagram
   - Generate logic-diagram.png using: plantuml -tpng logic-diagram.puml
   - Generate README.md (with embedded diagram reference)
   - Generate CodeReview.md
   - Track progress
3. Report summary (e.g., "Documented 15 of 16 flows successfully")
```

## Integration with Other Skills

- **dataverse-solution-parser**: Used to understand Dataverse solution structure
- **plantuml**: Used for generating flowchart diagrams as PlantUML files and images embedded in descriptions
- **git-commit**: Use after documentation generation for conventional commits
- **doc-coauthoring**: Can help structure complex documentation

## Output Structure

```
/wiki/Technical-Reference/cloud-flows/
├── AutomatedEmailAudit/
│   ├── README.md       # Business overview with embedded diagram
│   ├── logic-diagram.puml   # PlantUML source code
│   ├── logic-diagram.png    # Generated diagram image
│   ├── CodeReview.md        # Technical review
│   └── metadata.json        # Source file reference and flow metadata
├── AutomatedLetterCreation/
│   ├── README.md
│   ├── logic-diagram.puml
│   ├── logic-diagram.png
│   ├── CodeReview.md
│   └── metadata.json
└── AssociateTeamMembers/
    ├── README.md
    ├── logic-diagram.puml
    ├── logic-diagram.png
    ├── CodeReview.md
    └── metadata.json
```
    ├── CodeReview.md
    └── metadata.json
```

### metadata.json Structure

Each flow's metadata.json contains:

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
    "connectionReferences": ["shared_commondataserviceforapps", "shared_office365"]
  },
  "complexity": {
    "rating": "Medium",
    "factors": ["Multiple nested loops", "Complex conditions", "Multiple connection dependencies"]
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

**Metadata Benefits:**
- Quick flow assessment without parsing full JSON
- Batch analysis and reporting capabilities
- Enhanced AI context for faster evaluation
- Historical tracking of flow changes over time
- Dependency mapping across solutions

## Common Issues & Solutions

### Issue: Flow Name Unclear
**Solution:** Use filename without GUID, or extract from JSON displayName

### Issue: Complex Flow Too Large
**Solution:** AI will generate complete documentation but may need multiple iterations

### Issue: Invalid JSON
**Solution:** AI will report parse error and skip to next flow

### Issue: Missing Business Context
**Solution:** AI will infer from flow structure and clearly mark assumptions

## Best Practices for Maintainers

1. **Keep prompts focused**: Each prompt file should have a single, clear purpose
2. **Use examples**: Include concrete examples in prompt files (done)
3. **Version control standards**: Track changes to evaluation criteria over time
4. **Review generated docs**: Periodically review AI-generated documentation for quality
5. **Update anti-patterns**: Add newly discovered issues to flow-analysis-guide.md
6. **Document assumptions**: When criteria are subjective, document the reasoning

## Roadmap / Future Enhancements

Potential additions:
- **PerformanceMetrics.md** - Quantitative performance analysis with benchmarks
- **SecurityAudit.md** - Dedicated security-focused review
- **ComplianceCheck.md** - Regulatory compliance assessment
- **TestPlan.md** - Suggested test cases based on flow logic
- **Enhanced metadata.json** - Add dependency graph, version history, change tracking
- Automation scripts to run bulk analysis via CLI
- Integration with CI/CD pipelines for automated flow documentation

## Contributing

When updating this skill:
1. Test changes with representative flows
2. Update this README if structure changes
3. Keep prompts and references in sync with SKILL.md
4. Document any new conventions or patterns

## Version History

- **v1.1** (2026-02-25): Added metadata.json generation with source file reference and flow statistics
- **v1.0** (2026-02-25): Initial skill creation with Description and CodeReview prompts
