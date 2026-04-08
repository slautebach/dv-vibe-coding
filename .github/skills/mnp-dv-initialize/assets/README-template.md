# {ProjectName}

> {One-sentence description of what this project delivers and who it's for.}

## Overview

{2-3 paragraph description of the engagement, the client, and the business problem being solved.}

**ADO Project**: [{AdoProject}]({AdoOrgUrl}/{AdoProject})  
**ADO Boards**: [{AdoProject} Boards]({AdoOrgUrl}/{AdoProject}/_boards)  
**Wiki**: [{AdoProject} Wiki]({AdoOrgUrl}/{AdoProject}/_wiki)

---

## Prerequisites

Before working with this repository, ensure you have the following installed and configured:

| Tool | Purpose | Install |
|---|---|---|
| [Power Platform CLI (pac)](https://learn.microsoft.com/en-us/power-platform/developer/cli/introduction) | Solution export/import, portal sync | `dotnet tool install --global Microsoft.PowerApps.CLI.Tool` |
| [.NET SDK 8.x](https://dotnet.microsoft.com/download) | Plugin development and builds | [Download](https://dotnet.microsoft.com/download) |
| [Node.js (LTS)](https://nodejs.org/) | Web resource development | [Download](https://nodejs.org/) |
| [PowerShell 7+](https://github.com/PowerShell/PowerShell) | Build and deployment scripts | [Download](https://github.com/PowerShell/PowerShell/releases) |
| [Git](https://git-scm.com/) | Source control | [Download](https://git-scm.com/) |
| [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) | ADO work item management | [Download](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) |

**Access required:**
- Azure DevOps project: `{AdoOrgUrl}/{AdoProject}`
- Power Platform DEV environment: `https://dc-{solution}-dev.crm3.dynamics.com`

---

## Getting Started

### Clone and Initialize

```powershell
# Clone the repository
git clone {repoUrl}
cd {repoDirectory}

# Initialize the wiki submodule
git submodule update --init --recursive
```

### Open in VS Code

```powershell
code .
```

GitHub Copilot will automatically pick up the `.github/copilot-instructions.md` and project skills.

---

## Repository Structure

```
/
├── .github/                    <- Copilot & AI tooling configuration
│   ├── copilot-instructions.md
│   ├── prompts/
│   └── skills/
├── docs/                       <- AI working library (internal, not published)
│   ├── meeting-transcripts/
│   ├── requirements/
│   ├── client-docs/
│   ├── external-docs/
│   ├── decisions/
│   └── generated/
├── src/                        <- Solution source code
│   ├── solutions/              <- Unpacked Dataverse solutions
│   ├── plugins/                <- C# plugin projects
│   ├── webresources/           <- JS/TS/HTML web resources
│   └── powerpages/             <- Power Pages portal source
├── wiki/                       <- ADO Wiki (git submodule)
├── pipelines/
│   ├── build/
│   ├── export/
│   ├── deploy/
│   ├── templates/
│   └── scripts/
└── README.md
```

---

## Development Workflow

1. **Create a feature branch** from `main`
2. **Make changes** in the Dataverse DEV environment
3. **Export the solution** — run the export pipeline or use `export-solution` skill
4. **Review the diff** in the unpacked solution files
5. **Commit** using the `git-commit` skill (conventional commits)
6. **Open a PR** — build pipeline validates the changes
7. **Merge to `main`** — triggers the CI build pipeline

---

## Pipelines

| Pipeline | File | Trigger |
|---|---|---|
| Build Solution | `pipelines/build/solution.yml` | Merge to `main` |
| Export Solution | `pipelines/export/solution.yml` | Manual |
| Deploy Solution | `pipelines/deploy/solution.yml` | Manual (multi-stage with approvals) |

---

## Key Contacts

| Role | Name | Contact |
|---|---|---|
| Engagement Lead | {EngagementLead} | {EngagementLeadEmail} |
| Tech Lead | {TechLead} | {TechLeadEmail} |
| Client Contact | {ClientContact} | {ClientContactEmail} |

---

## Wiki

Project documentation is in the `wiki/` git submodule, published to Azure DevOps:  
[{AdoProject} Wiki]({AdoOrgUrl}/{AdoProject}/_wiki)

To update the wiki, commit changes from within the `wiki/` submodule folder.
