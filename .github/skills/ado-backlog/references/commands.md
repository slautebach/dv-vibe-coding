# az boards Command Reference

> Source: [learn.microsoft.com/en-us/cli/azure/boards](https://learn.microsoft.com/en-us/cli/azure/boards?view=azure-cli-latest)  
> Extension: `azure-devops` (Azure CLI 2.30.0+). Auto-installs on first `az boards` command.

## Table of Contents
- [Configuration](#configuration)
- [az boards query](#az-boards-query)
- [az boards work-item](#az-boards-work-item)
- [az boards work-item relation](#az-boards-work-item-relation)
- [az boards area project](#az-boards-area-project)
- [az boards iteration project](#az-boards-iteration-project)
- [az boards iteration team](#az-boards-iteration-team)
- [Output & Filtering](#output--filtering)

---

## Configuration

```bash
# Set org/project defaults — avoids --org / --project on every command
az devops configure --defaults organization=https://dev.azure.com/<org> project=<project>

# View current defaults
az devops configure --list

# Clear defaults
az devops configure --defaults organization="" project=""
```

Common flags on every command (omit when defaults are set):

| Flag | Short | Description |
|---|---|---|
| `--org` / `--organization` | | ADO org URL, e.g. `https://dev.azure.com/MyOrg/` |
| `--project` | `-p` | Project name or ID |
| `--detect` | | `true`/`false` — auto-detect org from git config |
| `--output` | `-o` | `json` (default), `table`, `tsv`, `yaml`, `jsonc`, `none` |
| `--query` | | JMESPath filter on output |

---

## az boards query

Query for a list of work items. **Only supports flat queries.**

```
az boards query [--id] [--path] [--wiql] [--detect] [--org] [--project]
```

Exactly one of `--id`, `--path`, or `--wiql` is required.

| Flag | Description |
|---|---|
| `--wiql` | WIQL string. Ignored if `--id` or `--path` specified. |
| `--id` | ID of a saved query in ADO. |
| `--path` | Path of a saved query (ignored if `--id` given). |

```bash
# Run inline WIQL
az boards query --wiql "SELECT [System.Id],[System.Title],[System.State] \
  FROM WorkItems WHERE [System.TeamProject] = @project \
  AND [System.IterationPath] = @CurrentIteration \
  ORDER BY [System.ChangedDate] DESC"

# Run a saved query by ID
az boards query --id <query-guid>

# Run a saved query by path
az boards query --path "Shared Queries/My Team/Active Items"
```

---

## az boards work-item

### work-item create

```
az boards work-item create --title <title> --type <type>
                           [--area] [--assigned-to] [--description]
                           [--discussion] [--fields] [--iteration]
                           [--open] [--org] [--project] [--reason]
```

| Flag | Req | Description |
|---|---|---|
| `--title` | ✅ | Title of the work item |
| `--type` | ✅ | Work item type name, e.g. `Bug`, `User Story`, `Task` |
| `--area` | | Area path (e.g. `Demos`) |
| `--assigned-to` | | Person name or email |
| `--description` / `-d` | | Description (HTML or plain text) |
| `--discussion` | | Comment to add to discussion thread |
| `--fields` / `-f` | | Space-separated `"field=value"` pairs for custom fields |
| `--iteration` | | Iteration path (e.g. `Demos\\Iteration 1`) |
| `--open` | | Open in default web browser after creation |
| `--reason` | | Reason for the initial state |

```bash
az boards work-item create \
  --type "User Story" \
  --title "As a user I can reset my password" \
  --assigned-to "user@example.com" \
  --iteration "MyProject\\Sprint 5" \
  --description "Acceptance criteria: ..." \
  --fields "Microsoft.VSTS.Common.Priority=2" "Microsoft.VSTS.Scheduling.StoryPoints=5"
```

### work-item show

```
az boards work-item show --id <id>
                         [--as-of] [--expand] [--fields] [--open] [--org]
```

| Flag | Description |
|---|---|
| `--id` ✅ | Work item ID |
| `--as-of` | Return state as of date/time. E.g. `'2024-01-20'`, `'2024-01-20 00:20:00 UTC'` |
| `--expand` | `all` (default), `fields`, `links`, `relations`, `none` |
| `--fields` / `-f` | Comma-separated list of fields to return |
| `--open` | Open in browser |

```bash
az boards work-item show --id 1234
az boards work-item show --id 1234 --expand fields
az boards work-item show --id 1234 --as-of "2024-03-01"
```

### work-item update

```
az boards work-item update --id <id>
                           [--area] [--assigned-to] [--description]
                           [--discussion] [--fields] [--iteration]
                           [--open] [--org] [--reason] [--state] [--title]
```

| Flag | Req | Description |
|---|---|---|
| `--id` | ✅ | ID of the work item to update |
| `--state` | | New state (e.g. `Active`, `Resolved`, `Done`) |
| `--assigned-to` | | New assignee |
| `--title` | | New title |
| `--iteration` | | New iteration path |
| `--area` | | New area path |
| `--discussion` | | Add a comment to the discussion thread |
| `--fields` / `-f` | | Space-separated `"field=value"` pairs |
| `--reason` | | Reason for state change |

```bash
az boards work-item update --id 1234 --state "Active" --assigned-to "user@example.com"
az boards work-item update --id 1234 --fields "Microsoft.VSTS.Scheduling.StoryPoints=8"
```

### work-item delete

```
az boards work-item delete --id <id> [--destroy] [--yes] [--org] [--project]
```

| Flag | Description |
|---|---|
| `--id` ✅ | Work item ID |
| `--destroy` | Permanently delete (cannot be restored). Default: `false` (soft delete) |
| `--yes` / `-y` | Skip confirmation prompt |

```bash
az boards work-item delete --id 1234 --yes
az boards work-item delete --id 1234 --destroy --yes   # permanent
```

---

## az boards work-item relation

### relation add

```
az boards work-item relation add --id <id> --relation-type <type>
                                 [--target-id] [--target-url] [--org]
```

> `--relation-type` accepts **friendly names** (e.g. `parent`, `child`) — not system reference names.

| Flag | Req | Description |
|---|---|---|
| `--id` | ✅ | Source work item ID |
| `--relation-type` | ✅ | Relation type. E.g. `parent`, `child` |
| `--target-id` | | Target work item ID(s), comma-separated. E.g. `1,2` |
| `--target-url` | | Target work item URL(s), comma-separated |

```bash
# Set parent
az boards work-item relation add --id 456 --relation-type parent --target-id 123

# Add multiple children at once
az boards work-item relation add --id 100 --relation-type child --target-id 201,202,203
```

### relation remove

```
az boards work-item relation remove --id <id> --relation-type <type> --target-id <ids>
                                    [--yes] [--org]
```

| Flag | Req | Description |
|---|---|---|
| `--id` | ✅ | Source work item ID |
| `--relation-type` | ✅ | Relation type to remove (e.g. `parent`, `child`) |
| `--target-id` | ✅ | Target ID(s) to remove, comma-separated |
| `--yes` / `-y` | | Skip confirmation |

```bash
az boards work-item relation remove --id 456 --relation-type parent --target-id 123 --yes
```

### relation show

Returns work item with relations resolved to friendly names.

```
az boards work-item relation show --id <id> [--org]
```

### relation list-type

List all relation types supported by the organization.

```
az boards work-item relation list-type [--org]
```

```bash
# Discover all available relation type names
az boards work-item relation list-type --output table
```

---

## az boards area project

| Command | Description |
|---|---|
| `az boards area project list` | List project areas |
| `az boards area project show` | Show area by ID |
| `az boards area project create` | Create a new area |
| `az boards area project update` | Rename or move an area |
| `az boards area project delete` | Delete an area |

### list

```bash
az boards area project list --depth 3
az boards area project list --path "\\MyProject\\Backend"
```

`--depth` defaults to `1`. Use `3` or higher to see the full tree.

### create

```bash
az boards area project create --name "Payment Services" \
  --path "\\MyProject\\Backend"
```

Creates at root if `--path` is omitted.

### update

```bash
# Rename
az boards area project update --path "\\MyProject\\Backend\\OldName" --name "NewName"

# Move as child of another area
az boards area project update --path "\\MyProject\\AreaToMove" --child-id <target-area-id>
```

### delete

```bash
az boards area project delete --path "\\MyProject\\Backend\\OldArea" --yes
```

---

## az boards iteration project

| Command | Description |
|---|---|
| `az boards iteration project list` | List project iterations |
| `az boards iteration project show` | Show iteration by ID |
| `az boards iteration project create` | Create a sprint/iteration |
| `az boards iteration project update` | Rename, move, or set dates |
| `az boards iteration project delete` | Delete an iteration |

### list

```bash
az boards iteration project list --depth 3
```

### create

```bash
az boards iteration project create \
  --name "Sprint 6" \
  --path "\\MyProject\\Release 1" \
  --start-date "2024-04-01" \
  --finish-date "2024-04-14"
```

Creates at root if `--path` is omitted. Dates format: `"YYYY-MM-DD"`.

### update

```bash
# Rename and update dates
az boards iteration project update \
  --path "\\MyProject\\Sprint 6" \
  --name "Sprint 6 - Updated" \
  --start-date "2024-04-01" \
  --finish-date "2024-04-14"

# Move as child of another iteration
az boards iteration project update --path "\\MyProject\\Sprint6" --child-id <target-id>
```

### delete

```bash
az boards iteration project delete --path "\\MyProject\\Sprint 6" --yes
```

---

## az boards iteration team

| Command | Description |
|---|---|
| `az boards iteration team list` | List team's assigned iterations |
| `az boards iteration team list-work-items` | List work items for a specific iteration |
| `az boards iteration team add` | Assign an iteration to a team |
| `az boards iteration team remove` | Remove iteration from team |
| `az boards iteration team show-backlog-iteration` | Show the team's backlog iteration |
| `az boards iteration team set-backlog-iteration` | Set the team's backlog iteration |
| `az boards iteration team show-default-iteration` | Show the team's default iteration |
| `az boards iteration team set-default-iteration` | Set the team's default iteration |

### list

```bash
az boards iteration team list --team "My Team"
az boards iteration team list --team "My Team" --timeframe current
```

`--timeframe` only supports `current`.

### list-work-items

```bash
az boards iteration team list-work-items --team "My Team" --id <iteration-id>
```

### add / remove

```bash
az boards iteration team add --team "My Team" --id <iteration-id>
az boards iteration team remove --team "My Team" --id <iteration-id>
```

### set-default-iteration

```bash
# By iteration ID
az boards iteration team set-default-iteration --team "My Team" --id <iteration-id>

# By macro
az boards iteration team set-default-iteration --team "My Team" \
  --default-iteration-macro "@CurrentIteration"
```

### set-backlog-iteration

```bash
az boards iteration team set-backlog-iteration --team "My Team" --id <iteration-id>
```

---

## Output & Filtering

All commands support `--output` / `-o` and `--query` (JMESPath).

| Output format | Flag |
|---|---|
| JSON (default) | `-o json` |
| Table | `-o table` |
| Tab-separated | `-o tsv` |
| YAML | `-o yaml` |

### Useful JMESPath patterns

```bash
# ID, Title, State, Assignee from a query result
az boards query --wiql "..." \
  --query "value[].{ID:id, Title:fields.\"System.Title\", State:fields.\"System.State\", Assignee:fields.\"System.AssignedTo\"}" \
  --output table

# All fields for a work item
az boards work-item show --id 1234 --query "fields"

# Filter query results to only Active items
az boards query --wiql "..." --query "value[?fields.\"System.State\"=='Active']"

# Count results
az boards query --wiql "..." --query "length(value)"

# Get iteration path of a work item
az boards work-item show --id 1234 --query "fields.\"System.IterationPath\""

# List only iteration names from project list
az boards iteration project list --depth 3 --query "children[].name" --output tsv
```
