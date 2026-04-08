---
name: az-boards-work-items
description: "Read, create, and update Azure Boards work items using the Azure CLI (az boards). Use this skill when a user wants to view work item details, update state/fields/assignments, create new work items, add comments/discussion, link work items (parent/child), or query work items via WIQL. Triggers on phrases like 'show work item', 'update work item', 'create task/bug/user story', 'assign work item', 'change state', 'query work items', 'link work item', or 'add comment to work item'."
---

# Az Boards Work Items

Manage Azure DevOps Boards work items via the `az boards` CLI commands.

## Prerequisites

Run the setup script from within any Azure DevOps git repo — it auto-detects the org URL and project from the git remote, logs in, installs the extension, and configures defaults:

```powershell
./.github/skills/az-boards-work-items/scripts/setup-auth.ps1
# Or target a different remote (default is 'origin')
./.github/skills/az-boards-work-items/scripts/setup-auth.ps1 -Remote upstream
```

The script handles all of the following automatically:
- Parses `https://dev.azure.com/{org}/{project}/_git/{repo}`, legacy `visualstudio.com`, and SSH URL formats
- Runs `az login` if not already authenticated
- Installs the `azure-devops` extension if missing
- Runs `az devops configure -d organization=<url> project=<name>`

After setup, `--org` and `--project` flags are optional on all commands.

### Manual install & verification (if you prefer not to run the setup script)

- Install Azure CLI:
  - Windows (winget): `winget install Microsoft.AzureCLI`
  - macOS (Homebrew): `brew install azure-cli`
  - Debian/Ubuntu: `curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash`

- Install or verify Azure DevOps extension (provides `az boards`):

```bash
az extension add --name azure-devops
az extension show --name azure-devops
```

- Authenticate & configure defaults:

```bash
az login
az devops configure -d organization=https://dev.azure.com/<org> project=<project>
```

- Quick verification:

```bash
az boards --help   # confirms the az boards commands are available
az boards work-item show --id 1 --org https://dev.azure.com/<org> --project <project> --output table
```

(If `az boards` is not available after installing the extension, restart your shell or re-run `az extension add --name azure-devops`.)

## Common Prompts

### Show a work item
```bash
az boards work-item show --id 1234
az boards work-item show --id 1234 --output table
# With relations (parent/child links)
az boards work-item relation show --id 1234
```

### Update a work item
```bash
# Change state
az boards work-item update --id 1234 --state "Active"

# Update title and assign
az boards work-item update --id 1234 --title "New Title" --assigned-to "user@example.com"

# Set custom fields (space-separated field=value pairs)
az boards work-item update --id 1234 --fields "Microsoft.VSTS.Common.Priority=1" "System.Tags=tag1;tag2"

# Add a comment/discussion entry
az boards work-item update --id 1234 --discussion "Investigation complete, moving to testing."

# Move to iteration
az boards work-item update --id 1234 --iteration "MyProject\Sprint 3"
```

### Create a work item
```bash
# Bug
az boards work-item create --title "Login fails on mobile" --type Bug --assigned-to "dev@example.com" --state "New"

# User Story / PBI
az boards work-item create --title "As a user I want..." --type "User Story" --area "MyProject\Team Area"

# Task with description and iteration
az boards work-item create --title "Write unit tests" --type Task \
  --description "Cover edge cases for auth module" \
  --iteration "MyProject\Sprint 3"
```

### Query work items
```bash
# Run a WIQL query inline
az boards query --wiql "SELECT [System.Id],[System.Title],[System.State] FROM workitems WHERE [System.TeamProject] = 'MyProject' AND [System.State] = 'Active'"

# Run a saved query by ID
az boards query --id "query-guid-here"

# Output as table for readability
az boards query --wiql "..." --output table
```

### Link work items
```bash
# Add parent link
az boards work-item relation add --id 1234 --relation-type parent --target-id 100

# Add child link
az boards work-item relation add --id 1234 --relation-type child --target-id 567

# List available relation types
az boards work-item relation list-type

# Remove a relation
az boards work-item relation remove --id 1234 --relation-type child --target-id 567 --yes
```

### Bulk read with JMESPath filtering
```bash
# Show only ID, title, and state from a work item
az boards work-item show --id 1234 --query "{id:id, title:fields.\"System.Title\", state:fields.\"System.State\"}"

# Get assigned-to from a work item
az boards work-item show --id 1234 --query "fields.\"System.AssignedTo\".displayName"
```

## Common Field Names

| Field | Reference Name |
|---|---|
| Title | `System.Title` |
| State | `System.State` |
| Assigned To | `System.AssignedTo` |
| Area Path | `System.AreaPath` |
| Iteration Path | `System.IterationPath` |
| Description | `System.Description` |
| Tags | `System.Tags` |
| Priority | `Microsoft.VSTS.Common.Priority` |
| Story Points | `Microsoft.VSTS.Scheduling.StoryPoints` |
| Remaining Work | `Microsoft.VSTS.Scheduling.RemainingWork` |

Use `--fields "RefName=value"` with `update` and `--fields "RefName"` (comma-separated) with `show` to target specific fields.

## Reference

For full parameter details see [references/commands.md](references/commands.md).

Official documentation: [az boards — Azure CLI reference](https://learn.microsoft.com/en-us/cli/azure/boards?view=azure-cli-latest)
