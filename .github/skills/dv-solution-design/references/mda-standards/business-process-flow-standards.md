# MDA Standards: Business Process Flows (BPF)

## WHY?

Provides a consistent business flow between multiple processes.

## Naming

`{Table} - {Business Process}`

Example: `Loan - Underwriting Approval`

## Multiple BPFs per Table

- Multiple BPFs for one table adds complexity, especially if the BPF is determined by a changeable attribute value
- Use **MNP.Plugins.Base.SetBPFStageActivity** to manage BPF switching programmatically
- Prefer a **single BPF per table** with branching/conditional features where possible

## Integrating BPF with the Source Table

1. Create a **`{Table}.Stage`** option set field on the source table to stay in sync with the BPF active stage
2. Use this field to automate BPF stage transitions from workflows

## BPF Lifecycle Workflows

| Workflow | Purpose |
|---|---|
| `{BPF Table} - Create - MNP` | Validate whether the BPF can be created (e.g. required fields are populated) |
| `{BPF Table} - Update - MNP` | Validate stage entry/exit; keep `{Table}.Stage` in sync; navigate BPF using `SetBPFStageActivity` |
| `{BPF Table} - Delete - MNP` | Validate whether the BPF can be deleted; throw ERROR if not |

## SetBPFStageActivity Plugin

See [MNP.Base.Plugin](../components/mnp-base-plugin.md#set-bpf-activity) for full parameter reference.

Key notes:
- Always check the **Error Message** output -- the plugin does not throw exceptions on failure
- Some stage movements may not be supported due to TraversedPath limitations on conditional stages
