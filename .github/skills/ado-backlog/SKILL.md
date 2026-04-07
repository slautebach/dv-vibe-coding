---
name: ado-backlog
description: Manage Azure DevOps backlog items using the az CLI (azure-devops extension). Use when asked to list, query, create, update, or move work items — including filtering by sprint/iteration, state, assignee, or work item type. Supports multiple orgs and projects via config or explicit flags. Do NOT use for pipeline management (use authoring-azure-devops-pipelines skill) or for solution deployments.
---

# ADO Backlog

Manage Azure DevOps work items from the terminal using the `az boards` CLI.

## Prerequisites

Install the Azure DevOps CLI extension once per machine:

```bash
az extension add --name azure-devops
```

## Authentication

Azure CLI maintains a **cache of multiple logged-in accounts and tenants simultaneously**. ADO auth then has its own layer on top. Both layers need to be correct.

### Layer 1 — Azure CLI account context

```bash
# See all cached logins and which is active
az account list
az account show   # current active context

# Log in (add a new account/tenant to cache)
az login

# Log in to a specific tenant (e.g., a client's Entra ID)
az login --tenant <tenant-id>

# Switch active subscription
az account set --subscription "<subscription name or id>"

# Remove all cached logins and start fresh
az account clear
```

Multiple tenants can be cached at once — you switch between them with `az login --tenant` or `az account set`. Azure CLI has **no named contexts** (unlike Az PowerShell); switching is done via tenant and subscription.

### Layer 2 — ADO-specific auth

`az boards` resolves auth in this order:

1. `AZURE_DEVOPS_EXT_PAT` environment variable — takes priority over everything
2. The active `az login` session (must match the ADO org's tenant)

```bash
# Use a PAT — required when the ADO org's tenant differs from your active az login,
# or when az login isn't practical (automation, CI)
$env:AZURE_DEVOPS_EXT_PAT = "<your-pat>"

# Clear PAT to fall back to az login
Remove-Item Env:AZURE_DEVOPS_EXT_PAT
```

> **`AZURE_DEVOPS_EXT_PAT` is a single global variable.** When working across multiple ADO orgs that belong to different tenants with different PATs, set the correct PAT before each cross-org command block, then restore it after.

### Verify your active context

```bash
az account show                 # which tenant/subscription is active
az devops configure --list      # which ADO org/project are the defaults
```

## Multi-org switching

When the user's request targets a different ADO org or project than the current defaults, follow this pattern:

### Step 1 — Identify the target

Ask the user which project they mean, or infer from context. Check `copilot-instructions.md` for a known org/project registry if one is defined.

### Step 2 — Handle auth for the target org

| Situation | What to do |
|---|---|
| Target org is in the **same tenant** as active `az login` | No auth change needed |
| Target org is in a **different tenant** | `az login --tenant <tenant-id>` to add/refresh that tenant, then `az account set` if needed |
| Target org requires a **PAT** (cross-tenant, automation, or MFA-protected) | `$env:AZURE_DEVOPS_EXT_PAT = "<pat-for-target-org>"` |

### Step 3 — Target the correct org and project

**Option A — explicit flags per command** (safest, no global state change):
```bash
az boards query --wiql "..." \
  --org https://dev.azure.com/<other-org> \
  --project <other-project>
```

**Option B — update defaults for a multi-command session**:
```bash
az devops configure --defaults organization=https://dev.azure.com/<other-org> project=<other-project>
# ... run commands ...
# Restore when done
az devops configure --defaults organization=https://dev.azure.com/<original-org> project=<original-project>
```

> Always restore defaults after Option B — subsequent commands will silently target the wrong project otherwise.

### Step 4 — Confirm before destructive operations

Before creating, updating, or deleting on an unfamiliar project:

```bash
az devops configure --list
az account show
```

## Multi-org quick reference

When `copilot-instructions.md` defines known org/project pairs, use those as the source of truth. Otherwise ask the user.

| Scenario | Auth | Targeting |
|---|---|---|
| Same org as defaults | Nothing | Just run commands |
| Different project, same org | Nothing | Add `--project <project>` |
| Different org, same tenant | Nothing (or `az login --tenant`) | Add `--org <url> --project <project>` |
| Different org, different tenant | `az login --tenant <id>` or set PAT | Add `--org <url> --project <project>` |
| Automation / CI | Set `AZURE_DEVOPS_EXT_PAT` | Use explicit `--org` and `--project` flags |

## Core Workflow

Set defaults once per session before running commands:

```bash
az devops configure --defaults organization=https://dev.azure.com/<org> project=<project>
```

### Query work items
Use WIQL for any non-trivial query. See [references/wiql.md](references/wiql.md) for syntax and common examples.

```bash
az boards query --wiql "SELECT [System.Id],[System.Title],[System.State],[System.AssignedTo] \
  FROM WorkItems WHERE [System.TeamProject] = @project \
  AND [System.IterationPath] = @CurrentIteration \
  ORDER BY [System.ChangedDate] DESC"
```

For quick single-item lookup:
```bash
az boards work-item show --id <id>
```

### Create a work item
```bash
az boards work-item create \
  --type "User Story" \
  --title "As a user I can reset my password" \
  --assigned-to "user@example.com" \
  --iteration "<project>\Sprint 5" \
  --description "Acceptance criteria: ..."
```

See [references/work-item-types.md](references/work-item-types.md) for valid `--type` values, required fields, and state names per process template.

### Update a work item
```bash
az boards work-item update \
  --id <id> \
  --state "Active" \
  --assigned-to "user@example.com"
```

### Move between states
State names depend on the process template (Agile / Scrum / CMMI). See [references/work-item-types.md](references/work-item-types.md) for valid transitions.

```bash
az boards work-item update --id <id> --state "Resolved"
```

## Output Formatting

All commands accept `--output` (`table`, `json`, `tsv`, `yaml`) and `--query` (JMESPath). See [references/commands.md](references/commands.md) for useful JMESPath patterns.

```bash
az boards query --wiql "..." --output table
```
