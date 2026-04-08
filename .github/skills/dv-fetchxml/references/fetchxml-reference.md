# FetchXML Reference

Source: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/reference/

[[_TOC_]]

## `<fetch>` — Root Element

```xml
<fetch
  top="50"
  count="50" page="1" paging-cookie="..."
  aggregate="true"
  aggregatelimit="5000"
  distinct="true"
  returntotalrecordcount="true"
  latematerialize="true"
  options="HashJoin,DisableRowGoal"
  useraworderby="false"
  datasource="retained"
>
```

| Attribute | Description |
|---|---|
| `top` | Max rows to return (≤ 5,000). Mutually exclusive with `count`/`page`. |
| `count` | Page size for paging (≤ 5,000). Use with `page`. |
| `page` | 1-based page number. |
| `paging-cookie` | Value returned by previous page; set for efficient cursor paging. |
| `aggregate` | `true` enables aggregate mode (`avg`, `sum`, `count`, etc.). |
| `aggregatelimit` | Custom limit below the 50,000 aggregate record cap. |
| `distinct` | Omit duplicate rows. |
| `returntotalrecordcount` | Return `@Microsoft.Dynamics.CRM.totalrecordcount` in response. |
| `latematerialize` | Breaks query into smaller parts — helps for many joins/lookups. |
| `options` | SQL hints (support only, e.g. `HashJoin`, `DisableRowGoal`). |
| `useraworderby` | Sort choice columns by integer value instead of label. |
| `datasource` | Set to `retained` for long-term data retention queries. |

---

## `<entity>` — Primary Table

```xml
<entity name="account">
  ...
</entity>
```

Only one `<entity>` is allowed per `<fetch>`. Use `<link-entity>` for joins.

---

## `<attribute>` — Column Selector

```xml
<!-- Standard column -->
<attribute name="name" alias="AccountName" />

<!-- Aggregate -->
<attribute name="totalamount" alias="TotalAmount" aggregate="sum" />
<attribute name="statuscode"  alias="StatusGroup" groupby="true" />
<attribute name="createdon"   alias="Month" groupby="true" dategrouping="month" />

<!-- Row aggregate (hierarchical) -->
<attribute name="accountid" alias="childCount" rowaggregate="CountChildren" />
```

| Attribute | Description |
|---|---|
| `name` | Logical name of the column. |
| `alias` | Output alias; required for aggregates. |
| `aggregate` | `avg`, `count`, `countcolumn`, `max`, `min`, `sum`. |
| `distinct` | Use with `countcolumn` to count unique values. |
| `groupby` | `true` to group by this column in aggregate queries. |
| `dategrouping` | `day`, `week`, `month`, `quarter`, `year`, `fiscal-period`, `fiscal-year`. |
| `usertimezone` | `false` to use UTC for date groupings (default: user timezone). |
| `rowaggregate` | `CountChildren` for hierarchical child counts. |

---

## `<all-attributes>` — Return All Columns

```xml
<all-attributes />
```

Returns all non-null column values. **Avoid in production** — causes performance issues.

---

## `<link-entity>` — Join

```xml
<link-entity
  name="contact"
  from="contactid"
  to="primarycontactid"
  link-type="outer"
  alias="ct"
  visible="true"
  intersect="false"
>
  <attribute name="fullname" alias="ContactName" />
</link-entity>
```

| Attribute | Description |
|---|---|
| `name` | Logical name of the table to join. |
| `from` | Column on the joined table. |
| `to` | Column on the parent table. |
| `link-type` | `inner` (default), `outer`, `any`, `not any`, `exists`, `not exists`, `matchfirstrowusingcrossapply`. |
| `alias` | Prefix for returned columns; required for cross-table filter conditions. |
| `visible` | Whether joined columns appear in results (default `true`). |
| `intersect` | `true` for N:N intersection tables. |

---

## `<filter>` — Condition Group

```xml
<filter type="and">
  <condition ... />
  <filter type="or">
    <condition ... />
  </filter>
</filter>
```

| Attribute | Description |
|---|---|
| `type` | `and` (default) or `or`. |
| `hint` | `union` — performance hint for OR across related tables (support only). |
| `isquickfindfields` | Internal use for quick-find. |
| `overridequickfindrecordlimitenabled` / `overridequickfindrecordlimitdisabled` | Quick-find overrides. |

---

## `<condition>` — Row Filter Condition

```xml
<condition attribute="statecode"   operator="eq"          value="0" />
<condition attribute="createdon"   operator="last-x-days" value="30" />
<condition attribute="ownerid"     operator="eq-userid" />
<condition attribute="statuscode"  operator="in">
  <value>1</value>
  <value>2</value>
</condition>
<condition attribute="name"        operator="like"        value="Contoso%" />
<!-- Cross-table: filter on link-entity column -->
<condition attribute="fullname"    operator="ne-null"     entityname="ct" />
```

| Attribute | Description |
|---|---|
| `attribute` | Logical name of the column to test. |
| `operator` | See table below. |
| `value` | Comparison value (single). |
| `valueof` | Name of another column in the same table to compare against. |
| `entityname` | Alias of a `link-entity` when filtering on a joined table column. |

### Common Operators

| Operator | Meaning |
|---|---|
| `eq` / `ne` | Equal / not equal |
| `lt` / `le` / `gt` / `ge` | Less / less-or-equal / greater / greater-or-equal |
| `like` / `not-like` | String pattern (use `%` wildcard — avoid leading `%`) |
| `in` / `not-in` | Value in list (`<value>` children) |
| `null` / `not-null` | Is null / is not null |
| `begins-with` / `ends-with` | String prefix/suffix |
| `between` / `not-between` | Range (two `<value>` children) |
| `eq-userid` / `ne-userid` | Equals / not equals current user |
| `eq-userteams` / `eq-useroruserteams` | Current user's teams |
| `eq-businessid` | Current business unit |
| `today` / `yesterday` / `tomorrow` | Date shortcuts |
| `on` / `on-or-before` / `on-or-after` | Exact date |
| `this-week` / `last-week` / `next-week` | Week ranges |
| `this-month` / `last-month` / `next-month` | Month ranges |
| `this-year` / `last-year` / `next-year` | Year ranges |
| `last-x-hours` / `last-x-days` / `last-x-weeks` / `last-x-months` / `last-x-years` | Relative past (use `value` for X) |
| `next-x-hours` / `next-x-days` / `next-x-weeks` / `next-x-months` / `next-x-years` | Relative future |
| `olderthan-x-days` / `olderthan-x-weeks` / `olderthan-x-months` / `olderthan-x-years` | Older than X units |
| `in-fiscal-period` / `in-fiscal-period-and-year` / `in-fiscal-year` | Fiscal period/year |
| `above` / `under` / `eq-or-above` / `eq-or-under` | Hierarchical |
| `contain-values` / `not-contain-values` | Choice column multi-select |

---

## `<order>` — Sort

```xml
<order attribute="createdon" descending="true" />
<order attribute="accountid" />                   <!-- tiebreaker -->

<!-- In aggregate queries, order by alias -->
<order alias="TotalAmount" descending="true" />
```

| Attribute | Description |
|---|---|
| `attribute` | Column logical name (non-aggregate queries). |
| `alias` | Alias of an aggregated column (aggregate queries). |
| `descending` | `true` for DESC; default is ASC. |

---

## `<value>` — Multi-Value List

Used with operators like `in`, `not-in`, `between`:

```xml
<condition attribute="statuscode" operator="in">
  <value>1</value>
  <value>2</value>
  <value>3</value>
</condition>
```

---

## Common Patterns

### Active Records Only
```xml
<filter type="and">
  <condition attribute="statecode" operator="eq" value="0" />
</filter>
```

### Date Range (last 30 days)
```xml
<condition attribute="createdon" operator="last-x-days" value="30" />
```

### Join Contact to Account
```xml
<link-entity name="contact" from="contactid" to="primarycontactid" link-type="outer" alias="ct">
  <attribute name="fullname" alias="PrimaryContactName" />
</link-entity>
```

### Aggregate: Sum + GroupBy
```xml
<fetch aggregate="true">
  <entity name="mnp_payment">
    <attribute name="mnp_amount" alias="TotalAmount" aggregate="sum" />
    <attribute name="statuscode" alias="StatusCode" groupby="true" />
    <order alias="StatusCode" />
  </entity>
</fetch>
```

### Paging with Cookie
```xml
<!-- Page 1 -->
<fetch count="50" page="1">
  <entity name="account">
    <attribute name="name" />
    <order attribute="name" />
    <order attribute="accountid" />
  </entity>
</fetch>

<!-- Page 2+ — set paging-cookie from previous response -->
<fetch count="50" page="2" paging-cookie="&lt;cookie page=&quot;1&quot; ...&gt;">
  ...
</fetch>
```

### Assigned to Current User
```xml
<condition attribute="ownerid" operator="eq-userid" />
```

### Link-Entity Filter (inner join semantics)
```xml
<link-entity name="systemuser" from="systemuserid" to="ownerid" link-type="inner" alias="usr">
  <filter>
    <condition attribute="isdisabled" operator="eq" value="0" />
  </filter>
</link-entity>
```
