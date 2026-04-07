# Dataverse Web API Endpoints — Solution Inspector Reference

All endpoints are relative to `{env_url}/api/data/v9.2/`.

## Solution & Component Discovery

| Purpose | Endpoint |
|---|---|
| Find solution by unique name | `solutions?$filter=uniquename eq '{name}'&$select=solutionid,uniquename,version,friendlyname` |
| List entity components in solution | `solutioncomponents?$filter=_solutionid_value eq '{solutionid}' and componenttype eq 1&$select=objectid,componenttype` |
| Resolve entity logical name from objectid | `EntityDefinitions({objectid})?$select=LogicalName,DisplayName,SchemaName` |

**Component type codes** (filter in `solutioncomponents`):
- `1` = Entity (table)
- `2` = Attribute (column)
- `26` = SavedQuery (view)
- `24` = SystemForm

## Component Date Lookup

`AttributeMetadata.CreatedOn` is **not reliable** in Dataverse — it often returns `1900-01-01` for both system and custom fields. Use `solutioncomponent.createdon` as the best proxy for "when this component arrived in this environment."

| Purpose | Endpoint |
|---|---|
| Earliest createdon for an entity | `solutioncomponents?$filter=objectid eq {metadataId} and componenttype eq 1&$select=objectid,createdon&$orderby=createdon asc&$top=1` |
| Earliest createdon for an attribute | `solutioncomponents?$filter=objectid eq {metadataId} and componenttype eq 2&$select=objectid,createdon&$orderby=createdon asc&$top=1` |
| Batch attribute dates (up to ~20 MetadataIds) | `solutioncomponents?$filter=componenttype eq 2 and (objectid eq {id1} or objectid eq {id2} ...)&$select=objectid,createdon&$orderby=objectid asc,createdon asc` |

**Notes:**
- `objectid` in `solutioncomponents` maps to `MetadataId` on `EntityDefinitions` and `AttributeMetadata`.
- GUID values in OData filter predicates are **unquoted**: `objectid eq 00000000-0000-0000-0000-000000000000`.
- When a component exists in multiple solution layers, take the **earliest** `createdon` across all rows.
- Filter out results where `createdon` starts with `1900-` — these are platform placeholder values.
- OOTB fields (IsCustomAttribute=false) almost always return placeholder dates; only query custom attributes.

## Entity Metadata

| Purpose | Endpoint |
|---|---|
| Entity definition | `EntityDefinitions(LogicalName='{entity}')` |
| All attributes | `EntityDefinitions(LogicalName='{entity}')/Attributes` |
| Picklist attributes (with option sets) | `EntityDefinitions(LogicalName='{entity}')/Attributes/Microsoft.Dynamics.CRM.PicklistAttributeMetadata?$expand=OptionSet,GlobalOptionSet` |
| Multi-select picklist attributes | `EntityDefinitions(LogicalName='{entity}')/Attributes/Microsoft.Dynamics.CRM.MultiSelectPicklistAttributeMetadata?$expand=OptionSet,GlobalOptionSet` |
| 1:N relationships | `EntityDefinitions(LogicalName='{entity}')/OneToManyRelationships` |
| N:1 relationships | `EntityDefinitions(LogicalName='{entity}')/ManyToOneRelationships` |
| N:N relationships | `EntityDefinitions(LogicalName='{entity}')/ManyToManyRelationships` |

## Forms

| Purpose | Endpoint |
|---|---|
| All active forms for entity | `systemforms?$filter=objecttypecode eq '{entity}' and formactivationstate eq 1&$select=name,type,description,isdefault,formjson,iscustomizable` |
| All forms including inactive | `systemforms?$filter=objecttypecode eq '{entity}'&$select=name,type,description,isdefault,formactivationstate` |

**Form type codes** (`type` field in systemform):
- `0` = Main
- `1` = Mobile
- `2` = Quick Create
- `4` = Quick View
- `5` = Card
- `6` = Main (Interactive experience)
- `8` = Power BI embedded

## Views (Saved Queries)

| Purpose | Endpoint |
|---|---|
| All views for entity | `savedqueries?$filter=returnedtypecode eq '{entity}'&$select=name,querytype,isdefault,iscustomizable,fetchxml,layoutxml,description` |
| System views only | `savedqueries?$filter=returnedtypecode eq '{entity}' and querytype eq 0&$select=name,isdefault,fetchxml,layoutxml` |
| Public views | `savedqueries?$filter=returnedtypecode eq '{entity}' and querytype eq 0` |

**Query type codes** (`querytype` field):
- `0` = Main grid view (public)
- `1` = Advanced Find view
- `2` = Associated view
- `4` = Quick Find view
- `64` = Lookup view

## Common OData Query Options

```
$select=field1,field2        # Limit returned fields
$filter=condition            # Filter results
$top=50                      # Limit result count
$expand=NavProp              # Expand navigation property
$orderby=field asc/desc      # Sort results
```

## Authentication Notes

- Uses `DataverseClient` from `.github/scripts/dataverse_sdk_client.py`
- Environment URLs and tenant IDs from `.env`
- Interactive browser auth by default; service principal via `--app-id` + `--client-secret`
- Token is cached in OS keychain between runs
