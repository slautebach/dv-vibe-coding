---
mode: agent
description: Generate release notes for a Dataverse solution version. Summarizes solution component changes and links to Azure DevOps work items included in the release. Run before tagging a release or deploying to UAT/PROD.
---

# Solution Release Notes Generator

Generate professional release notes for a solution deployment.

## Required Information

Ask the user for the following before proceeding:

1. **Solution name and version** — e.g., "GrantsManagement v2.3.0"
2. **Target environment and deployment date** — e.g., "UAT deployment, 2025-03-15"
3. **Previous version** (for comparison) — e.g., "v2.2.1"
4. **Work items included** — Ask the user to provide work item IDs, or use the `ado-backlog` skill to query completed items in the current sprint/iteration

## Steps

1. **Gather git diff** — Run: `git --no-pager diff {previous-tag}..HEAD --name-only -- src/solutions/`
   Summarize the changed solution components by category (entities, forms, flows, plugins, security roles, etc.)

2. **Query work items** — Use the `ado-backlog` skill to get details for each provided work item ID:
   - Title, type (User Story / Bug / Task), state, assigned to

3. **Generate release notes** using this format:

```markdown
# Release Notes — {SolutionName} v{Version}

**Deployment Date**: {Date}
**Target Environment**: {Environment}
**Previous Version**: v{PreviousVersion}

---

## Summary

{2-3 sentence high-level summary of what this release delivers}

---

## New Features

{List user stories / features delivered. For each:}
- **{Work Item Title}** (#{WorkItemId}) — {brief description of what the user can now do}

## Bug Fixes

{List bugs resolved:}
- **{Bug Title}** (#{WorkItemId}) — {brief description of what was fixed}

## Technical Changes

{Summarize solution component changes by category:}

### Entities / Tables
- {entity changes}

### Forms & Views
- {form/view changes}

### Cloud Flows
- {flow changes}

### Plugins
- {plugin changes}

### Security Roles
- {security role changes}

### Other
- {other changes}

---

## Deployment Notes

{Any special instructions for this deployment:}
- Connection references to update
- Workflows to activate
- Data migrations required
- Known issues or limitations

---

## Rollback Plan

If issues arise, roll back by deploying v{PreviousVersion} from the `Package` artifact of the previous successful build.
```

4. **Review with the user** — Present the draft and ask if anything needs to be added, changed, or removed.

5. **Save the output** — Save to `docs/generated/release-notes-v{Version}-{Date}.md` for review before publishing to the wiki.
