# Pattern - Migrating to Power Pages Enhanced Data Model

Wiki source: `wiki/Welcome/Platform-Delivery-Playbook/Solution-Design/Pattern-%2D-Migrating-to-PowerPages-Enhanced-Data-Model.md`

> **Note:** This document is a high-level guide. Update/correct steps for the next person as you encounter issues.

## WHY?

- The Enhanced Data Model (EDM) is now out of preview and is the new standard for Power Pages portals
- EDM provides improved performance, modern data model, and new Power Pages Studio features
- This is the most straightforward method to migrate from the standard data model

## Pre-Requisites

1. [PAC CLI (Power Platform Command Line utility)](https://learn.microsoft.com/en-us/power-platform/developer/cli/introduction) installed
2. A local folder containing your existing portal source (or a new folder to download to)
3. Your **Web Site record GUID** — log into Portal Management App > Web Sites > get the record GUID
4. Enhanced Data Model turned on in your Dataverse environment

## Migration Steps

```powershell
# 1. Navigate to your power pages directory
cd <power pages download folder path>

# 2. Authenticate with Dataverse
pac auth create --name <connection name> --url <*.crm3.dynamics.com url>

# 3. Download the portal in standard model format (version 1)
pac powerpages download --path .\ --overwrite --websiteId <website guid> --modelVersion 1

# 4. Upload as Enhanced Data Model (version 2)
pac powerpages upload --path .\<site folder name> --modelVersion 2 -f
```

## Verification Steps

1. Navigate into Dataverse and verify the Enhanced Data Model virtual entity records are populated
2. Open the Enhanced Data Model Power Pages Management app and review records
3. Create a new Power Pages Site and link it to the new EDM website record
4. Log into the new portal site, test all pages, find and fix issues

## Notes

- `-f` flag in the upload command forces the upload
- Some configuration may need manual adjustments after migration
- Test thoroughly in DEV before migrating higher environments

## References
- [Power Pages Enhanced Data Model overview](https://learn.microsoft.com/en-us/power-pages/admin/enhanced-data-model)
- [pac powerpages CLI reference](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/powerpages)
