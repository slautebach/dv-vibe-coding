---
name: pp-solution-design
description: Surface and apply MNP solution design patterns and implementation standards for Power Pages (portal) development — including portal submission flows, authentication strategies, analytics, web templates, invitation redemption, Ontario Design System integration, malware protection, and all Power Pages configuration standards (forms, pages, web templates, table permissions, site settings). Use when asked "what pattern should I use for a portal...", "how should I design a portal...", "what are the Power Pages standards for...", "portal form submission", "portal authentication", or "portal web template". Cross-references dv-solution-design for Dataverse concerns.
---

# Power Pages Solution Design

This skill surfaces MNP's Power Pages patterns and implementation standards. Reference files do the heavy lifting — load only the files relevant to the query.

> For Dataverse/CRM concerns (plugins, workflows, table design, etc.), use the **dv-solution-design** skill.

## Domains and Reference Files

### Patterns (`references/patterns/`) — load when asked about architecture, approach, or "how should I…"

| Query topic | File |
|---|---|
| Portal form submission flows (anonymous, authenticated, multi-step) | `references/patterns/portal-submission.md` |
| Authentication, identity providers, Public Secure, Entra ID | `references/patterns/portal-authentication.md` |
| Google Analytics, session timeout, tracking code | `references/patterns/portal-analytics.md` |
| Web templates, Liquid, page layouts, template inheritance | `references/patterns/portal-web-template.md` |
| Invitation redemption, reference-number challenge pattern | `references/patterns/redeem-invitation.md` |
| Migrating from standard to Enhanced Data Model | `references/patterns/enhanced-data-model-migration.md` |
| Ontario Design System (ODS), ontario-Header/Footer, ODS CSS | `references/patterns/ontario-ods.md` |
| Malware scanning for file uploads | `references/patterns/malware-protection.md` |
| Payment processing, CCPay (Ontario), Moneris | `references/patterns/payment-transaction-portal.md` |

### Components (`references/components/`) — load when asked about a specific library or component

| Query topic | File |
|---|---|
| `mnp_common.js` portal helper library (Web API, form helpers, masks, validators, timeouts) | `references/components/mnp-common-js-portal.md` |

### PP Standards (`references/pp-standards/`) — load when asked about naming conventions, configuration standards, or "what are the standards for…"

| Query topic | File |
|---|---|
| Web site, language, URL structure | `references/pp-standards/web-site-standards.md` |
| Web page, partial URL, JS/CSS placement | `references/pp-standards/web-page-standards.md` |
| Web template naming, inheritance, security, FetchXML | `references/pp-standards/web-template-standards.md` |
| Basic forms: naming, CRM form, query strings, metadata | `references/pp-standards/basic-form-standards.md` |
| Advanced forms (multi-step): naming, steps, metadata | `references/pp-standards/advanced-form-standards.md` |
| Entity lists and subgrids | `references/pp-standards/entity-list-subgrid-standards.md` |
| Table permissions: scope, relationships, web roles | `references/pp-standards/table-permissions-standards.md` |
| Web files: folder structure, ODS assets | `references/pp-standards/web-file-standards.md` |
| Site settings: Google Analytics, Azure Storage, Auth settings | `references/pp-standards/site-setting-standards.md` |
| Content snippets: naming, Timeout/TrackingCode/Head snippets | `references/pp-standards/content-snippet-standards.md` |

## Progressive Disclosure

- **Pattern query** (e.g., "how do I implement portal auth") → load the matching `references/patterns/` file
- **Standards query** (e.g., "what are the naming standards for basic forms") → load the matching `references/pp-standards/` file
- **Component query** (e.g., "what functions does mnp_common.js have") → load `references/components/mnp-common-js-portal.md`
- **Cross-cutting query** (e.g., "design an application submission portal") → load the submission pattern + relevant standards files

## Example Prompts

- "What pattern should I use for a citizen-facing application submission form in Power Pages?"
- "How do I implement portal authentication for a program with internal and external user types?"
- "Set up malware scanning for file uploads on a portal form"
- "How do I integrate the Ontario Design System into our Power Pages site?"
- "What are the table permission standards for a portal that reads Case records?"
- "What naming convention should I use for a basic form that creates an Application record?"
- "How does invitation redemption work for pre-created cases?"
- "What site settings do I need for Google Analytics and session timeout?"
