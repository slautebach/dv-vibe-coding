# Dataverse Metadata API Endpoints

Source: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/

Use these endpoints for metadata validation. The `dataverse_client.py` wrapper methods are preferred where they exist.

[[_TOC_]]

## Base URI

```
{environment_url}/api/data/v9.2/
```

All requests require:
```
Authorization: Bearer {token}
OData-MaxVersion: 4.0
OData-Version: 4.0
Accept: application/json
```

---

## Entity Metadata

### Validate an Entity by Logical Name

```
GET /api/data/v9.2/EntityDefinitions?$filter=LogicalName eq '{entity}'&$select=LogicalName,EntitySetName,DisplayName,PrimaryIdAttribute,PrimaryNameAttribute
```

**Python (dataverse_client.py):**
```python
meta = client.get_entity_metadata('mnp_payment')
# meta['LogicalName']    -> 'mnp_payment'
# meta['EntitySetName']  -> 'mnp_payments'  (use for execution URL)
# meta['PrimaryIdAttribute']
```

**Response fields to capture:**
- `MetadataId` — required for attribute queries by ID
- `LogicalName`
- `EntitySetName` — the OData set name used in queries
- `DisplayName.UserLocalizedLabel.Label`
- `PrimaryIdAttribute`
- `PrimaryNameAttribute`

### List All Entities

```
GET /api/data/v9.2/EntityDefinitions?$select=LogicalName,EntitySetName,DisplayName
```

**Python:**
```python
all_entities = client.get_all_entity_metadata()
# Returns list of entity metadata dicts
```

---

## Attribute Metadata

### All Attributes for an Entity (by logical name)

```
GET /api/data/v9.2/EntityDefinitions(LogicalName='{entity}')/Attributes?$select=LogicalName,AttributeType,DisplayName,IsLogical,MaxLength,IsPrimaryId,IsPrimaryName
```

**Python:**
```python
attrs = client.get_entity_attributes('mnp_payment')
attr_map = {a['LogicalName']: a for a in attrs}

# Check if attribute exists
if 'mnp_amount' not in attr_map:
    print("WARNING: attribute not found")

# Check if logical (expensive)
if attr_map.get('mnp_amount', {}).get('IsLogical'):
    print("NOTE: logical column — filter may be slow")

# Check string length (filter safety)
if attr_map.get('description', {}).get('MaxLength', 0) > 850:
    print("WARNING: large text column — avoid filtering")
```

### Attributes by Entity MetadataId

```
GET /api/data/v9.2/EntityDefinitions({MetadataId})/Attributes?$select=LogicalName,AttributeType,DisplayName
```

### Attribute Types Reference

| `AttributeType` | Description |
|---|---|
| `String` | Short text (check `MaxLength`) |
| `Memo` | Multi-line text (always large) |
| `Integer` / `BigInt` | Integer |
| `Decimal` / `Double` / `Money` | Numeric |
| `Boolean` | Two-option |
| `DateTime` | Date/time |
| `Picklist` / `State` / `Status` | Choice (option set) |
| `Lookup` / `Owner` / `Customer` | Relationship lookup |
| `UniqueIdentifier` | GUID |
| `Virtual` | Calculated/formula |

---

## Relationship Metadata

### Validate a Relationship by Schema Name

```
GET /api/data/v9.2/RelationshipDefinitions?$filter=SchemaName eq '{SchemaName}'
```

### One-to-Many Relationships for an Entity

```
GET /api/data/v9.2/EntityDefinitions(LogicalName='{entity}')/OneToManyRelationships?$select=SchemaName,ReferencingEntity,ReferencingAttribute,ReferencedAttribute
```

### Many-to-One Relationships for an Entity

```
GET /api/data/v9.2/EntityDefinitions(LogicalName='{entity}')/ManyToOneRelationships?$select=SchemaName,ReferencedEntity,ReferencingAttribute,ReferencedAttribute
```

### Many-to-Many Relationships

```
GET /api/data/v9.2/EntityDefinitions(LogicalName='{entity}')/ManyToManyRelationships?$select=SchemaName,Entity1LogicalName,Entity2LogicalName,IntersectEntityName
```

---

## Executing FetchXML

### Via EntitySet + fetchXml parameter

```
GET /api/data/v9.2/{entitySetName}?fetchXml={url_encoded_fetchxml}
```

Headers:
```
Prefer: odata.include-annotations="*"
If-None-Match: null
```

**Python:**
```python
results = client.get_records_with_fetchxml(entity_set_name, fetch_xml_string)
records = results.get('value', [])
next_link = results.get('@odata.nextLink')  # pagination
total = results.get('@Microsoft.Dynamics.CRM.totalrecordcount', -1)
```

### Paging Cookie (Web API)

When the response includes `@Microsoft.Dynamics.CRM.fetchxmlpagingcookie`, extract and URL-decode it, then set as `paging-cookie` attribute on the next request.

The `@odata.nextLink` in the response already encodes the next page URL — use it directly:
```python
while next_link:
    results = client._invoke_resilient_request('GET', next_link, client.base_headers)
    records.extend(results.get('value', []))
    next_link = results.get('@odata.nextLink')
```

---

## Option Set (Choice) Values

To look up display labels for picklist values:

```
GET /api/data/v9.2/EntityDefinitions(LogicalName='{entity}')/Attributes/Microsoft.Dynamics.CRM.PicklistAttributeMetadata?$select=LogicalName&$expand=OptionSet($select=Options)&$filter=LogicalName eq '{attribute}'
```

---

## Global Option Sets

```
GET /api/data/v9.2/GlobalOptionSetDefinitions?$select=Name,Options
```
