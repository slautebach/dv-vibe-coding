# FetchXML to OData Conversion Guide

Source: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/query/overview

Use this guide when converting FetchXML to OData `$filter`/`$expand` expressions for use in canvas apps, Power Automate, or direct Web API calls.

[[_TOC_]]

## OData Query Options

| OData Option | FetchXML Equivalent | Purpose |
|---|---|---|
| `$select` | `<attribute>` | Columns to return |
| `$filter` | `<filter>` / `<condition>` | Row filter |
| `$expand` | `<link-entity>` | Join related table |
| `$orderby` | `<order>` | Sort |
| `$top` | `<fetch top="N">` | Limit rows |
| `$count=true` | `returntotalrecordcount="true"` | Include total count |
| `$apply` | `<fetch aggregate="true">` | Aggregate/group |

---

## Column Selection

**FetchXML:**
```xml
<attribute name="name" />
<attribute name="statuscode" />
<attribute name="createdon" />
```

**OData:**
```
$select=name,statuscode,createdon
```

---

## Filtering

### Basic Conditions

| FetchXML operator | OData `$filter` |
|---|---|
| `eq` | `field eq value` |
| `ne` | `field ne value` |
| `lt` / `le` / `gt` / `ge` | `field lt value` etc. |
| `null` | `field eq null` |
| `not-null` | `field ne null` |
| `like` (suffix `%`) | `startswith(field, 'prefix')` |
| `like` (`%text%`) | `contains(field, 'text')` |
| `begins-with` | `startswith(field, 'value')` |
| `ends-with` | `endswith(field, 'value')` |
| `in` | `field in ('a','b','c')` or `(field eq 'a' or field eq 'b')` |
| `between` | `field ge low and field le high` |
| `today` | `Microsoft.Dynamics.CRM.Today()` |
| `last-x-days` | `Microsoft.Dynamics.CRM.LastXDays(x=30)` |
| `eq-userid` | `_ownerid_value eq {userId}` |

**FetchXML:**
```xml
<filter type="and">
  <condition attribute="statecode"  operator="eq"          value="0" />
  <condition attribute="createdon"  operator="last-x-days" value="30" />
  <condition attribute="name"       operator="begins-with" value="Contoso" />
</filter>
```

**OData:**
```
$filter=statecode eq 0 and Microsoft.Dynamics.CRM.LastXDays(PropertyName='createdon',PropertyValue=30) and startswith(name,'Contoso')
```

### AND / OR

**FetchXML:**
```xml
<filter type="or">
  <condition attribute="statuscode" operator="eq" value="1" />
  <condition attribute="statuscode" operator="eq" value="2" />
</filter>
```

**OData:**
```
$filter=(statuscode eq 1 or statuscode eq 2)
```

---

## Joining Tables (`$expand`)

OData `$expand` follows navigation properties — it cannot join on arbitrary columns.

**FetchXML:**
```xml
<link-entity name="contact" from="contactid" to="primarycontactid" link-type="outer" alias="ct">
  <attribute name="fullname" alias="ContactName" />
</link-entity>
```

**OData:**
```
$expand=primarycontactid($select=fullname)
```

### Finding Navigation Property Names

Navigation properties follow conventions:
- Single-valued (lookup): `_fieldname_value` for the GUID; `fieldname` for `$expand`
- Collection-valued: `entitylogicalname_parententitylogicalname` or defined in metadata

Check `$metadata` or the entity reference docs to find the correct navigation property name.

### OData Join Limitations vs FetchXML

| Capability | FetchXML | OData |
|---|---|---|
| Join without relationship | Yes (`from`/`to` any columns) | No (navigation properties only) |
| Cross-table column comparison | Yes | No |
| Nested N:N expand | Yes | Limited |
| `inner` vs `outer` join | Yes (`link-type`) | `$expand` is always outer |
| Late materialize | Yes | No |
| Aggregate on linked entity | Yes | Limited |

---

## Sorting

**FetchXML:**
```xml
<order attribute="createdon" descending="true" />
<order attribute="accountid" />
```

**OData:**
```
$orderby=createdon desc,accountid
```

Note: OData sorts choice columns by integer value; FetchXML sorts by label by default.

---

## Limiting Rows

**FetchXML:**
```xml
<fetch top="50">
```

**OData:**
```
$top=50
```

Do not use `$top` with `Prefer: odata.maxpagesize` — they conflict. Use only one at a time.

---

## Aggregation (`$apply`)

OData aggregation uses `$apply=aggregate(...)` or `$apply=groupby(...)`.

**FetchXML:**
```xml
<fetch aggregate="true">
  <entity name="mnp_payment">
    <attribute name="mnp_amount" alias="TotalAmount" aggregate="sum" />
    <attribute name="statuscode" alias="Status" groupby="true" />
  </entity>
</fetch>
```

**OData:**
```
$apply=groupby((statuscode),aggregate(mnp_amount with sum as TotalAmount))
```

### OData Aggregate Functions

| FetchXML | OData |
|---|---|
| `sum` | `sum` |
| `avg` | `average` |
| `min` | `min` |
| `max` | `max` |
| `count` | `$count` or `countdistinct` |
| `countcolumn` | `countdistinct` (with `distinct="true"`) |

### OData Aggregation Limitations (vs FetchXML)

- No `distinct` count via `countcolumn` in all scenarios
- No time zone control for date groupings (always UTC)
- No row aggregate (`CountChildren`)
- No `aggregatelimit`

---

## Paging

**OData paging** uses `Prefer: odata.maxpagesize=N` and follows `@odata.nextLink`:

```
GET /api/data/v9.2/accounts?$select=name&$orderby=name,accountid
Prefer: odata.maxpagesize=50
```

If `@odata.nextLink` is in the response, use it verbatim for the next page. Do not modify the URL.

---

## Canvas App Formula Examples

In Power Fx (canvas apps), use the `Filter`, `Sort`, and `LookUp` functions which generate OData behind the scenes:

```powerfx
// Active accounts created in last 30 days
Filter(
    Accounts,
    Status = "Active",
    'Created On' >= DateAdd(Today(), -30, Days)
)

// With related contact name
AddColumns(
    Filter(mnp_payments, statuscode = 1),
    "ContactName",
    LookUp(Contacts, contactid = ThisRecord.customerid).fullname
)
```

For complex FetchXML that has no OData equivalent, use a custom connector or a Power Automate flow with the Dataverse connector's "List rows" action (which supports FetchXML via the `Fetch Xml Query` parameter).
