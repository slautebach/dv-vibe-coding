---
name: dv-entity
description: Create and manage Dataverse entities (tables) and attributes in Dynamics 365 / Dataverse, enforcing MNP naming standards and best practices. Use when asked to "create a table", "add an attribute", "scaffold an entity", "review attribute names", "create a Dataverse table", "add fields to a table", or "create a lookup/datetime/currency/boolean field". Resolves the project publisher prefix automatically from Solution.xml, config, or --prefix flag (falls back to `mnp`). Do NOT use for documenting existing entities (use dv-doc-entity skill) or for reading entity metadata.
---

# Dataverse Entity & Attribute Manager

Creates and manages Dataverse tables and attributes, enforcing MNP naming standards. Stages proposed changes for review before applying to Dataverse.

## Dataverse Skills Dependency

Requires the Dataverse-skills plugin for live operations:

```bash
copilot plugin marketplace add microsoft/Dataverse-skills
copilot plugin install dataverse@dataverse-skills
```

Before any live write operation:
1. Load `dv-overview`
2. Use `dv-connect` to select the target environment and confirm auth context

**Authentication:** Uses `dataverse_sdk_client.py` (from `dataverse@dataverse-skills`). Browser popup by default; tokens cached in OS credential store. Set `CLIENT_ID` + `CLIENT_SECRET` in `.env` for service principal auth.

## Core Workflow

### Step 1: Resolve Publisher Prefix

Resolve the prefix using this waterfall — stop at first success:

1. `--prefix` flag in the user's request (e.g., "use the grants prefix")
2. `Solution.xml` `<Publisher><UniqueName>` — search `StarterKits/{kit}/Solutions/**/Other/Solution.xml`
3. `.env` or `config.json` `PUBLISHER_PREFIX`
4. Fallback: `mnp` (warn the user)

See [references/prefix-resolution.md](references/prefix-resolution.md) for code examples and the full algorithm.

### Step 2: Validate Naming

Before generating any output, validate all proposed names against MNP standards.

**Tables:**
- Logical name: `{prefix}_{genericterm}` — generic and reusable, NOT project-specific
- Description: required
- Ownership: User or Team (default); Organization for reference tables only
- Auditing: always ON

**Attributes — naming by type:**
| Type | Pattern | Example |
|---|---|---|
| General | `{prefix}_{field}` | `mnp_name` |
| Lookup | `{prefix}_{relatedtable}id` | `mnp_contactid` |
| Lookup (context) | `{prefix}_{context}{relatedtable}id` | `mnp_billingaccountid` |
| Lookup to SystemUser | `{prefix}_{action}by` | `mnp_approvedby` |
| DateTime | `{prefix}_{action}on` | `mnp_submittedon` |
| Currency | `{prefix}_{field}amount` | `mnp_grantamount` |
| Boolean | `{prefix}_is{field}` | `mnp_isapproved` |
| Grouped | `{prefix}_{tag}_{field}` | `mnp_loan_amount` |

**Violations to catch and correct:**
- Table name repeated in attribute name: `mnp_applicationstatus` on `mnp_application` table -> `mnp_status`
- Missing type suffix: `mnp_grant` for currency -> `mnp_grantamount`
- Behaviour suffix: `mnp_amount_calc` -> `mnp_amount`
- Local option set proposed -> warn to use global option set instead
- No description provided -> require before proceeding

See [references/table-attribute-standards.md](references/table-attribute-standards.md) for the full standards.
See [references/date-time-standards.md](references/date-time-standards.md) for DateTime behavior selection (User Local / Date Only / Time-Zone Independent).

### Step 3: Stage Proposed Changes

Write proposed definitions to `src/dataverse/entity-authoring/` for user review before applying:

```
src/dataverse/
  entity-authoring/
    {entity-logical-name}/
      entity.json          # EntityDefinitions POST body
      attributes/
        {attr-logical-name}.json   # Attribute POST body per field
      summary.md           # Human-readable review table
```

Always write `summary.md` as a human-readable table:

```markdown
## Proposed: mnp_application

| Property | Value |
|---|---|
| Logical Name | mnp_application |
| Display Name | Application |
| Description | Tracks grant applications submitted by clients. |
| Ownership | User or Team |
| Auditing | ON |

### Attributes

| Logical Name | Type | Display Name | Notes |
|---|---|---|---|
| mnp_contactid | Lookup (contact) | Contact | |
| mnp_submittedon | DateTime (User Local) | Submitted On | |
| mnp_grantamount | Currency | Grant Amount | |
| mnp_isapproved | Boolean | Is Approved | |
```

Present the summary table to the user and ask for confirmation before applying.

### Step 4: Apply to Dataverse

Only after user confirms staged changes, apply via Web API using `.github/scripts/dataverse_client.py`:

```python
from dataverse_client import DataverseClient

client = DataverseClient()   # inherits auth context from dv-connect

# Create entity
response = client.post('EntityDefinitions', entity_payload)
entity_id = response['MetadataId']

# Add to solution
client.post('AddSolutionComponent', {
    "ComponentId": entity_id,
    "ComponentType": 1,
    "SolutionUniqueName": solution_unique_name,
    "AddRequiredComponents": True
})

# Add attributes
for attr_payload in attribute_payloads:
    client.post(f'EntityDefinitions({entity_id})/Attributes', attr_payload)
```

See [references/web-api-metadata.md](references/web-api-metadata.md) for complete JSON payload examples for each attribute type.

### Step 5: Output Summary

After applying, output a wiki-ready summary table in ADO wiki format:

```markdown
## mnp_application — Created

| Property | Value |
|---|---|
| Logical Name | mnp_application |
| Schema Name | mnp_Application |
| Display Name | Application |
| Ownership | UserOwned |
| Auditing | ON |

### Attributes Added

| Logical Name | Type | Display Name | Required |
|---|---|---|---|
| mnp_contactid | Lookup (contact) | Contact | No |
| mnp_submittedon | DateTime (User Local) | Submitted On | No |
```

## Naming Review Mode

When asked to "review these attribute names" or "check naming standards", run validation only — no creation:

1. List each name with PASS / FAIL status
2. For each FAIL, provide the corrected name and the violated rule
3. Do not stage or create anything

## Example Prompts

- "Create a new Dataverse table called Application with a lookup to Contact and a status global option set"
- "Add a loan amount, start date, and term in months to the loanrequest table"
- "Review these attribute names and flag any that violate naming standards"
- "Create a Payment table for the Grants solution — use the grants prefix"
- "Scaffold an Application entity with fields for contact, submitted date, and approved amount"

## Reference Files

| File | When to read |
|---|---|
| [references/table-attribute-standards.md](references/table-attribute-standards.md) | Always — contains the full MNP naming standards and validation checklist |
| [references/date-time-standards.md](references/date-time-standards.md) | When creating DateTime attributes — behavior selection guide |
| [references/prefix-resolution.md](references/prefix-resolution.md) | When resolving the publisher prefix — full algorithm with code examples |
| [references/web-api-metadata.md](references/web-api-metadata.md) | When building API payloads — JSON body examples for each attribute type |

