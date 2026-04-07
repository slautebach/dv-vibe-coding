# Work Item Types, Fields & State Machines

## Table of Contents
- [Process Templates](#process-templates)
- [Work Item Types by Template](#work-item-types-by-template)
- [State Machines](#state-machines)
- [Common Field Reference](#common-field-reference)
- [Field Names vs CLI Arguments](#field-names-vs-cli-arguments)

---

## Process Templates

ADO has three built-in process templates. State names and work item types differ between them.

| Template | Story type | Bug tracks as | Typical for |
|---|---|---|---|
| **Agile** | User Story | Requirement or Task | General software projects |
| **Scrum** | Product Backlog Item (PBI) | PBI | Teams using Scrum ceremonies |
| **CMMI** | Requirement | Requirement | Regulated / CMMI-compliant teams |

Determine which template a project uses:
```bash
az devops project show --project <project> --query "capabilities.processTemplate.templateName"
```

---

## Work Item Types by Template

### Agile
| Type | `--type` value | Hierarchy level |
|---|---|---|
| Epic | `Epic` | 1 |
| Feature | `Feature` | 2 |
| User Story | `User Story` | 3 |
| Task | `Task` | 4 (child of Story) |
| Bug | `Bug` | 3 or 4 |
| Test Case | `Test Case` | — |

### Scrum
| Type | `--type` value | Hierarchy level |
|---|---|---|
| Epic | `Epic` | 1 |
| Feature | `Feature` | 2 |
| Product Backlog Item | `Product Backlog Item` | 3 |
| Task | `Task` | 4 |
| Bug | `Bug` | 3 or 4 |
| Impediment | `Impediment` | — |

### CMMI
| Type | `--type` value |
|---|---|
| Epic | `Epic` |
| Feature | `Feature` |
| Requirement | `Requirement` |
| Task | `Task` |
| Bug | `Bug` |
| Change Request | `Change Request` |

---

## State Machines

### Agile

| Type | States (in order) | Terminal state |
|---|---|---|
| User Story | New → Active → Resolved → Closed | Closed |
| Bug | Active → Resolved → Closed (also: New) | Closed |
| Task | New → Active → Closed | Closed |
| Feature | New → Active → Resolved → Closed | Closed |
| Epic | New → Active → Resolved → Closed | Closed |

### Scrum

| Type | States (in order) | Terminal state |
|---|---|---|
| PBI | New → Approved → Committed → Done | Done |
| Bug | New → Approved → Committed → Done | Done |
| Task | To Do → In Progress → Done | Done |
| Feature | New → In Progress → Done | Done |
| Epic | New → In Progress → Done | Done |

### CMMI

| Type | States (in order) | Terminal state |
|---|---|---|
| Requirement | Proposed → Active → Resolved → Closed | Closed |
| Bug | Proposed → Active → Resolved → Closed | Closed |
| Task | Proposed → Active → Resolved → Closed | Closed |

> **Note:** Custom process templates may have additional or renamed states. Query live states with:
> ```bash
> az boards work-item type state list --type "User Story"
> ```

---

## Common Field Reference

### System fields (all work item types)

| Display name | Field reference name | CLI argument |
|---|---|---|
| Title | `System.Title` | `--title` |
| State | `System.State` | `--state` |
| Assigned To | `System.AssignedTo` | `--assigned-to` |
| Iteration Path | `System.IterationPath` | `--iteration` |
| Area Path | `System.AreaPath` | `--area` |
| Description | `System.Description` | `--description` |
| Work Item Type | `System.WorkItemType` | `--type` (on create only) |
| Tags | `System.Tags` | `--fields "System.Tags=tag1; tag2"` |
| Created Date | `System.CreatedDate` | read-only |
| Changed Date | `System.ChangedDate` | read-only |
| Created By | `System.CreatedBy` | read-only |
| Team Project | `System.TeamProject` | `--project` |
| ID | `System.Id` | `--id` |
| Parent | `System.Parent` | via `work-item relation add` |

### Microsoft.VSTS fields (common)

| Display name | Field reference name | Notes |
|---|---|---|
| Priority | `Microsoft.VSTS.Common.Priority` | 1–4; 2 is default |
| Story Points / Effort | `Microsoft.VSTS.Scheduling.StoryPoints` | Agile / Scrum |
| Original Estimate | `Microsoft.VSTS.Scheduling.OriginalEstimate` | CMMI / Task |
| Remaining Work | `Microsoft.VSTS.Scheduling.RemainingWork` | Task |
| Completed Work | `Microsoft.VSTS.Scheduling.CompletedWork` | Task |
| Acceptance Criteria | `Microsoft.VSTS.Common.AcceptanceCriteria` | User Story / PBI |
| Repro Steps | `Microsoft.VSTS.TCM.ReproSteps` | Bug |
| Severity | `Microsoft.VSTS.Common.Severity` | Bug |
| Business Value | `Microsoft.VSTS.Common.BusinessValue` | Epic / Feature |
| Risk | `Microsoft.VSTS.Common.Risk` | User Story |

---

## Field Names vs CLI Arguments

Named CLI arguments cover the most common fields. Use `--fields` for everything else:

```bash
# Named argument (preferred when available)
az boards work-item update --id 123 --state "Active"

# --fields for fields without named arguments
az boards work-item update --id 123 \
  --fields "Microsoft.VSTS.Common.Priority=1" \
           "Microsoft.VSTS.Scheduling.StoryPoints=5" \
           "System.Tags=backend; sprint-5"
```

Look up all fields for a work item type:
```bash
az boards work-item type field list --type "User Story" --output table
```
