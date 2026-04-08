# MDA Standards: Web Resources

## WHY?

- Optimized deployment of client-side code
- Consistent usage and discoverability

## Design Guidance

- Use **`mnp_common.library.js`** to access common helper classes (see [Client API CRM](../components/client-api-crm.md))
- Always require passing `FormContext` as the first parameter to functions
- Always use file extensions on web resource names
- Use folder structure to organize related resources
- **Prioritize Canvas Apps over Web Resource HTML** for UI components

## Naming Convention

`mnp_{Table}.Library.js`

Examples:
- `mnp_contact.library.js` -- JS functions for the Contact table
- `mnp_claim.library.js` -- JS functions for the Claim table
- `mnp_common.library.js` -- shared common functions (do not modify directly)
