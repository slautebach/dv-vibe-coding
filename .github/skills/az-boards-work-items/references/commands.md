# Az Boards Work Item — Full Command Reference

## Contents
- [Configuration](#configuration)
- [work-item show](#work-item-show)
- [work-item update](#work-item-update)
- [work-item create](#work-item-create)
- [work-item delete](#work-item-delete)
- [work-item relation](#work-item-relation)
- [boards query](#boards-query)
- [Output formats](#output-formats)

> **Official docs:** [az boards — Azure CLI reference](https://learn.microsoft.com/en-us/cli/azure/boards?view=azure-cli-latest)

---

## Configuration

```bash
# Set persistent defaults
az devops configure -d organization=https://dev.azure.com/OrgName project=ProjectName

# View current defaults
az devops configure --list
```

Once defaults are set, `--org` and `--project` are optional on all commands.

---

## work-item show

```
az boards work-item show --id <int>
    [--as-of <datetime>]          # Historical snapshot, e.g. '2024-01-20'
    [--expand {all,fields,links,none,relations}]  # Default: all
    [--fields <comma-separated>]  # e.g. System.Id,System.Title
    [--org <url>]
    [--output {json,table,tsv,yaml}]
```

**Examples:**
```bash
az boards work-item show --id 42
az boards work-item show --id 42 --output table
az boards work-item show --id 42 --fields "System.Id,System.Title,System.State" --output table
az boards work-item show --id 42 --as-of "2024-06-01"
```

---

## work-item update

```
az boards work-item update --id <int>
    [--area <path>]               # e.g. "MyProject\Team"
    [--assigned-to <name/email>]
    [--description <text>]
    [--discussion <comment>]      # Appends comment to discussion thread
    [--fields <"field=value" ...>] # Space-separated pairs
    [--iteration <path>]          # e.g. "MyProject\Sprint 3"
    [--reason <text>]
    [--state <text>]              # e.g. "Active", "Closed", "Resolved"
    [--title <text>]
    [--org <url>]
    [--project <name>]
```

**Examples:**
```bash
# Change state
az boards work-item update --id 42 --state "Resolved"

# Assign and set priority via custom field
az boards work-item update --id 42 --assigned-to "jane@example.com" \
  --fields "Microsoft.VSTS.Common.Priority=2"

# Add a discussion comment
az boards work-item update --id 42 --discussion "Fixed in PR #99, ready for review."

# Move to a sprint
az boards work-item update --id 42 --iteration "MyProject\Sprint 5"

# Multiple fields at once
az boards work-item update --id 42 \
  --fields "Microsoft.VSTS.Scheduling.RemainingWork=3" "System.Tags=backend;auth"
```

---

## work-item create

```
az boards work-item create --title <text> --type <type>
    [--area <path>]
    [--assigned-to <name/email>]
    [--description <text>]
    [--discussion <comment>]
    [--fields <"field=value" ...>]
    [--iteration <path>]
    [--reason <text>]
    [--org <url>]
    [--project <name>]
```

**Common work item types:** `Bug`, `Task`, `User Story`, `Feature`, `Epic`, `Issue`, `Product Backlog Item`

**Examples:**
```bash
# Create a bug
az boards work-item create --title "NullRef in checkout" --type Bug \
  --assigned-to "dev@example.com" --state "Active"

# Create a task under a sprint
az boards work-item create --title "Write integration tests" --type Task \
  --iteration "MyProject\Sprint 3" \
  --fields "Microsoft.VSTS.Scheduling.RemainingWork=4"

# Create a User Story with description
az boards work-item create --title "User can reset password" --type "User Story" \
  --description "As a registered user, I want to reset my password via email."
```

---

## work-item delete

```
az boards work-item delete --id <int>
    [--destroy]   # Permanent delete (cannot be recovered)
    [--yes]       # Skip confirmation prompt
    [--org <url>]
    [--project <name>]
```

> **Warning:** `--destroy` is irreversible. Omitting it sends to recycle bin.

---

## work-item relation

### Add relation
```
az boards work-item relation add --id <int> --relation-type <type>
    [--target-id <int,...>]   # Comma-separated IDs
    [--target-url <url,...>]
    [--org <url>]
```

```bash
# Link as child
az boards work-item relation add --id 200 --relation-type child --target-id 201,202

# Link as parent
az boards work-item relation add --id 200 --relation-type parent --target-id 100
```

### Remove relation
```bash
az boards work-item relation remove --id 200 --relation-type child --target-id 201 --yes
```

### Show with friendly relation names
```bash
az boards work-item relation show --id 200
```

### List available relation types
```bash
az boards work-item relation list-type
```

**Common relation types:** `parent`, `child`, `related`, `duplicate`, `duplicate-of`, `successor`, `predecessor`

---

## boards query

```
az boards query
    [--id <query-guid>]          # Run saved query by GUID
    [--wiql <wiql-string>]       # Inline WIQL query
    [--path <query-path>]        # Run saved query by path
    [--org <url>]
    [--project <name>]
    [--output {json,table,tsv}]
```

**Examples:**
```bash
# All active bugs in the project
az boards query --wiql "SELECT [System.Id],[System.Title],[System.State],[System.AssignedTo] \
  FROM workitems WHERE [System.TeamProject] = @project AND [System.WorkItemType] = 'Bug' \
  AND [System.State] <> 'Closed' ORDER BY [System.ChangedDate] DESC" --output table

# Items assigned to current user
az boards query --wiql "SELECT [System.Id],[System.Title] FROM workitems \
  WHERE [System.AssignedTo] = @me AND [System.State] = 'Active'"

# Run a saved query by GUID
az boards query --id "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

**Useful WIQL macros:** `@project`, `@me`, `@today`, `@currentIteration`

---

## Output Formats

| Flag | Use case |
|------|----------|
| `--output json` | Default; full detail |
| `--output table` | Human-readable summary |
| `--output tsv` | Scripting/parsing |
| `--output yaml` | YAML format |

**JMESPath filtering** (use with `--query`):
```bash
# Extract just title and state
az boards work-item show --id 42 \
  --query "{id:id, title:fields.\"System.Title\", state:fields.\"System.State\"}"

# Get display name of assigned user
az boards work-item show --id 42 --query "fields.\"System.AssignedTo\".displayName"
```
