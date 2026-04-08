---
name: mnp-dv-initialize
description: Initialize a new MNP Digital Dynamics 365 / Power Platform project repository with the standard folder structure, .github Copilot configuration, wiki git submodule, Azure DevOps YAML pipeline stubs, and prompt files. Use when asked to "initialize a project", "set up a new engagement repo", "scaffold a project structure", "create the repo structure", or "set up the wiki submodule". Prompts for solution name, publisher prefix, ADO org URL, and DevOps project, then creates all required files and folders.
---

# MNP DV Initialize

Scaffold a new MNP Digital Dynamics 365 engagement repository. Automates what every project lead does manually at engagement start.

## Step 1: Gather Required Information

Ask the user for these values before doing anything:

| Input | Example | Variable |
|---|---|---|
| Project / engagement name | `Grants Management` | `{ProjectName}` |
| Solution unique name | `GrantsManagement` | `{SolutionName}` |
| Publisher prefix | `mnpgm` | `{Prefix}` |
| ADO organization URL | `https://dev.azure.com/MNPDigital` | `{AdoOrgUrl}` |
| ADO project name | `DC-GrantsManagement` | `{AdoProject}` |
| Client name | `Government of Ontario` | `{ClientName}` |

> If any value is unclear, make a reasonable inference and confirm with the user before proceeding.

## Step 2: Create Folder Structure

Create all directories and placeholder files. Use PowerShell:

```powershell
# Run from the repo root
$dirs = @(
  ".github/prompts",
  ".github/skills",
  "docs/meeting-transcripts",
  "docs/requirements",
  "docs/client-docs",
  "docs/external-docs",
  "docs/decisions",
  "docs/generated",
  "src/solutions",
  "src/plugins",
  "src/webresources",
  "src/powerpages",
  "wiki",
  "pipelines/build",
  "pipelines/export",
  "pipelines/deploy",
  "pipelines/templates",
  "pipelines/scripts"
)
foreach ($d in $dirs) {
  New-Item -ItemType Directory -Force -Path $d | Out-Null
  Write-Host "Created: $d"
}
```

Create `.gitkeep` files in empty leaf folders so git tracks them:

```powershell
$leafDirs = @(
  "docs/meeting-transcripts", "docs/requirements", "docs/client-docs",
  "docs/external-docs", "docs/decisions", "src/solutions", "src/plugins",
  "src/webresources", "src/powerpages", "pipelines/scripts"
)
foreach ($d in $leafDirs) {
  New-Item -Force -Path "$d/.gitkeep" -ItemType File | Out-Null
}
```

## Step 3: Create `.github/` Configuration Files

### `copilot-instructions.md`

Copy `assets/copilot-instructions-template.md` to `.github/copilot-instructions.md`.

Replace all placeholders:
- `{ProjectName}` -> user-provided project name
- `{SolutionUniqueName}` -> solution unique name
- `{PublisherPrefix}` -> publisher prefix
- `{ClientName}` -> client name
- `{AdoOrgUrl}` -> ADO org URL
- `{AdoProject}` -> ADO project name
- `{prefix}` -> publisher prefix (lowercase)
- `{solution}` -> solution name (lowercase)
- `{EngagementLead}`, `{TechLead}`, etc. -> ask user or leave as TODO

### Prompt Files

Copy from `assets/prompts/` to `.github/prompts/`:
- `document-gathering.prompt.md`
- `solution-release-notes.prompt.md`
- `portal-sync.prompt.md`

### Skills

Copy all skills from the StarterKit `.github/skills/` folder to the new repo's `.github/skills/`. The StarterKit lives at `C:\dev\StarterKit\DC-StarterKits_Solution` by default — confirm the source and target repo paths with the user.

## Step 4: Create `docs/generated/README.md`

Create `docs/generated/README.md`:

```markdown
# Generated Documentation

AI-generated documentation staged for human review.

Content here is produced by GitHub Copilot skills (entity docs, flow docs, plugin summaries, wiki drafts) and awaits review before being published to the wiki.

**Nothing in this folder is authoritative or visible to stakeholders until promoted to `wiki/`.**
```

## Step 5: Create Pipeline Files

Copy pipeline stubs from `assets/pipelines/` to the target repo, renaming as shown:

| Source (assets/pipelines/) | Destination (pipelines/) |
|---|---|
| `build-solution.yml` | `pipelines/build/solution.yml` |
| `export-solution.yml` | `pipelines/export/solution.yml` |
| `deploy-solution.yml` | `pipelines/deploy/solution.yml` |
| `steps-build.yml` | `pipelines/templates/steps-build.yml` |
| `steps-export.yml` | `pipelines/templates/steps-export.yml` |
| `steps-deploy.yml` | `pipelines/templates/steps-deploy.yml` |

In every copied pipeline file, replace:
- `__SolutionName__` -> solution unique name (e.g., `GrantsManagement`)
- `__Solution__` -> solution acronym for environment names (e.g., `GRANTS`)
- `__solution__` -> solution name lowercase for URLs (e.g., `grants`)

## Step 6: Create `README.md`

Copy `assets/README-template.md` to `README.md` and replace all `{...}` placeholders with user-provided values.

## Step 7: Set Up Wiki Submodule

Present these commands to the user and offer to run them. Construct the submodule URL from `{AdoOrgUrl}` and `{AdoProject}`:

```powershell
# Extract orgName from AdoOrgUrl (last path segment)
# e.g. https://dev.azure.com/MNPDigital -> orgName = MNPDigital
git submodule add https://{orgName}@dev.azure.com/{orgName}/{AdoProject}/_git/{AdoProject}.wiki wiki
cd wiki
git checkout wikiMaster
cd ..
git submodule set-branch --branch wikiMaster wiki
git add .gitmodules wiki
git commit -m "chore: add wiki as git submodule"
```

> The wiki repository must exist in Azure DevOps before running this. Enable the Wiki feature in ADO project settings if it has not been enabled yet.

See `references/wiki-submodule-setup.md` for full details including post-clone initialization.

## Step 8: Initial Commit

```powershell
git add .
git commit -m "chore: initialize project repository structure"
```

## Post-Init Checklist

Output this checklist after completing all steps (substituting actual values):

```
Post-Initialization Checklist for {ProjectName}
================================================

Infrastructure
[ ] Create ADO environments: DC-{Solution}-DEV, DC-{Solution}-SIT, DC-{Solution}-UAT, DC-{Solution}-PROD
[ ] Configure manual approval checks on DC-{Solution}-SIT, -UAT, -PROD environments
[ ] Register pipelines from pipelines/build/, pipelines/export/, pipelines/deploy/
[ ] Create service principal; add AppId + ClientSecret as pipeline variable group secrets
[ ] Configure DLP policies (see references/environment-standards.md)

Dataverse
[ ] Verify publisher: MNP Digital, prefix: {Prefix}
[ ] Enable Dataverse Search on all environments
[ ] Enable Auditing on all environments (retain logs forever)
[ ] Create initial solution in DEV and export to src/solutions/{SolutionName}/

Wiki
[ ] Verify wiki submodule: git submodule update --init --recursive
[ ] Create wiki Home.md with project overview
[ ] Set up wiki .order files for navigation

.github Configuration
[ ] Update .github/copilot-instructions.md with team contacts and key entities
[ ] Verify .github/prompts/ files are working in Copilot Chat
[ ] Add any project-specific skills to .github/skills/

Power Pages (if applicable)
[ ] Create Power Pages site using Blank Template
[ ] Enable Enhanced Data Model when out of Preview
[ ] Configure SharePoint site: CRMDocuments{Environment}
```

## References

Read these files when additional detail is needed:

- **`references/repo-structure-standards.md`** — Full repo structure with folder-by-folder descriptions
- **`references/environment-standards.md`** — Environment naming, Dataverse configuration, DLP guidance
- **`references/wiki-submodule-setup.md`** — Wiki submodule commands, URL patterns, ADO wiki format rules
- **`references/pipeline-standards.md`** — Pipeline folder structure, naming, YAML patterns by type

## Example Prompts

- "Initialize a new project repo for a Grants solution called GrantsManagement"
- "Set up the folder structure and copilot instructions for the QUARTS project"
- "Create the wiki submodule and pipeline stubs for a new Benefits engagement"
- "Scaffold a new engagement repo for DC-PATH at https://dev.azure.com/MNPDigital"