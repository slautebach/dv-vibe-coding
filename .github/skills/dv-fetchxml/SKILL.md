---
name: dv-fetchxml
description: Write, validate, execute, and optimize FetchXML queries for Dynamics 365 / Dataverse. Validates entity and attribute names against live Dataverse metadata before authoring. Executes queries against the target environment and previews results. Use when asked to "write a FetchXML", "build a query", "create a FetchXML query", "run a FetchXML", "convert FetchXML to OData", or "optimize a FetchXML query". Requires dataverse@dataverse-skills for live metadata validation and execution.
---

# dv-fetchxml

Write, validate, execute, and optimize FetchXML queries for Dynamics 365 / Dataverse.

## Setup

1. Install the Dataverse plugin (once per environment):
   ```
   copilot plugin marketplace add microsoft/Dataverse-skills
   copilot plugin install dataverse@dataverse-skills
   ```
2. Load `dv-overview` for environment context.
3. Run `dv-connect` to select the target environment and confirm auth context.
4. All API calls use `.github/scripts/dataverse_client.py`, which inherits the auth context established by `dv-connect`. Set `CLIENT_ID` + `CLIENT_SECRET` in `.env` for service principal auth.

## Core Workflow

### Step 1 -- Resolve Entity
Validate the entity logical name against live metadata:
```python
meta = client.get_entity_metadata('mnp_payment')
entity_set = meta['EntitySetName']  # needed for execution
```
If not found, list candidate entities and ask the user to confirm.

### Step 2 -- Validate Attributes
Fetch and validate every attribute name used in the query:
```python
attrs = client.get_entity_attributes('mnp_payment')
attr_names = {a['LogicalName'] for a in attrs}
# Warn on any name not in attr_names
```
For link-entity joins, validate attributes on the related entity too.

### Step 3 -- Validate Relationships (joins)
For each `link-entity`, verify the `from`/`to` column names exist on their respective entities. For named schema names, use:
```
GET /api/data/v9.2/RelationshipDefinitions?$filter=SchemaName eq '{schema}'
```

### Step 4 -- Warn Before Generating
If any entity or attribute could not be confirmed, report clearly:
> !! Could not validate: `mnp_paymentstatus` on `mnp_payment`. Proceeding may produce a runtime error.

Only proceed after warning; never silently drop unvalidated names.

### Step 5 -- Generate FetchXML
Produce well-formed XML. See [fetchxml-reference.md](references/fetchxml-reference.md) for all elements and common patterns.

Key rules:
- Always include `top` or `count`+`page` -- never unbounded queries on large tables.
- Prefer specific `<attribute>` elements over `<all-attributes>`.
- Always add an `<order>` when paging; include the primary key as a tiebreaker.
- Use `alias` on every aggregate attribute.

### Step 6 -- Execute and Preview
```python
results = client.get_records_with_fetchxml(entity_set, fetch_xml)
records = results.get('value', [])
```
Display: row count + first 10 records as a markdown table. If results are paginated, report total pages retrieved.

### Step 7 -- Report Performance
After execution, flag any issues found. See [performance-guidance.md](references/performance-guidance.md) for anti-patterns and optimizations.

## Reference Files

| File | When to Read |
|------|-------------|
| [references/fetchxml-reference.md](references/fetchxml-reference.md) | All element/attribute syntax, common query patterns |
| [references/performance-guidance.md](references/performance-guidance.md) | Reviewing queries for anti-patterns; optimization advice |
| [references/metadata-api-endpoints.md](references/metadata-api-endpoints.md) | Raw endpoint shapes for metadata validation beyond `dataverse_client.py` |
| [references/odata-conversion.md](references/odata-conversion.md) | Converting FetchXML to OData for canvas apps |

## OData Conversion

When the user asks to convert FetchXML to OData, read [references/odata-conversion.md](references/odata-conversion.md) for the operator mapping and known OData limitations.

## Example Prompts

- "Write a FetchXML to get active applications from the last 30 days with contact name -- then run it against dev"
- "Build a FetchXML for `mnp_payment` grouped by status with total amount sum, validate attribute names first"
- "Convert this FetchXML to an OData query for a canvas app"
- "Review this FetchXML for performance issues and show me the record count"
