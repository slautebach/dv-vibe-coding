# MDA Standards: Forms

## WHY?

- Provides an engaging layout to surface the right information at the right time
- Ensures consistent layout across all tables and apps

## Minimum Forms to Create

- **Main** form
- **Quick View** form
- **Card** form

## Naming

| Form | Prefix/Convention |
|---|---|
| Portal-only form | `Portal -` prefix (e.g. `Portal - Create`) |
| Quick View | `qv_{QuickViewName}` |

## Description

Provide a concise description of the form's purpose -- used to generate data model metadata documentation.

## Main Form

- **Header:** Add Status Reason, Owner

## Tab Standards

| Rule | Detail |
|---|---|
| Name | `tab_{TabArea}` (e.g. `tab_general`) |
| Label | Mixed Case |
| Duplicate related record tabs | Rename for clarity (e.g. "Payment Contact", "Service Contact" instead of "Contact, Contact") |
| Record Details tab | Always include -- contains admin/audit fields (Created By, Created On, Modified By, Modified On, legacy IDs, name) |
| Minimum columns | Always use at least 2 columns for a better experience |

### 3-Column Tab Layout

| Column | Width | Purpose |
|---|---|---|
| Left | 50% | Primary -- most important information |
| Center | 30% | Timeline |
| Right | 20% | Supporting related information |

### Record Details Tab

- Section name: `section_recorddetails`
- 4-column section
- Include: Created By, Created On, Modified By, Modified On
- Add hidden supporting attributes (legacy IDs, name fields, rollup tracers)

## Section Standards

| Rule | Detail |
|---|---|
| Name | `section_{SectionArea}` |
| Label | ALLCAPS |
| Component label position | **Top** (label appears above the control) |
| Grouping | Group like attributes together (e.g. PAYMENTS, DATES) |
| Responsive wrapping | Order sections so wrapping still produces a logical layout |

## Field Standards

- **DO NOT** make fields read-only on the form -- use Business Rules instead
  - Keeps fields accessible to Workflows/Actions
  - Allows admins to temporarily unlock by deactivating the Business Rule
- Add a **Quick View** directly below lookup fields to surface related record details
- Remove redundant text from labels within grouped sections (e.g. inside LOAN section, use "Interest Rate" not "Loan Interest Rate")

## Subgrid Standards

| Rule | Detail |
|---|---|
| Name | `subgrid_{SubgridViewName}` |
| Label | ALLCAPS |

## Timeline

- Remove activity types not relevant to the table

## JavaScript on Forms

- Use `mnp_common.library.js` for common functions
- Create table-specific web resources: `mnp_{table}.library.js`
- See [Web Resources Standards](web-resources-standards.md)

## Toolbar

- Remove **Deactivate** and **Activate** if not applicable
- Add custom buttons to execute Flows/Actions (avoid requiring users to navigate to the Flow menu)
