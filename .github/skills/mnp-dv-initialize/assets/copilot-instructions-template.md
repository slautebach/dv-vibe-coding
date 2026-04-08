# {ProjectName} - Copilot Instructions

## Project Overview

**{ProjectName}** is a Dynamics 365 / Power Platform engagement for **{ClientName}**. This repository contains all source code, pipeline definitions, and documentation for the solution.

- **Solution Name**: `{SolutionUniqueName}`
- **Publisher Prefix**: `{PublisherPrefix}`
- **Publisher**: MNP Digital
- **ADO Organization**: `{AdoOrgUrl}`
- **ADO Project**: `{AdoProject}`
- **ADO Board**: [{AdoProject} Boards]({AdoOrgUrl}/{AdoProject}/_boards)

## Technology Stack

- **Platform**: Microsoft Dynamics 365 / Dataverse
- **Power Platform**: Power Apps (Model-driven), Power Automate, Power Pages (if applicable)
- **Custom Development**:
  - C# plugins (`src/plugins/`)
  - JavaScript / TypeScript web resources (`src/webresources/`)
  - Power Pages portal (`src/powerpages/`)
- **Automation**: PowerShell scripts (`pipelines/scripts/`)
- **CI/CD**: Azure DevOps YAML pipelines (`pipelines/`)

## Repository Structure

```
/
├── .github/
│   ├── copilot-instructions.md   <- This file
│   ├── prompts/                  <- Reusable Copilot prompt files
│   └── skills/                   <- Custom Copilot skills
├── docs/                         <- AI working library (internal, not published)
│   ├── meeting-transcripts/
│   ├── requirements/
│   ├── client-docs/
│   ├── external-docs/
│   ├── decisions/
│   └── generated/
├── src/                          <- Solution source code
│   ├── solutions/                <- Unpacked Dataverse solutions
│   ├── plugins/                  <- C# plugin projects
│   ├── webresources/             <- JS/TS/HTML web resources
│   └── powerpages/               <- Power Pages portal source
├── wiki/                         <- ADO Wiki git submodule
├── pipelines/
│   ├── build/
│   ├── export/
│   ├── deploy/
│   ├── templates/
│   └── scripts/
└── README.md
```

## Key Entities and Components

<!-- Update this section as the project evolves -->

| Entity / Component | Description |
|---|---|
| `{prefix}_EntityName` | TODO: describe purpose |
| `{prefix}_AnotherEntity` | TODO: describe purpose |

## Environments

| Environment | URL | Purpose |
|---|---|---|
| DEV | `https://dc-{solution}-dev.crm3.dynamics.com` | Developer environment |
| SIT | `https://dc-{solution}-sit.crm3.dynamics.com` | QA / system integration testing |
| UAT | `https://dc-{solution}-uat.crm3.dynamics.com` | Client acceptance testing |
| PROD | `https://dc-{solution}.crm3.dynamics.com` | Production |

## Team Contacts

| Role | Name | Contact |
|---|---|---|
| Engagement Lead | {EngagementLead} | {EngagementLeadEmail} |
| Tech Lead | {TechLead} | {TechLeadEmail} |
| QA Lead | {QaLead} | {QaLeadEmail} |
| Client Contact | {ClientContact} | {ClientContactEmail} |

## Development Guidelines

### Working with Solutions

Export and unpack solutions using the `export-solution` skill or PowerShell:

```powershell
pac solution export --path ./export --name {SolutionUniqueName} --managed false
pac solution unpack --zipfile ./export/{SolutionUniqueName}.zip --folder ./src/solutions/{SolutionUniqueName}
```

### Plugins

- Plugin projects are in `src/plugins/`
- Build with: `dotnet build src/plugins/{PluginProject}.csproj -c Release`
- Register using the Plugin Registration Tool or pipelines

### Web Resources

- Web resources are in `src/webresources/`
- Follow MNP Common JS library patterns for form scripting

### Power Pages

- Portal source is in `src/powerpages/`
- Sync with: `pac pages download --path src/powerpages`

### Git Workflow

1. Create a feature branch from `main`
2. Make changes in your Dataverse DEV environment
3. Export solution using the export pipeline or `export-solution` skill
4. Review the unpacked solution diff
5. Commit using the `git-commit` skill for conventional commit messages
6. Open a pull request — build pipeline validates the PR
7. Merge to `main` triggers the build pipeline

### Wiki Authoring

The `wiki/` folder is a git submodule. Commit wiki changes from within the submodule:

```powershell
cd wiki
git add .
git commit -m "docs: update solution overview"
git push
cd ..
git add wiki && git commit -m "chore: update wiki pointer"
```

## Available Skills

- **export-solution** — Export and unpack Dataverse solutions using pac CLI
- **dataverse-solution-parser** — Parse and document Dataverse solution XML components
- **dv-doc-entity** — Generate entity documentation from live Dataverse metadata
- **dv-doc-flows** — Analyze and document Power Automate cloud flows
- **dv-doc-plugin-steps** — Document plugin assemblies and SDK message processing steps
- **git-commit** — Intelligent git commits with conventional commit messages
- **ado-backlog** — Manage Azure DevOps work items via az CLI
- **doc-coauthoring** — Co-author structured documentation
- **mermaid-expert** — Create flowcharts, sequence diagrams, and visualizations
- **microsoft-docs** — Query official Microsoft documentation
- **microsoft-code-reference** — Look up Microsoft API references and code samples

## Azure DevOps Backlog

```bash
az devops configure --defaults organization={AdoOrgUrl} project={AdoProject}
```

## Build and Deployment

### Build Pipeline

Triggered on merge to `main`:
```
pipelines/build/solution.yml
```

### Export Pipeline

Triggered manually or on PR to capture Dataverse changes:
```
pipelines/export/solution.yml
```

### Deploy Pipeline

Multi-stage: DEV -> SIT -> UAT -> PROD with manual approval gates:
```
pipelines/deploy/solution.yml
```
