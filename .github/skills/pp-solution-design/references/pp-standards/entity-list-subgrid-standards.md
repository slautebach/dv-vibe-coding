# Entity List and Sub-Grid Standards

Wiki source: `wiki/Welcome/Platform-Delivery-Playbook/Implementation-Standards/Using-PowerPages/Entity-List-and-Sub-Grid-Standards.md`

> **Note:** This standards page is currently a stub in the wiki. Guidance below is synthesized from MNP Power Pages conventions.

## WHY?
Entity Lists display multiple records in a grid on a portal page, allowing users to browse, filter, and navigate to individual records. Sub-Grids appear within Basic Forms to show related records.

## Naming Convention

`{Solution} - {Table} - {Purpose}`

**Examples:**
- `QUARTS - Application - My Applications` — shows all applications for the current portal user
- `QUARTS - Registration - Active Registrations`

## Entity List Design Guidance

- **Filter to current user**: Always filter to `contact.contactid = {{ user.id }}` for authenticated portals to prevent users from seeing other users' records
- **Views**: Base Entity Lists on a dedicated Dataverse view — create portal-specific views to control visible columns
- **Actions**: Configure Create, View, Edit, Delete actions per business requirements
  - Use **Filter Criteria** on actions to conditionally show/hide based on record status
- **Search**: Enable search bar for lists where users need to find specific records

## Sub-Grid Design Guidance (inside Basic Forms)

- Use **the same View** for both **View Details** and **Edit** to enable default link opening in Edit Form
- Use **Filter Criteria** to show/hide View and Edit actions based on record attributes
- **NOTE:** Filter Criteria for **Create** and **Associate/Disassociate** do **NOT** work
- For JS customizations that interact with the subgrid, apply them **after the subgrid has loaded**

## Table Permissions Requirement
Entity Lists and Sub-Grids require **Table Permissions** to be configured for the portal web role. Without table permissions, the list will be empty.

See [Table Permissions Standards](table-permissions-standards.md).

## Related
- [Table Permissions Standards](table-permissions-standards.md)
- [Basic Form Standards](basic-form-standards.md)
