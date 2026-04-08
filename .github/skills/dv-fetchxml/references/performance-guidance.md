# FetchXML Performance Guidance

Sources:
- https://learn.microsoft.com/en-us/power-apps/developer/data-platform/query-antipatterns
- https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/optimize-performance

[[_TOC_]]

## Anti-Patterns to Detect and Fix

When reviewing a FetchXML query, check for each of the following. Report any found before executing.

### 1. Unbounded Query (no `top`, `count`, or filter)

```xml
<!-- BAD: returns up to 5,000 rows with no bound -->
<fetch>
  <entity name="account">
    <all-attributes />
  </entity>
</fetch>

<!-- GOOD -->
<fetch top="100">
  <entity name="account">
    <attribute name="name" />
    <filter>
      <condition attribute="statecode" operator="eq" value="0" />
    </filter>
  </entity>
</fetch>
```

Always add `top` or `count`+`page` unless deliberately retrieving all records. Always add a `<filter>` on indexed columns (e.g., `statecode`, `createdon`) on large tables.

---

### 2. Selecting All Attributes (`<all-attributes>`)

Error identifier: `LargeAmountOfAttributes`

```xml
<!-- BAD -->
<all-attributes />

<!-- GOOD: select only what is needed -->
<attribute name="name" />
<attribute name="statuscode" />
<attribute name="createdon" />
```

Returns all columns including large text and logical columns. Always use explicit `<attribute>` elements.

---

### 3. Too Many Logical Columns

Error identifier: `LargeAmountOfLogicalAttributes`

Logical columns store values across multiple database tables (check `IsLogical` in metadata). Requesting many logical columns forces Dataverse to perform extra joins. Minimize them.

---

### 4. Leading Wildcard in `like` Condition

Error identifier: `PerformanceLeadingWildCard`  
Dataverse error: `LeadingWildcardCauseTimeout` (0x80048573)

```xml
<!-- BAD: leading % forces full table scan -->
<condition attribute="accountnumber" operator="like" value="%234" />

<!-- Also bad: ends-with, contains -->
<condition attribute="name" operator="ends-with" value="Corp" />

<!-- GOOD: starts-with is index-friendly -->
<condition attribute="name" operator="begins-with" value="Contoso" />
```

Use Dataverse Search for full-text or suffix matching instead.

---

### 5. Filtering on Calculated or Formula Columns

Error identifier: `FilteringOnCalculatedColumns`  
Dataverse error: `ComputedColumnCauseTimeout` (0x80048574)

Calculated/formula column values are computed at runtime per row. Filtering on them forces full-table evaluation. Move the logic to a real persisted column if you need to filter.

---

### 6. Ordering by Choice Columns

Error identifier: `OrderOnEnumAttribute`

```xml
<!-- BAD: sorts by localized label, requires extra join -->
<order attribute="statuscode" />

<!-- GOOD: use useraworderby to sort by integer value instead -->
```

Or set `<fetch useraworderby="true">` to sort by the stored integer rather than the localized label.

---

### 7. Ordering by Columns in Related Tables

Error identifier: `OrderOnPropertiesFromJoinedTables`

```xml
<!-- BAD -->
<link-entity name="contact" from="contactid" to="primarycontactid" alias="ct">
  <attribute name="fullname" />
</link-entity>
<order attribute="fullname" entityname="ct" />
```

Sort by a column on the root entity when possible. Only order by linked table columns when necessary.

---

### 8. Filtering on Large Text Columns

Error identifier: `PerformanceLargeColumnSearch`

- `StringAttributeMetadata` with `MaxLength > 850` — not indexed
- `MemoAttributeMetadata` (multi-line text) — never indexed

Use Dataverse Search for full-text queries on these columns.

---

### 9. Deep Link-Entity Chains

More than 3–4 `link-entity` levels significantly increases query complexity. Consider denormalizing data or splitting into multiple queries.

---

### 10. Aggregate Queries Without Tight Filters

Aggregate queries are limited to 50,000 records. Without filters, queries against large tables hit `AggregateQueryRecordLimit exceeded` (error `8004E023`).

Always add a filter to reduce the record set:
```xml
<fetch aggregate="true">
  <entity name="mnp_payment">
    <filter>
      <condition attribute="createdon" operator="last-x-months" value="3" />
    </filter>
    ...
  </entity>
</fetch>
```

Use `aggregatelimit` for a soft cap that returns partial results instead of an error.

---

## FetchXML-Specific Optimizations

### Late Materialize

For queries with many joins and lookup/computed columns that run slowly, try:

```xml
<fetch latematerialize="true">
  ...
</fetch>
```

This breaks the query into smaller parts. Most beneficial for: many joins + many lookup/computed columns. May slow down simple queries.

### Union Hint

For `OR` filters across related tables, the `union` hint can improve performance:

```xml
<filter type="or" hint="union">
  <condition attribute="telephone1" operator="eq" value="555-1234" entityname="ac" />
  <condition attribute="telephone1" operator="eq" value="555-1234" entityname="co" />
</filter>
```

Restrictions: filter must be `type="or"`, only one `union` hint per query, hint must be within 3 levels deep.

### Query Options (SQL Hints — Support Use Only)

Only apply when recommended by Microsoft support:

| Option | SQL Hint |
|---|---|
| `HashJoin` | Hash Join |
| `MergeJoin` | Merge Join |
| `LoopJoin` | Loop Join |
| `ForceOrder` | Force Order |
| `DisableRowGoal` | DISABLE_OPTIMIZER_ROWGOAL |
| `NO_PERFORMANCE_SPOOL` | NO_PERFORMANCE_SPOOL |

```xml
<fetch options="HashJoin,DisableRowGoal">
```

---

## Paging Best Practices

- Always include `<order>` when paging — without it results are nondeterministic.
- Include the primary key as a final tiebreaker order to guarantee determinism:
  ```xml
  <order attribute="createdon" descending="true" />
  <order attribute="accountid" />
  ```
- Use paging cookies (`paging-cookie`) instead of simple page increments for datasets > 5,000 rows.
- Simple paging (no cookie) is limited to 50,000 total rows and degrades with page number.
- Do not use `top` and `count`/`page` together.
- Max page size: 5,000 for standard tables, 500 for elastic tables.

---

## Dataverse Error Codes

| Error | Code | Cause |
|---|---|---|
| `LeadingWildcardCauseTimeout` | 0x80048573 | Leading `%` wildcard |
| `ComputedColumnCauseTimeout` | 0x80048574 | Filter on calculated column |
| `PerformanceValidationIssuesCauseTimeout` | 0x80048575 | Multiple anti-patterns |
| `AggregateQueryRecordLimit exceeded` | 8004E023 | Aggregate > 50,000 records |
