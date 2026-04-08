# Wiki Submodule Setup

## Overview

The `wiki/` folder is an Azure DevOps Wiki git submodule. This allows wiki pages to be authored directly in VS Code alongside source code with full GitHub Copilot support, while remaining published to Azure DevOps as the official project documentation.

## Azure DevOps Wiki URL Pattern

```
https://<org>@dev.azure.com/<org>/<project>/_git/<project>.wiki
```

- `<org>` = Azure DevOps organization name (e.g., `MNPDigital`)
- `<project>` = Azure DevOps project name (e.g., `DC-Delivery`)
- The wiki repo name is always `<project>.wiki`

**Example:**
```
https://MNPDigital@dev.azure.com/MNPDigital/DC-GrantsManagement/_git/DC-GrantsManagement.wiki
```

## Adding the Wiki Submodule (New Projects)

```powershell
# 1. Add the wiki repo as a submodule
git submodule add https://<org>@dev.azure.com/<org>/<project>/_git/<project>.wiki wiki

# 2. Pin to the wikiMaster branch (Azure DevOps default wiki branch)
cd wiki
git checkout wikiMaster
cd ..
git submodule set-branch --branch wikiMaster wiki

# 3. Commit the submodule registration
git add .gitmodules wiki
git commit -m "chore: add wiki as git submodule"
git push
```

## Initializing After Cloning

```powershell
git submodule update --init --recursive
```

## Updating the Wiki

Always commit and push wiki changes from **within the `wiki/` submodule folder**, not from the main repo root:

```powershell
cd wiki
git add .
git commit -m "docs: update architecture overview"
git push
cd ..
```

Then update the main repo's submodule pointer:

```powershell
git add wiki
git commit -m "chore: update wiki submodule pointer"
git push
```

## ADO Wiki Format Rules

- **Root page**: `wiki/Home.md`
- **Sub-pages**: placed in a folder matching the parent page name (e.g., `wiki/Architecture/Solution-Overview.md`)
- **File names**: PascalCase or Hyphenated-Names (e.g., `Solution-Overview.md`)
- **NEVER use `README.md`** — not supported by ADO wiki
- **Page ordering**: Every folder must have a `.order` file listing page names without `.md` extension
- **Mermaid diagrams**: Use `::: mermaid` / `:::` delimiters (not backtick fences)
- **Line breaks in diagrams**: Use `<br/>` not `\n`

## .gitmodules Reference

After setup, `.gitmodules` will contain:

```ini
[submodule "wiki"]
    path = wiki
    url = https://<org>@dev.azure.com/<org>/<project>/_git/<project>.wiki
    branch = wikiMaster
```
