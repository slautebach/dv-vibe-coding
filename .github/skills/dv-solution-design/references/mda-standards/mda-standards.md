# MDA Standards: Model-Driven App Structure

## WHY?

- Provides a targeted app for a user community
- Ensures consistency across different apps

## App Structure Guidance

- Consider **multiple MDAs** for different business process roles (e.g. Finance Operations Hub, Grants Operations Hub)
  - Balance maintenance effort against the benefit of separate apps
- For Customer Service/Case Management solutions, consider renaming the OOTB **Customer Service Hub** to `{SolutionName} Customer Service Hub` to retain Microsoft customizations
- Suggested app naming: `{SolutionName} Operations Hub`

## Minimum Two App Areas

### Primary Area (e.g. "Service")
- Contains operational tables and dashboards grouped in sections
- First section must be **My Workspace** (includes Activities, Dashboards, Knowledge Search, etc.)

### Administration Area (e.g. "Admin")
- Contains supporting configuration tables for administrators
- Sections to include:
  - **Reference** -- reference/lookup tables
  - **Supporting** -- internal tables such as intersect or portal tables
- Group pages into sections with most-used items at the top

## Include Only Relevant Forms and Views

- Turn **OFF** "Include all forms in the app" and "Use all views"
- Be explicit about which forms and views are included
- **Recommended: only one form per entity per MDA**
  - Multiple forms may indicate a second MDA is warranted
