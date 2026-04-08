---
mode: agent
description: Assist with syncing Power Pages portal content between Dataverse environments. Guides export from source environment and import to target environment using pac CLI. Use when deploying portal changes from DEV to SIT/UAT/PROD.
---

# Portal Sync Assistant

Help sync Power Pages portal content between environments using the Power Platform CLI (`pac`).

## Required Information

Ask the user:

1. **Source environment** — URL of the environment to export from (e.g., `https://dc-grants-dev.crm3.dynamics.com`)
2. **Target environment** — URL of the environment to import into
3. **Portal website ID** (if known) — GUID from Power Pages admin, or leave blank to list available portals
4. **Sync scope** — Full portal or specific changes only?

## Steps

### 1. Authenticate

```powershell
# Authenticate to source environment
pac auth create --url {sourceEnvironmentUrl}
```

### 2. List Available Portals (if website ID unknown)

```powershell
pac pages list
```

Present the list to the user and confirm which portal to sync.

### 3. Export Portal from Source

```powershell
# Export portal to src/powerpages/
pac pages download --path src/powerpages --websiteId {websiteId}
```

Review the exported files:
```powershell
git --no-pager diff --name-only src/powerpages/
```

Summarize the changed portal components for the user:
- Web files (HTML/JS/CSS changes)
- Web templates (Liquid template changes)
- Content snippets
- Table permissions / entity forms / entity lists
- Site settings

### 4. Commit the Export

```powershell
git add src/powerpages/
git commit -m "feat(portal): export portal changes from DEV - {brief description}"
```

### 5. Deploy to Target Environment

```powershell
# Authenticate to target environment
pac auth create --url {targetEnvironmentUrl}

# Upload portal to target
pac pages upload --path src/powerpages --websiteId {websiteId}
```

### 6. Verify

- Open Power Pages management for the target environment
- Clear the portal cache if needed: Power Apps Portal Admin Center > Portal Actions > Restart
- Verify the changes appear correctly in the portal

## Common Issues

| Issue | Resolution |
|---|---|
| Website ID mismatch | Confirm correct website ID for target environment — IDs differ per environment |
| Authentication failure | Run `pac auth list` to confirm active auth profile, then `pac auth select` |
| Content not updating | Clear portal cache via Portal Admin Center > Restart |
| Table permission errors | Verify table permissions are configured correctly on the target environment |
| Missing site settings | Some site settings are environment-specific — verify after import |

## Notes

- Portal website IDs are **environment-specific** — confirm the correct ID for each environment
- Site settings containing environment-specific URLs (e.g., redirect URLs, API endpoints) must be updated manually after sync
- Always test portal functionality after deploying to a new environment
