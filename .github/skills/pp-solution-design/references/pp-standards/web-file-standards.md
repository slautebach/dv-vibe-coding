# Web File Standards

Wiki source: `wiki/Welcome/Platform-Delivery-Playbook/Implementation-Standards/Using-PowerPages/Web-File-Standards.md`

## WHY?
To be consistent with Power Pages web file implementation and to standardize folder structure and file organization.

## Design Guidance

### System Configuration
- Adjust the **maximum file size** in CRM > Advanced Settings > System Settings > Email (controls attachment size limits)
- Use **XrmToolbox** plugins to manage Web Files (bulk upload/manage)

### ODS Accelerator Web Files
Load the ODS Portal files from the Git repo or via the [ODS Portal Pipeline](https://dev.azure.com/MNPDigital/DC-Delivery/_build?definitionId=187):
- Source: [Ontario Design System Complete Package](https://www.npmjs.com/package/@ontario-digital-service/ontario-design-system-complete-styles)
- Only a subset of ODS files are uploaded — refresh when the ODS theme version is updated

### Solution-Specific Folder Structure

Use a clear, consistent directory structure for solution-specific web files:

```
/                       (root — favicon.ico)
/style/                 CSS files (solution-specific overrides)
/scripts/               JavaScript files (solution-specific + jQuery plugins)
/images/                Images and digital assets
```

**Always update `favicon.ico`** for the solution.

### Naming
- Files should use descriptive, lowercase-hyphenated names
- Version numbers can be included for external libraries (e.g., `jquery-3.6.0.min.js`)

## Related
- [Web Site Standards](web-site-standards.md)
- [Pattern - Ontario ODS](../patterns/ontario-ods.md)
- [Content Snippet Standards](content-snippet-standards.md) — `Head/Bottom` snippet loads web files
