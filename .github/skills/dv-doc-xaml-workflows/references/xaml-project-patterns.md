# XAML Workflow Project Patterns

This is a **project-specific supplement** to the authoritative XAML parsing reference.

**Primary reference (load first):**
`.github/skills/dataverse-solution-parser/references/workflow-schema.md`

This document adds MNP Income Assistance project-specific patterns that extend the base reference: custom plugin names, DisplayName conventions, entity display name mappings, and option set values observed in this codebase.

---

## Entity Display Name Mappings

The `.data.xml` `PrimaryEntity` uses logical names. Common ones in this project:

| Logical Name | Display Name | Notes |
|---|---|---|
| `incident` | Case | Main program case record |
| `invoice` | Invoice | Payment invoice |
| `mnp_application` | Application | Client application |
| `mnp_benefitassessment` | Benefit Assessment | Calculated benefit amounts |
| `mnp_asset` | Asset | Client asset record |
| `mnp_invoiceproductrevision` | Invoice Product Revision | |
| `mnp_saidmonthlycalculation` | SAID Monthly Calculation | |
| `mnp_overpaymentcredits` | Overpayment Credits | |
| `contact` | Contact | Client/individual |
| `account` | Account | Organization/provider |
| `task` | Task | Activity task |
| `email` | Email | Email activity |
| `mnp_letter` | Letter | Generated letter |
| `mnp_portalfile` | Portal File | Portal client file |
| `mnp_portalinvitation` | Portal Invitation | |

---

## MNP Custom Plugin Activities

When you see an `AssemblyQualifiedName` that starts with `MNP.` or contains `Mnp`, it is a custom plugin activity. Common ones:

| Class Name Pattern | Purpose |
|---|---|
| `MNP.CRM.Plugins.*CloseCaseActivity` | Executes program-specific case closure logic |
| `MNP.CRM.Plugins.*CreateApplicationActivity` | Creates application records for a program |
| `MNP.CRM.Plugins.*CaseProcessFlow` | Drives case process flow transitions |
| `MNP.CRM.Plugins.*IndividualizedPlan` | Creates individualized plan records |
| `ConvertCrmXrmTypes` | Internal type conversion utility (boilerplate) |

When documenting a custom activity step, use the class name (minus namespace) as the step label in diagrams and descriptions. If the `DisplayName` is generic (e.g., `CustomActivityStep8`), derive the name from the `AssemblyQualifiedName` class name.

---

## DisplayName Conventions in This Project

Steps in this project follow these naming patterns — use them to infer intent:

| DisplayName Pattern | Meaning |
|---|---|
| `ConditionStep1: <description>` | The description after the colon is the actual condition logic |
| `ConditionStep1` (no description) | No inline description; infer from `GetEntityProperty` attributes |
| `CustomActivityStep<N>` | Custom plugin call; check `AssemblyQualifiedName` for class name |
| `StopWorkflowStep<N>` | Terminates the workflow (check `Status` arg: Succeeded vs Failed) |
| `ConvertCrmXrmTypes` | Boilerplate type conversion — skip in documentation |

---

## Program Prefixes

Workflow filenames and display names follow these program prefixes:

| Prefix | Program |
|---|---|
| `SIS-` | Saskatchewan Income Support |
| `SEI-` | Saskatchewan Employment Incentive |
| `PCHB` | Private Care Home Benefit |
| `Multi-App-` | Applies across multiple programs |
| `ITS-` | Invoice/payment processing |
| `OnDemand-` | Manually triggered utility workflows |
| `DataMigration-` | Data migration/cleanup (may be deprecated) |
| `Deprecated-` | No longer active — document but flag as deprecated |

---

## Common Option Set Values

Frequently referenced option set codes in workflow conditions:

### Case Status Reason (`incident.statuscode`)
| Value | Meaning |
|---|---|
| `120310001` | Pending Closure |
| `120310002` | Active |
| `120310005` | Closed |

### Invoice Status (`invoice.statuscode`)
| Value | Meaning |
|---|---|
| `100003` | Cancelled |
| `100004` | Void |
| `100001` | Active |
| `100005` | Paid / Complete |

### Program Type (`incident.mnp_programtype` / `mnp_application.mnp_programtype`)
| Value | Meaning |
|---|---|
| `120310001` | SIS |
| `120310002` | SEI |
| `120310003` | PCHB |

---

## .data.xml Trigger Combinations — Common in This Project

| Pattern | What it means |
|---|---|
| `OnDemand=1`, no update/create/delete triggers | Manual-only; called from ribbon or another workflow |
| `TriggerOnUpdateAttributeList=statuscode,statecode` | Fires on any status change |
| `TriggerOnCreate=1` + condition step immediately | Creates on all records but gates early via condition |
| `Subprocess=1` | Called by a parent workflow — document who calls it |

---

## Notes on XAML in This Codebase

- **`x:Class` GUID format**: The root `Activity` class name encodes the workflow GUID (e.g., `XrmWorkflowe9581e0b...`). Use the `.data.xml` `WorkflowId` attribute instead for the canonical ID.
- **Variable naming**: Local variables follow `ConditionBranchStep<N>_<index>` — these are boilerplate evaluation variables and do not need to appear in documentation.
- **`EvaluateExpression` / `EvaluateCondition`**: These are low-level boilerplate for comparing values. Skip them in documentation; the surrounding `ConditionSequence` DisplayName conveys the intent.
- **`mva:VisualBasic.Settings`**: Always present; always skip.
