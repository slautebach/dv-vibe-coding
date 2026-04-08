# MDA Standards: Views

## WHY?

- Provides consistent views into the table tailored to the user's perspective/role
- Separates technical views (portal) from user-facing views

## Views to Create

- Create an **All {Table}** view for full transparency
- Ensure **All, Active, Inactive** views have similar column layouts
- Use **XrmToolBox - View Layout Replicator** to sync column layouts across views

## View Naming Conventions

| Context | Pattern | Example |
|---|---|---|
| MDA views | User-resonating business name | "Active Applications" |
| Portal views | `Portal - {Description}` | "Portal - Registration" |
| Portal French | `Portal - {Description} - FR` | "Portal - Registration - FR" |
| Subgrid views | `Subgrid - {Target Table}` | "Subgrid - Claims" |

- **Do NOT include Portal or Subgrid views in the MDA**

## Column Layout

- Suggest always including **Modified On** as the last column
- Subgrid views: remove redundant columns (e.g. the parent table name column)

## Description

Provide a concise description of the view's purpose -- used to generate data model metadata documentation.
