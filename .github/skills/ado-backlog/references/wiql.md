# WIQL Query Reference

Work Item Query Language (WIQL) is SQL-like syntax for querying ADO work items.

## Table of Contents
- [Basic Syntax](#basic-syntax)
- [Common Macros](#common-macros)
- [Common Query Patterns](#common-query-patterns)
- [Operators & Functions](#operators--functions)

---

## Basic Syntax

```sql
SELECT [field1], [field2], ...
FROM WorkItems
WHERE <conditions>
ORDER BY [field] ASC|DESC
```

Field names must be wrapped in square brackets. Use the reference name (e.g., `[System.State]`), not the display name.

Run a query:
```bash
az boards query --wiql "SELECT [System.Id],[System.Title],[System.State] \
  FROM WorkItems WHERE [System.TeamProject] = @project \
  ORDER BY [System.ChangedDate] DESC"
```

---

## Common Macros

| Macro | Expands to |
|---|---|
| `@project` | Current default project |
| `@me` | Currently authenticated user |
| `@CurrentIteration` | Active sprint for the team |
| `@CurrentIteration + 1` | Next sprint |
| `@CurrentIteration - 1` | Previous sprint |
| `@StartOfDay` | Midnight today (UTC) |
| `@StartOfWeek` | Start of current week |
| `@StartOfMonth` | Start of current month |
| `@Today` | Today's date |
| `@Today - 7` | 7 days ago |

`@CurrentIteration` requires a team context. Specify it with:
```sql
@CurrentIteration('[project]\[team]')
```

---

## Common Query Patterns

### All items in current sprint
```sql
SELECT [System.Id],[System.Title],[System.State],[System.AssignedTo],[System.WorkItemType]
FROM WorkItems
WHERE [System.TeamProject] = @project
  AND [System.IterationPath] = @CurrentIteration
ORDER BY [System.WorkItemType], [System.State]
```

### My active items
```sql
SELECT [System.Id],[System.Title],[System.State],[System.WorkItemType],[System.IterationPath]
FROM WorkItems
WHERE [System.TeamProject] = @project
  AND [System.AssignedTo] = @me
  AND [System.State] <> 'Closed'
  AND [System.State] <> 'Done'
ORDER BY [System.ChangedDate] DESC
```

### Items by assignee
```sql
SELECT [System.Id],[System.Title],[System.State],[System.IterationPath]
FROM WorkItems
WHERE [System.TeamProject] = @project
  AND [System.AssignedTo] = 'First Last <user@example.com>'
  AND [System.State] NOT IN ('Closed', 'Done', 'Removed')
```

### Items by state
```sql
SELECT [System.Id],[System.Title],[System.AssignedTo],[System.WorkItemType]
FROM WorkItems
WHERE [System.TeamProject] = @project
  AND [System.State] = 'Active'
  AND [System.WorkItemType] IN ('User Story', 'Bug', 'Task')
ORDER BY [System.AssignedTo]
```

### Items in a specific sprint
```sql
SELECT [System.Id],[System.Title],[System.State],[System.AssignedTo]
FROM WorkItems
WHERE [System.TeamProject] = @project
  AND [System.IterationPath] = '<project>\Sprint 5'
ORDER BY [System.WorkItemType], [System.State]
```

### Unassigned items in backlog
```sql
SELECT [System.Id],[System.Title],[System.WorkItemType],[System.State]
FROM WorkItems
WHERE [System.TeamProject] = @project
  AND [System.AssignedTo] = ''
  AND [System.State] = 'New'
  AND [System.WorkItemType] IN ('User Story', 'Product Backlog Item', 'Bug')
ORDER BY [Microsoft.VSTS.Common.Priority]
```

### Items changed in the last 7 days
```sql
SELECT [System.Id],[System.Title],[System.State],[System.ChangedBy],[System.ChangedDate]
FROM WorkItems
WHERE [System.TeamProject] = @project
  AND [System.ChangedDate] >= @Today - 7
ORDER BY [System.ChangedDate] DESC
```

### Items by tag
```sql
SELECT [System.Id],[System.Title],[System.State],[System.Tags]
FROM WorkItems
WHERE [System.TeamProject] = @project
  AND [System.Tags] CONTAINS 'backend'
```

### Bugs by severity
```sql
SELECT [System.Id],[System.Title],[System.State],[Microsoft.VSTS.Common.Severity]
FROM WorkItems
WHERE [System.TeamProject] = @project
  AND [System.WorkItemType] = 'Bug'
  AND [Microsoft.VSTS.Common.Severity] IN ('1 - Critical', '2 - High')
  AND [System.State] NOT IN ('Closed', 'Done')
ORDER BY [Microsoft.VSTS.Common.Severity]
```

### Children of a specific parent
```sql
SELECT [System.Id],[System.Title],[System.State],[System.AssignedTo]
FROM WorkItemLinks
WHERE [Source].[System.Id] = <parent-id>
  AND [System.Links.LinkType] = 'System.LinkTypes.Hierarchy-Forward'
  AND [Target].[System.WorkItemType] IN ('User Story', 'Task', 'Bug')
MODE (MustContain)
```

---

## Operators & Functions

| Operator | Usage |
|---|---|
| `=` | Exact match |
| `<>` | Not equal |
| `>`, `>=`, `<`, `<=` | Comparison (dates, numbers) |
| `IN (...)` | Match any value in list |
| `NOT IN (...)` | Exclude list |
| `CONTAINS` | String contains substring |
| `CONTAINS WORDS` | Full-text word search |
| `UNDER` | Field value is under a tree node (IterationPath, AreaPath) |
| `IN GROUP` | User is member of an ADO group |
| `WAS EVER` | Field ever held a value |
| `EVER` | Alternative syntax for WAS EVER |

### UNDER operator (area/iteration hierarchy)
```sql
-- All items in Sprint 5 and any child iterations
WHERE [System.IterationPath] UNDER '<project>\Sprint 5'

-- All items in a team area and sub-areas
WHERE [System.AreaPath] UNDER '<project>\Backend Team'
```

### WAS EVER (audit history)
```sql
-- Items that were ever assigned to a specific person
WHERE [System.AssignedTo] WAS EVER 'user@example.com'

-- Items that were ever in Active state
WHERE [System.State] WAS EVER 'Active'
```
