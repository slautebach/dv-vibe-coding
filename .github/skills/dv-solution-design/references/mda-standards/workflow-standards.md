# MDA Standards: Workflows

## WHY?

- Optimizes workflow execution performance
- Provides consistency and reduces time to trace how data is updated

## General Rules

- Workflows that should remain deactivated: prefix with **DNU-** (Do Not Use)
- Test/POC workflows: prefix with your initials (e.g. **EC-**)
- All workflows must be owned by a **Service Principal/Account**
- **Real-Time workflows are preferred** over background workflows
- **Preference for Workflows over Power Automate Flows**
  - Power Automate throttling is not transparent
  - Simple action steps are easier to implement in Classic Workflows

## Centralized Workflow Model

One workflow per trigger type per table:
- ONE Create workflow per table
- ONE Update workflow per table (handles ALL update scenarios)
- ONE Delete workflow per table

## Create Workflow

**Name:** `{Table} - Create - MNP`

**Step order:**
1. Validation steps
2. Default record steps (e.g. default primary name)
3. Solution-specific steps

**Validation:** Use `Stop Workflow - Cancelled` to throw errors
- Message format: `ERROR: {Message} - {Workflow Name}`

## Update Workflow

**Name:** `{Table} - Update - MNP` (post-update)
**Name:** `{Table} - Update - Pre - MNP` (pre-update, rare)

**Key technique:** Use `MNP.Plugins.Base.GetAttributesChangedActivity` to get the list of changed attributes, then branch conditionally.

Example:
- If `GetAttributesChangedList contains [mnp_loan_interestrate]` then call recalculate action

**Filter optimization:** Under "Record fields change", only select attributes that should activate the workflow.

**Step order:**
1. Validation steps
2. Solution-specific steps based on business process

## Delete Workflow

**Name:** `{Table} - Delete - MNP` (post-delete)
**Name:** `{Table} - Delete - Pre - MNP` (pre-delete, rare)

**Step order:**
1. Validation steps
2. Solution/cleanup steps

## On Demand Workflow

**Name:** `{Table} - {Action} - On Demand - MNP`

Added to the Form Toolbar for user-initiated actions.

## Child Workflow

**Name:** `{Table} - {Action} - Child - MNP`

Called from parent workflows. Always include the workflow name in ERROR messages for traceability.

## Background Workflow

**Name:** `{Table} - {Action} - Background - MNP`

Used for low-priority async processes (e.g. email notifications). Real-Time workflows are preferred where possible.
