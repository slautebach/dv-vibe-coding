# FetchXML Reference

## Overview

FetchXML is Dataverse's proprietary XML query language for retrieving data. Used in:
- **SavedQueries**: System views
- **UserQuery**: Personal views
- **Workflows**: Data retrieval steps
- **Reports**: SSRS reports
- **Code**: SDK and Web API queries
- **Dashboards**: Chart and grid queries

**Official Documentation**: [FetchXML Reference](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/reference/)

## Basic Structure

```xml
<fetch version="1.0" mapping="logical" distinct="false">
  <entity name="mnp_application">
    <attribute name="mnp_applicationid" />
    <attribute name="mnp_name" />
    <order attribute="mnp_name" descending="false" />
    <filter type="and">
      <condition attribute="statecode" operator="eq" value="0" />
    </filter>
  </entity>
</fetch>
```

## fetch Element

The root element of a FetchXML query.

[Official Reference](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/reference/fetch)

```xml
<fetch 
  version="1.0"
  mapping="logical"
  distinct="false"
  no-lock="false"
  page="1"
  count="50"
  top="10"
  aggregate="false"
  aggregatelimit="50000"
  returntotalrecordcount="false"
  latematerialize="false"
  useraworderby="false"
  datasource="retained"
  options="HashJoin,DisableRowGoal"
  paging-cookie="..."
>
  <entity name="account" />
</fetch>
```

### Attributes

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| `aggregate` | No | Boolean | Specify that the query returns aggregate values. [Learn more](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/aggregate-data) |
| `aggregatelimit` | No | Integer | Set a limit below the standard 50,000 record aggregate limit |
| `count` | No | Positive Integer | Number of records to return in a page. [Learn more](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/page-results) |
| `datasource` | No | String | Set to `'retained'` for long-term data retention queries |
| `distinct` | No | Boolean | Specify that duplicate rows not be included in results |
| `latematerialize` | No | Boolean | Break query into smaller parts and reassemble results. May improve performance for long-running queries |
| `mapping` | No | String | Typically `"logical"` to use logical names |
| `no-lock` | No | Boolean | Legacy setting to prevent shared locks. [No longer necessary](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/optimize-performance#no-lock) |
| `options` | No | String | SQL optimization hints (e.g., `"HashJoin,DisableRowGoal"`). Only use when recommended by Microsoft support |
| `page` | No | Positive Integer | Page number to return (1-based). [Learn more](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/page-results) |
| `paging-cookie` | No | String | Encoded string from previous page to improve paging performance |
| `returntotalrecordcount` | No | Boolean | Return the total number of records matching criteria. [Learn more](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/count-rows) |
| `top` | No | Positive Integer | Limit number of records (max 5,000). Don't use with `page`, `count`, or `returntotalrecordcount` |
| `useraworderby` | No | Boolean | Sort choice columns by integer value instead of label |
| `version` | No | String | FetchXML version (typically "1.0") |

### options Attribute Values

⚠️ **Important**: Only apply these options when recommended by Microsoft technical support. Incorrect use can damage query performance.

When using multiple options, separate with commas: `options="HashJoin,DisableRowGoal"`

| Option | SQL Server Hint |
|--------|-----------------|
| `ForceOrder` | Force Order |
| `DisableRowGoal` | Disable Optimizer Row Goal |
| `EnableOptimizerHotfixes` | Enable Query Optimizer Hotfixes |
| `LoopJoin` | Loop Join |
| `MergeJoin` | Merge Join |
| `HashJoin` | Hash Join |
| `NO_PERFORMANCE_SPOOL` | No Performance Spool |
| `ENABLE_HIST_AMENDMENT_FOR_ASC_KEYS` | Enable Histogram Amendment for Ascending Keys |

### Child Elements

- **entity** (required, exactly 1): The primary table to query  

## entity Element

Specifies the primary table for the query. Only one entity element is allowed per fetch element.

[Official Reference](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/reference/entity)

```xml
<entity name="mnp_application">
  <attribute name="mnp_name" />
  <all-attributes />
  <order attribute="mnp_name" descending="false" />
  <filter type="and">...</filter>
  <link-entity>...</link-entity>
</entity>
```

### Attributes

| Attribute | Required | Description |
|-----------|----------|-------------|
| `name` | Yes | Logical name of the table |

### Child Elements

- **all-attributes** (0 or 1): Return all non-null columns. ⚠️ Not recommended
- **attribute** (0 or many): Specify columns to return
- **order** (0 or many): Sort order for results
- **link-entity** (0 or many): Join related tables
- **filter** (0 or 1): Conditions to filter records

## attribute Element

Specifies a column from an entity or link-entity to return with the query.

[Official Reference](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/reference/attribute) | [Select Columns Guide](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/select-columns)

```xml
<attribute name="mnp_name" />
<attribute name="createdon" />
```

### Standard Usage

```xml
<entity name="account">
  <attribute name="name" />
  <link-entity name="contact" from="contactid" to="primarycontactid" alias="contact">
    <attribute name="fullname" />
  </link-entity>
</entity>
```

### Attributes

| Attribute | Required | Description |
|-----------|----------|-------------|
| `name` | Yes | Logical name of the column |
| `alias` | No | Name for the column in results. Required for aggregate queries |
| `aggregate` | No | Aggregate function to apply: `count`, `countcolumn`, `sum`, `avg`, `min`, `max` |
| `groupby` | No | When aggregating, group results by this column (Boolean) |
| `dategrouping` | No | For datetime grouping: `day`, `week`, `month`, `quarter`, `year`, `fiscal-period`, `fiscal-year` |
| `distinct` | No | For `countcolumn` aggregate, count only unique values (Boolean) |
| `rowaggregate` | No | Set to `CountChildren` to include count of hierarchical child records |
| `usertimezone` | No | For datetime grouping, use user's timezone (`true`) or UTC (`false`). Default is `true` |

### Aggregation Example

```xml
<fetch aggregate="true">
  <entity name="mnp_application">
    <attribute name="mnp_amount" aggregate="sum" alias="total_amount" />
    <attribute name="mnp_applicationid" aggregate="countcolumn" alias="app_count" />
    <attribute name="mnp_status" groupby="true" alias="status" />
    <attribute name="createdon" groupby="true" dategrouping="month" alias="month" />
  </entity>
</fetch>
```

### Aggregate Functions

| Function | Description |
|----------|-------------|
| `count` | Number of rows |
| `countcolumn` | Number of rows with data in the column |
| `sum` | Total value of column values |
| `avg` | Average value of column values |
| `min` | Minimum value in the column |
| `max` | Maximum value in the column |

### Date Grouping Options

| Value | Description |
|-------|-------------|
| `day` | Group by day of the month |
| `week` | Group by week of the year |
| `month` | Group by month of the year |
| `quarter` | Group by quarter of the fiscal year |
| `year` | Group by the year |
| `fiscal-period` | Group by period of the fiscal year |
| `fiscal-year` | Group by the fiscal year |

## all-attributes Element

⚠️ **Not Recommended**: Returns all non-null column values for each row. Same as not adding any attribute elements.

[Official Reference](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/reference/all-attributes)

```xml
<entity name="account">
  <all-attributes/>
</entity>
```

Using all-attributes makes applications run slower and may cause timeout errors. Always specify specific attributes instead.

## order Element

Specifies sort order for query results.

[Official Reference](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/reference/order) | [Order Rows Guide](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/order-rows)

```xml
<order attribute="mnp_name" descending="false" />
<order attribute="createdon" descending="true" />
```

### Attributes

| Attribute | Required | Description |
|-----------|----------|-------------|
| `attribute` | Yes* | Logical name of the attribute to sort by |
| `alias` | No* | Alias of the attribute to sort by (for aggregates) |
| `descending` | No | Sort in descending order (Boolean, default false) |
| `entityname` | No | Alias of link-entity to apply order from. Used to process link-entity orders first |

*Either `attribute` or `alias` is required

### Multiple Sort Orders

```xml
<entity name="account">
  <attribute name="name" />
  <attribute name="accountnumber" />
  <attribute name="createdon" />
  <order attribute="createdon" />
  <order attribute="name" />
  <order attribute="accountnumber" />
</entity>
```

### Link-Entity Ordering

By default, order elements in link-entity are processed last. Use `entityname` to control ordering:

```xml
<entity name="account">
  <attribute name="name" />
  <order attribute="name" entityname="contact" />
  <order attribute="name" />
  <link-entity name="contact" from="contactid" to="primarycontactid" alias="contact">
    <attribute name="fullname" />
  </link-entity>
</entity>
```

## filter Element

Specifies complex conditions for filtering query results.

[Official Reference](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/reference/filter) | [Filter Rows Guide](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/filter-rows)

```xml
<filter type="and">
  <condition attribute="statecode" operator="eq" value="0" />
  <condition attribute="mnp_status" operator="in">
    <value>120310001</value>
    <value>120310002</value>
  </condition>
  <filter type="or">
    <condition attribute="mnp_priority" operator="eq" value="120310000" />
    <condition attribute="mnp_urgent" operator="eq" value="1" />
  </filter>
</filter>
```

### Attributes

| Attribute | Required | Description |
|-----------|----------|-------------|
| `type` | No | `and` (all conditions must match) or `or` (any condition). Default is `and` |
| `hint` | No | Set to `union` for performance optimization in specific scenarios |
| `isquickfindfields` | No | Execute as quick find query (Boolean) |
| `overridequickfindrecordlimitenabled` | No | Apply quick find record limit |
| `overridequickfindrecordlimitdisabled` | No | Bypass quick find record limit |

### Child Elements

- **condition** (0 to 500): Individual filter conditions
- **filter** (0 or many): Nested filters for complex logic
- **link-entity** (0 or many): Used when filtering on values in related records

### Nested Filters

Filters can be nested for complex boolean logic:

```xml
<filter type="and">
  <condition attribute="statecode" operator="eq" value="0" />
  <filter type="or">
    <filter type="and">
      <condition attribute="mnp_priority" operator="eq" value="120310000" />
      <condition attribute="mnp_amount" operator="gt" value="5000" />
    </filter>
    <filter type="and">
      <condition attribute="mnp_urgent" operator="eq" value="1" />
      <condition attribute="ownerid" operator="eq-userid" />
    </filter>
  </filter>
</filter>
```

Logic: `Active AND ((High Priority AND Amount > 5000) OR (Urgent AND Owned by Me))`

## condition Element

Specifies individual filter conditions that must be true for records to be returned.

[Official Reference](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/reference/condition) | [Operators Reference](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/reference/operators)

```xml
<condition 
  attribute="mnp_name" 
  operator="like" 
  value="%test%" 
/>
```

### Attributes

| Attribute | Required | Description |
|-----------|----------|-------------|
| `operator` | Yes | Comparison operator (see Operators section) |
| `attribute` | No* | Column name to filter on |
| `value` | No** | Single value to compare (for operators like `eq`, `ne`, `like`) |
| `valueof` | No | Column name to compare against (filter on column values in same row) |
| `entityname` | No | Link-entity `name` or `alias` to apply condition to (for outer joins) |

*Required unless using operators like `null` that don't need an attribute  
**Not needed for operators like `null`, `not-null`, `eq-userid`

### Child Elements

- **value** (0 or many): Multiple values for operators like `in`, `between`

### Examples

**Single value:**

```xml
<condition attribute="statecode" operator="eq" value="0" />
```

**Multiple values:**

```xml
<condition attribute="statuscode" operator="in">
  <value>1</value>
  <value>2</value>
  <value>3</value>
</condition>
```

**Between values:**

```xml
<condition attribute="mnp_amount" operator="between">
  <value>1000</value>
  <value>5000</value>
</condition>
```

**No value required:**

```xml
<condition attribute="ownerid" operator="eq-userid" />
<condition attribute="mnp_approvedby" operator="null" />
```

**Filter on other column values:**

```xml
<condition attribute="actualend" operator="gt" valueof="scheduledend" />
```

## Operators

FetchXML supports a wide range of operators for filtering data. [Official Operators Reference](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/reference/operators)

### Comparison Operators

| Operator | Description | Data Types | Example |
|----------|-------------|------------|---------|
| `eq` | Equals | All | `<condition attribute="statecode" operator="eq" value="0" />` |
| `ne` | Not equals | All | `<condition attribute="statecode" operator="ne" value="1" />` |
| `lt` | Less than | Number, Datetime, String | `<condition attribute="mnp_amount" operator="lt" value="1000" />` |
| `le` | Less than or equal | Number, Datetime, String | `<condition attribute="mnp_amount" operator="le" value="1000" />` |
| `gt` | Greater than | Number, Datetime, String | `<condition attribute="mnp_amount" operator="gt" value="500" />` |
| `ge` | Greater than or equal | Number, Datetime, String | `<condition attribute="mnp_amount" operator="ge" value="500" />` |
| `between` | Between two values | Number, Datetime | `<condition attribute="mnp_amount" operator="between"><value>100</value><value>1000</value></condition>` |
| `not-between` | Not between two values | Number, Datetime | `<condition attribute="mnp_amount" operator="not-between"><value>100</value><value>1000</value></condition>` |

### String Operators

All string operators are **case-insensitive**. Wildcard characters (`%`, `_`, `[]`) are supported.

| Operator | Description | Example |
|----------|-------------|---------|
| `like` | Contains pattern | `<condition attribute="mnp_name" operator="like" value="%test%" />` |
| `not-like` | Does not contain pattern | `<condition attribute="mnp_name" operator="not-like" value="%temp%" />` |
| `begins-with` | Starts with | `<condition attribute="mnp_name" operator="begins-with" value="App" />` |
| `not-begin-with` | Does not start with | `<condition attribute="mnp_name" operator="not-begin-with" value="Test" />` |
| `ends-with` | Ends with | `<condition attribute="mnp_name" operator="ends-with" value="2024" />` |
| `not-end-with` | Does not end with | `<condition attribute="mnp_name" operator="not-end-with" value="old" />` |

### Null Check Operators

| Operator | Description | Data Types | Example |
|----------|-------------|------------|---------|
| `null` | Is null | All | `<condition attribute="mnp_approvedby" operator="null" />` |
| `not-null` | Is not null | All | `<condition attribute="mnp_approvedby" operator="not-null" />` |

### List Operators

| Operator | Description | Data Types | Example |
|----------|-------------|------------|---------|
| `in` | Value in list | Choice, Number, Owner, String, Unique Identifier | `<condition attribute="statecode" operator="in"><value>0</value><value>1</value></condition>` |
| `not-in` | Value not in list | Number | `<condition attribute="statuscode" operator="not-in"><value>2</value></condition>` |

### Date/Time Operators

#### Absolute Date Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `on` | On specific date | `<condition attribute="createdon" operator="on" value="2024-01-15" />` |
| `on-or-before` | On or before date | `<condition attribute="createdon" operator="on-or-before" value="2024-12-31" />` |
| `on-or-after` | On or after date | `<condition attribute="createdon" operator="on-or-after" value="2024-01-01" />` |

#### Relative Date Operators

| Operator | Description |
|----------|-------------|
| `today` | Today |
| `yesterday` | Yesterday |
| `tomorrow` | Tomorrow |
| `this-week` | Current week (Sunday-Saturday) |
| `this-month` | Current month |
| `this-year` | Current year |
| `last-week` | Previous week |
| `last-month` | Previous month |
| `last-year` | Previous year |
| `next-week` | Next week |
| `next-month` | Next month |
| `next-year` | Next year |
| `last-seven-days` | Last 7 days including today |
| `next-seven-days` | Next 7 days |

#### Parameterized Date Operators

Specify X in the `value` attribute:

| Operator | Description | Example |
|----------|-------------|---------|
| `last-x-hours` | Last X hours | `<condition attribute="createdon" operator="last-x-hours" value="24" />` |
| `last-x-days` | Last X days | `<condition attribute="createdon" operator="last-x-days" value="7" />` |
| `last-x-weeks` | Last X weeks | `<condition attribute="createdon" operator="last-x-weeks" value="4" />` |
| `last-x-months` | Last X months | `<condition attribute="createdon" operator="last-x-months" value="6" />` |
| `last-x-years` | Last X years | `<condition attribute="createdon" operator="last-x-years" value="2" />` |
| `next-x-hours` | Next X hours | `<condition attribute="scheduledstart" operator="next-x-hours" value="48" />` |
| `next-x-days` | Next X days | `<condition attribute="scheduledstart" operator="next-x-days" value="30" />` |
| `next-x-weeks` | Next X weeks | `<condition attribute="scheduledstart" operator="next-x-weeks" value="2" />` |
| `next-x-months` | Next X months | `<condition attribute="scheduledstart" operator="next-x-months" value="3" />` |
| `next-x-years` | Next X years | `<condition attribute="scheduledstart" operator="next-x-years" value="1" />` |
| `olderthan-x-minutes` | Older than X minutes | `<condition attribute="createdon" operator="olderthan-x-minutes" value="30" />` |
| `olderthan-x-hours` | Older than X hours | `<condition attribute="createdon" operator="olderthan-x-hours" value="2" />` |
| `olderthan-x-days` | Older than X days | `<condition attribute="createdon" operator="olderthan-x-days" value="90" />` |
| `olderthan-x-weeks` | Older than X weeks | `<condition attribute="createdon" operator="olderthan-x-weeks" value="12" />` |
| `olderthan-x-months` | Older than X months | `<condition attribute="createdon" operator="olderthan-x-months" value="6" />` |
| `olderthan-x-years` | Older than X years | `<condition attribute="createdon" operator="olderthan-x-years" value="5" />` |

#### Fiscal Period Operators

Behavior depends on organization fiscal year settings.

| Operator | Description |
|----------|-------------|
| `this-fiscal-year` | Current fiscal year |
| `this-fiscal-period` | Current fiscal period |
| `last-fiscal-year` | Previous fiscal year |
| `last-fiscal-period` | Previous fiscal period |
| `next-fiscal-year` | Next fiscal year |
| `next-fiscal-period` | Next fiscal period |
| `in-fiscal-year` | In specified fiscal year (value required) |
| `in-fiscal-period` | In specified fiscal period (value required) |
| `in-fiscal-period-and-year` | In specified period and year (two values) |
| `in-or-before-fiscal-period-and-year` | In or before specified period and year |
| `in-or-after-fiscal-period-and-year` | In or after specified period and year |
| `last-x-fiscal-years` | Last X fiscal years |
| `last-x-fiscal-periods` | Last X fiscal periods |
| `next-x-fiscal-years` | Next X fiscal years |
| `next-x-fiscal-periods` | Next X fiscal periods |

### User/Team Context Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `eq-userid` | Equals current user ID | `<condition attribute="ownerid" operator="eq-userid" />` |
| `ne-userid` | Not equal to current user ID | `<condition attribute="ownerid" operator="ne-userid" />` |
| `eq-userteams` | In current user's teams | `<condition attribute="ownerid" operator="eq-userteams" />` |
| `eq-useroruserteams` | Current user or user's teams | `<condition attribute="ownerid" operator="eq-useroruserteams" />` |
| `eq-useroruserhierarchy` | Current user or reporting hierarchy | `<condition attribute="ownerid" operator="eq-useroruserhierarchy" />` |
| `eq-useroruserhierarchyandteams` | Current user, hierarchy, or teams | `<condition attribute="ownerid" operator="eq-useroruserhierarchyandteams" />` |
| `eq-businessid` | Current business unit | `<condition attribute="owningbusinessunit" operator="eq-businessid" />` |
| `ne-businessid` | Not current business unit | `<condition attribute="owningbusinessunit" operator="ne-businessid" />` |
| `eq-userlanguage` | User's language ID | `<condition attribute="languagecode" operator="eq-userlanguage" />` |

### Hierarchical Operators

For querying hierarchical data. [Learn more](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/query-hierarchical-data)

| Operator | Description |
|----------|-------------|
| `under` | All child records below referenced record |
| `not-under` | All records not below referenced record |
| `above` | All records in referenced record's ancestry line |
| `eq-or-above` | Referenced record and all above it |
| `eq-or-under` | Referenced record and all children below it |

### Choice Column Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `contain-values` | Choice value is one of specified values | `<condition attribute="mnp_type" operator="contain-values"><value>1</value></condition>` |
| `not-contain-values` | Choice value is not one of specified values | `<condition attribute="mnp_type" operator="not-contain-values"><value>2</value></condition>` |

### Legacy Operators

| Operator | Description |
|----------|-------------|
| `neq` | ⚠️ Deprecated. Use `ne` instead |

## value Element

Used to specify multiple values for operators like `in`, `between`, and `in-fiscal-period-and-year`.

[Official Reference](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/reference/value)

```xml
<condition attribute="numberofemployees" operator="between">
  <value>6</value>
  <value>20</value>
</condition>

<condition attribute="statuscode" operator="in">
  <value>1</value>
  <value>2</value>
  <value>3</value>
</condition>
```

## link-entity Element

Joins a table related to the entity or another link-entity to return additional columns or apply filters on related data.

[Official Reference](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/reference/link-entity) | [Join Tables Guide](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/join-tables)

```xml
<link-entity 
  name="contact"
  from="contactid"
  to="mnp_contactid"
  link-type="inner"
  alias="contact"
  intersect="true"
>
  <attribute name="fullname" />
  <attribute name="emailaddress1" />
  <filter type="and">
    <condition attribute="statecode" operator="eq" value="0" />
  </filter>
</link-entity>
```

### Attributes

| Attribute | Required | Description |
|-----------|----------|-------------|
| `name` | Yes | Logical name of the related table |
| `from` | No* | Column from the related table to match |
| `to` | No* | Column in the parent element to match |
| `alias` | No | Alias for the related table. Auto-generated if not specified (pattern: `{name}{N}`) |
| `link-type` | No | Type of join. Default is `inner`. See Link Types below |
| `intersect` | No | Indicates the link is for joining only (typically many-to-many), not returning columns |

*While not technically required, `from` and `to` are usually specified. If omitted for many-to-many relationships, Dataverse attempts to determine the relationship automatically.

⚠️ **Important**: The `from` and `to` columns must be the same type. Using different types can cause significant performance penalties.

### Link Types

| Link Type | Description | Use Case |
|-----------|-------------|----------|
| `inner` | Default. Returns only records with matching values in both tables | Standard inner join |
| `outer` | Left outer join. Returns all parent records even without matches | Include parent records without related data |
| `any` | Returns parent rows with **any** matching rows in linked entity | EXISTS-style filtering |
| `not any` | Returns parent rows with **no** matching rows in linked entity | NOT EXISTS-style filtering |
| `all` | Returns parent rows where **none** of the matching rows satisfy additional filters | Complex negation logic (invert filters) |
| `not all` | Equivalent to `any` despite the name | Same as `any` |
| `exists` | Variant of `inner` using SQL EXISTS. No duplicate parent rows | Performance optimization |
| `in` | Variant of `inner` using SQL IN. No duplicate parent rows | Performance optimization |
| `matchfirstrowusingcrossapply` | Returns only first matching row from linked entity | Performance when only one match needed |

### Relationship Examples

#### Many-to-One (Lookup)

```xml
<entity name="account">
  <attribute name="name" />
  <link-entity name="contact" from="contactid" to="primarycontactid" alias="contact">
    <attribute name="fullname" />
  </link-entity>
</entity>
```

#### One-to-Many

```xml
<entity name="contact">
  <attribute name="fullname" />
  <link-entity name="account" from="primarycontactid" to="contactid" alias="accounts">
    <attribute name="name" />
  </link-entity>
</entity>
```

#### Many-to-Many

```xml
<entity name="systemuser">
  <attribute name="fullname" />
  <link-entity name="teammembership" from="systemuserid" to="systemuserid" intersect="true">
    <link-entity name="team" from="teamid" to="teamid" alias="team">
      <attribute name="name" />
    </link-entity>
  </link-entity>
</entity>
```

**Simplified** (Dataverse infers the relationship):

```xml
<entity name="systemuser">
  <attribute name="fullname" />
  <link-entity name="team" alias="team">
    <attribute name="name" />
  </link-entity>
</entity>
```

### Nested Joins

Link-entities can be nested multiple levels:

```xml
<entity name="mnp_application">
  <attribute name="mnp_name" />
  <link-entity name="contact" from="contactid" to="mnp_contactid" alias="applicant">
    <attribute name="fullname" />
    <link-entity name="account" from="accountid" to="parentcustomerid" alias="company">
      <attribute name="name" />
    </link-entity>
  </link-entity>
</entity>
```

### Child Elements

- **all-attributes** (0 or 1): Return all columns from linked table
- **attribute** (0 or many): Specific columns to return
- **order** (0 or many): Sort order
- **link-entity** (0 or many): Nested joins
- **filter** (0 or 1): Conditions on linked table

### Result Column Naming

Linked entity attributes are prefixed with the alias:

- Parent entity: `mnp_name`
- Linked entity: `applicant.fullname` or `applicant_fullname` (depending on context)
- Nested link: `company.name`

### Performance Link Types

**exists** and **in** link types provide performance benefits when you don't need duplicate parent rows:

```xml
<link-entity name="task" from="regardingobjectid" to="accountid" link-type="exists">
  <filter>
    <condition attribute="statecode" operator="eq" value="0" />
  </filter>
</link-entity>
```

Use `matchfirstrowusingcrossapply` when only one example of a match is needed:

```xml
<link-entity name="contact" from="accountid" to="accountid" 
             link-type="matchfirstrowusingcrossapply" alias="contact">
  <attribute name="fullname" />
</link-entity>
```

## SavedQuery Context

FetchXML appears in SavedQuery (system view) and UserQuery (personal view) files within Dynamics 365 solutions.

[Learn about customizing views](https://learn.microsoft.com/en-us/power-apps/developer/model-driven-apps/customize-entity-views)

```xml
<savedquery>
  <name>Active Applications</name>
  <querytype>0</querytype>
  <isdefault>false</isdefault>
  <isquickfindquery>false</isquickfindquery>
  <fetchxml>
    <fetch version="1.0" mapping="logical">
      <entity name="mnp_application">
        <attribute name="mnp_name" />
        <attribute name="mnp_status" />
        <attribute name="createdon" />
        <filter type="and">
          <condition attribute="statecode" operator="eq" value="0" />
        </filter>
        <order attribute="mnp_name" />
      </entity>
    </fetch>
  </fetchxml>
  <layoutxml>
    <grid name="resultset" jump="mnp_name" select="1" preview="1">
      <row name="result" id="mnp_applicationid">
        <cell name="mnp_name" width="200" />
        <cell name="mnp_status" width="100" />
        <cell name="createdon" width="125" />
      </row>
    </grid>
  </layoutxml>
</savedquery>
```

### SavedQuery Attributes

| Attribute | Description |
|-----------|-------------|
| `querytype` | View type: `0` = Public View, `1` = Quick Find, `2` = Advanced Find, `4` = Lookup |
| `isdefault` | Is this the default view for the entity (Boolean) |
| `isquickfindquery` | Is this a quick find view (Boolean) |
| `fetchxml` | The FetchXML query definition (CDATA section) |
| `layoutxml` | Column layout and display configuration |

## Advanced Patterns

### Pagination

Use `page` and `count` attributes for paging through large result sets:

```xml
<fetch page="2" count="50">
  <entity name="mnp_application">
    <attribute name="mnp_name" />
  </entity>
</fetch>
```

**Best Practice**: Use `paging-cookie` from previous results for better performance:

```xml
<fetch page="2" count="50" paging-cookie="&lt;cookie page='1'&gt;...&lt;/cookie&gt;">
  <entity name="mnp_application">
    <attribute name="mnp_name" />
  </entity>
</fetch>
```

[Learn more about paging](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/page-results)

### Aggregation Query

```xml
<fetch aggregate="true">
  <entity name="mnp_application">
    <attribute name="mnp_amount" aggregate="sum" alias="total_amount" />
    <attribute name="mnp_amount" aggregate="avg" alias="avg_amount" />
    <attribute name="mnp_applicationid" aggregate="count" alias="count" />
    <attribute name="mnp_status" groupby="true" alias="status" />
    <attribute name="createdon" groupby="true" dategrouping="month" alias="month" />
  </entity>
</fetch>
```

Returns grouped totals by status and month.

[Learn more about aggregation](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/aggregate-data)

### Distinct Results

```xml
<fetch distinct="true">
  <entity name="mnp_application">
    <attribute name="mnp_contactid" />
  </entity>
</fetch>
```

Returns unique contacts who have applications (removes duplicates).

[Learn more about distinct results](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/overview#return-distinct-results)

### Top N Results

```xml
<fetch top="10">
  <entity name="account">
    <attribute name="name" />
    <attribute name="revenue" />
    <order attribute="revenue" descending="true" />
  </entity>
</fetch>
```

Returns top 10 accounts by revenue. Maximum value is 5,000.

⚠️ Don't use `top` with `page`, `count`, or `returntotalrecordcount`.

### Complex Filter Logic

```xml
<filter type="and">
  <condition attribute="statecode" operator="eq" value="0" />
  <filter type="or">
    <filter type="and">
      <condition attribute="mnp_priority" operator="eq" value="120310000" />
      <condition attribute="mnp_amount" operator="gt" value="5000" />
    </filter>
    <filter type="and">
      <condition attribute="mnp_urgent" operator="eq" value="1" />
      <condition attribute="ownerid" operator="eq-userid" />
    </filter>
  </filter>
</filter>
```

**Logic**: Active AND ((High Priority AND Amount > 5000) OR (Urgent AND Owned by Me))

### Count Total Records

```xml
<fetch returntotalrecordcount="true" count="50" page="1">
  <entity name="account">
    <attribute name="name" />
  </entity>
</fetch>
```

Response includes total count of all records matching criteria (not just current page).

[Learn more about counting rows](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/count-rows)

### Filter on Related Records

```xml
<entity name="account">
  <attribute name="name" />
  <filter>
    <link-entity name="contact" from="accountid" to="accountid" link-type="any">
      <filter>
        <condition attribute="statecode" operator="eq" value="0" />
        <condition attribute="lastname" operator="eq" value="Smith" />
      </filter>
    </link-entity>
  </filter>
</entity>
```

Returns accounts that have **any** active contact with lastname "Smith".

[Learn more about filtering on related records](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/filter-rows#filter-on-values-in-related-records)

## Parsing Strategy

When analyzing FetchXML in Dynamics 365 solutions, use this systematic approach:

### 1. Identify Query Scope

- **Primary entity**: What table is the main focus (`<entity name="...">`)?
- **Query type**: Is it aggregate, distinct, or standard retrieval?
- **Pagination**: Check for `page`, `count`, `top`, or `paging-cookie`
- **Limits**: Note any `aggregatelimit` or `top` restrictions

### 2. Map Returned Columns

- **Direct attributes**: List all `<attribute>` elements from entity
- **Linked attributes**: Track `<attribute>` elements from `<link-entity>` with their aliases
- **Aggregates**: Note aggregate functions and aliases
- **All-attributes**: Flag if `<all-attributes>` is used (performance concern)

### 3. Parse Filter Logic

- **Primary filters**: Conditions directly on the entity
- **Nested logic**: Map `and`/`or` filter nesting structure
- **Link-entity filters**: Conditions on related tables
- **Special operators**: Note user context (`eq-userid`), date relative (`last-x-days`), etc.
- **Filter on related**: Look for `link-type="any"` or `link-type="not any"` in filters

### 4. Understand Joins

- **Relationship type**: Many-to-one, one-to-many, many-to-many
- **Join type**: `inner`, `outer`, `any`, `not any`, `exists`, `in`, etc.
- **Purpose**: Data retrieval vs. filtering only (check for `intersect="true"`)
- **Nested structure**: Map multi-level join hierarchy
- **Auto-generated aliases**: Track which link-entities have explicit vs. auto-generated aliases

### 5. Determine Sort Order

- **Primary sorts**: `<order>` elements in entity
- **Link-entity sorts**: `<order>` elements in link-entities
- **Processing order**: Check for `entityname` attribute to control order precedence
- **Aggregate sorting**: Note sorting on aggregate aliases

### 6. Context Analysis

- **View context**: In SavedQuery, note `querytype`, `isdefault`, `isquickfindquery`
- **Workflow context**: Part of a workflow step?
- **Report context**: SSRS report data source?
- **SDK context**: Used in custom code?

### 7. Performance Indicators

- **All-attributes usage**: Performance red flag
- **Distinct without need**: May slow queries
- **Complex nested filters**: Potential performance impact
- **No pagination**: Risk of timeout on large datasets
- **Link-type optimization**: Use of `exists`, `in`, or `matchfirstrowusingcrossapply`
- **Late materialize**: Check for `latematerialize="true"`
- **Options hints**: Note any SQL optimization options

### 8. Document Findings

Create structured documentation including:
- **Purpose**: What business requirement does this query serve?
- **Tables involved**: Entity and all linked entities
- **Data returned**: Column list with aliases
- **Filter criteria**: Plain language description of conditions
- **Performance notes**: Concerns or optimizations
- **Relationships used**: Named relationships being traversed
- **Business logic**: Translation of complex filters to business rules

## Common Issues and Best Practices

### Issues to Watch For

#### 1. Case-Sensitive Logical Names

❌ **Wrong**: `mnp_Application`, `ContactID`  
✅ **Correct**: `mnp_application`, `contactid`

Logical names are case-sensitive. Always use lowercase.

#### 2. Ambiguous Attributes in Joins

```xml
<!-- ❌ May fail if multiple entities have 'name' -->
<condition attribute="name" operator="eq" value="Test" />

<!-- ✅ Specify entity using alias -->
<condition attribute="name" operator="eq" value="Test" entityname="contact" />
```

#### 3. from/to Direction Confusion

```xml
<!-- Link direction: from Related TO Parent -->
<link-entity name="contact" from="contactid" to="primarycontactid">
```

- **from**: Column in the related table (contact)
- **to**: Column in the parent table (account)

⚠️ **Note**: FetchXML `from`/`to` are **opposite** of QueryExpression `LinkFromAttributeName`/`LinkToAttributeName`

#### 4. Missing Alias for Multiple Joins

```xml
<!-- ❌ Second join to same table needs explicit alias -->
<link-entity name="contact" from="contactid" to="primarycontactid">
<link-entity name="contact" from="contactid" to="secondarycontactid">

<!-- ✅ Use distinct aliases -->
<link-entity name="contact" from="contactid" to="primarycontactid" alias="primarycontact">
<link-entity name="contact" from="contactid" to="secondarycontactid" alias="secondarycontact">
```

#### 5. Mismatched Column Types

```xml
<!-- ❌ Joining string to GUID causes performance issues -->
<link-entity name="contact" from="emailaddress1" to="customerid">

<!-- ✅ Join on matching types -->
<link-entity name="contact" from="contactid" to="customerid">
```

Column types in `from` and `to` must match or Dataverse forces type conversion with severe performance penalty.

#### 6. Date Format Issues

❌ **Wrong**: `2024-02-18`, `02/18/2024`  
✅ **Correct**: `2024-02-18T00:00:00Z` (ISO 8601 with time)

Always use ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`

#### 7. String Value Escaping

For values containing XML special characters:

```xml
<!-- Use CDATA for complex strings -->
<condition attribute="description" operator="like">
  <value><![CDATA[<test> & "quotes"]]></value>
</condition>

<!-- Or XML entity encoding -->
<condition attribute="description" operator="like" value="&lt;test&gt; &amp; &quot;quotes&quot;" />
```

#### 8. top with Other Attributes

```xml
<!-- ❌ Don't combine top with pagination -->
<fetch top="10" page="2" count="50">

<!-- ✅ Use one or the other -->
<fetch top="10">
<!-- OR -->
<fetch page="2" count="50">
```

### Performance Best Practices

1. **Always specify columns**: Never use `<all-attributes>` in production
2. **Use appropriate link-types**: Consider `exists`, `in`, or `matchfirstrowusingcrossapply` for filtering
3. **Add paging for large datasets**: Use `count` and `page` to avoid timeouts
4. **Minimize nested joins**: Each level adds complexity and time
5. **Index aware filters**: Filter on indexed columns when possible
6. **Limit top results**: Set reasonable `top` values (max 5,000)
7. **Use aggregate limits**: Set `aggregatelimit` below 50,000 when appropriate
8. **Consider late materialize**: Use `latematerialize="true"` for complex queries with large intermediate results

### Validation Checklist

- [ ] All logical names are lowercase
- [ ] Aliases used for multiple joins to same table
- [ ] `from`/`to` columns are same type
- [ ] Date values in ISO 8601 format
- [ ] XML special characters properly escaped
- [ ] No `<all-attributes>` usage
- [ ] Pagination implemented for large result sets
- [ ] Filter conditions use appropriate operators
- [ ] Aggregate queries include groupby attributes
- [ ] link-type matches intended join behavior

## Additional Resources

- **Official FetchXML Reference**: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/reference/
- **Query Data Guide**: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/overview
- **Select Columns**: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/select-columns
- **Join Tables**: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/join-tables
- **Filter Rows**: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/filter-rows
- **Aggregate Data**: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/aggregate-data
- **Page Results**: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/page-results
- **Optimize Performance**: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/optimize-performance
- **Operators Reference**: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/reference/operators
