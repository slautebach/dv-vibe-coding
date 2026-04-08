# Pattern: Checklists

## WHY?

Provides a flexible checklist feature where:
- Checklist items can be tailored to varying business needs
- Completion can be validated before advancing to the next stage

## Tables

### Checklist Template
| Field | Notes |
|---|---|
| Name | Template name |
| Description | Purpose of the checklist |

### Checklist Item Template
| Field | Notes |
|---|---|
| Code | Unique code for the item |
| Name | Display name |
| Description | What needs to be verified |
| Checklist Template | Lookup to Checklist Template |

### Checklist Item
| Field | Notes |
|---|---|
| Reference | Lookup to the business table (e.g. Case, Application) -- ideal would be a Regarding lookup but not always possible |
| Checklist Template Item | Lookup to Checklist Item Template |
| Comments | Free-text notes |
| Verified | Choice: Yes / No / N/A |

## Design Guidance

- Create Checklist Items when needed (e.g. after initial intake, before assessment, before closure)
- Validate completion using a calculated field and automation
- Provide an **editable subgrid** as the user experience for checklist items

## Automation

### Checklist - Create - Action
- Use Power Automate or a Workflow
- Bulk-create Checklist Item records based on the Checklist Template selected (or defined by a Service Configuration table: Service Delivery Lifecycle, Category, Program, etc.)
- Assign the **Reference** lookup so each item is linked to the target table

### Checklist Validation (syncPush plugin)
Configure a `syncPushEntity` plugin to roll up:
- **(A)** Total number of checklist items
- **(B)** Total number where Verified = Yes or N/A

See [MNP.Base.Plugin - Sync Push](../components/mnp-base-plugin.md) for configuration details.

### Calculated Field on Reference Table
- **Checklist Completed (Boolean):** `(A) == (B)`
- Use this field to gate stage transitions or block functions until the checklist is complete
