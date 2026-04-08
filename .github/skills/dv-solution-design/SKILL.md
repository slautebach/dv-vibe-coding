---
name: dv-solution-design
description: Surface and apply MNP solution design patterns and Model-Driven App implementation standards for Dynamics 365 / Dataverse development -- including plugin patterns, rollup strategies, email notifications, checklists, reference tables, external integrations, URS, and MDA standards (forms, views, actions, BPFs, web resources). Use when asked "what pattern should I use for...", "how should I design...", "what is the MNP approach for...", "design a solution for...", or "what MDA standards apply to...". Cross-references pp-solution-design for portal concerns.
---

# MNP Solution Design

## Domain Map

Load the relevant reference file(s) based on the query type:

### Patterns (`references/patterns/`)
Load when the query is about solving a recurring design problem:

| File | Load when asked about... |
|---|---|
| `reference-tables.md` | lookup tables, global option sets with extra metadata, bilingual portal lists, code fields |
| `solution-plugin.md` | writing plugins, early bound classes, solution-specific plugin structure |
| `email-notification.md` | sending emails, email templates, notification framework, triggered alerts |
| `checklists.md` | checklist features, multi-step validation, checklist items, completion tracking |
| `realtime-rollup.md` | rollup calculations, real-time sync, syncPush, parent-child aggregation |
| `external-integration.md` | calling Azure Functions, Logic Apps, REST APIs, external services, spinner/polling pattern |
| `payment-transaction.md` | payment processing, CCPay (Ontario Government), Moneris integration |
| `urs.md` | Universal Resource Scheduling, booking timeslots, bookable resources, resource requirements |

### Components (`references/components/`)
Load when the query involves a specific reusable library or component:

| File | Load when asked about... |
|---|---|
| `mnp-base-plugin.md` | MNP.Base.Plugin, syncPush, syncPull, SetEntityName, workflow activities, validation plugin |
| `north52.md` | North52 formulas, N52, BPA, decision tables, SmartFlow, xCache |
| `liquid-rules-engine.md` | Liquid templates, LiquidRuleEngine, rule-driven field updates |
| `client-api-crm.md` | JavaScript form helpers, mnp_Common.js, CRM client API, form scripting |

### MDA Standards (`references/mda-standards/`)
Load when the query is about how to implement or name a specific MDA component:

| File | Load when asked about... |
|---|---|
| `mda-standards.md` | MDA structure, app areas, naming the app, Primary/Admin areas |
| `form-standards.md` | form layout, tabs, sections, fields, subgrids, Quick View naming |
| `view-standards.md` | views, view naming, Subgrid/Portal views, column layout |
| `action-standards.md` | Actions, global actions, polymorphism, EntityReference parameters |
| `business-rule-standards.md` | business rules, Lock Fields, Show/Hide, scope |
| `business-process-flow-standards.md` | BPF, stage sync, BPF validation workflows |
| `workflow-standards.md` | workflow naming, Create/Update/Delete patterns, GetAttributesChanged |
| `web-resources-standards.md` | web resources, JS naming, mnp_common.library.js |
| `dashboard-standards.md` | dashboards, role-based vs purpose-based, KPI charts |
| `message-standards.md` | error messages, ERROR: prefix, tracing in messages |
| `reports-standards.md` | reports, report naming, layout, header/footer standards |
| `canvas-dialogs.md` | Canvas dialogs in MDA, canvas page as dialog, command button |

## Progressive Disclosure

1. Read the domain map above to identify which file(s) apply.
2. Load only the matching reference file(s) -- avoid loading entire folders unless the query spans multiple domains.
3. Multiple files may apply (e.g., designing an email notification Action requires both `email-notification.md` and `action-standards.md`).

## Example Prompts

- "What pattern should I use for sending emails when a case status changes?"
  - Load: `patterns/email-notification.md` + `mda-standards/action-standards.md`
- "Design a checklist implementation for multi-step application review"
  - Load: `patterns/checklists.md`
- "How should I call an Azure Function from a model-driven app button?"
  - Load: `patterns/external-integration.md`
- "What is the MNP pattern for rollup calculations that need to be real-time?"
  - Load: `patterns/realtime-rollup.md` + `components/mnp-base-plugin.md`
- "What form standards should I follow for the Application entity?"
  - Load: `mda-standards/form-standards.md` + `mda-standards/mda-standards.md`
