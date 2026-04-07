# Dynamics 365 Starter Kits - Copilot Instructions

## Project Overview

This repository contains reusable **Dynamics 365 / Dataverse Starter Kits** - modular, pre-built solutions and shared libraries designed to accelerate Power Platform development. The starter kits provide common functionality, automation scripts, and best practices for building enterprise Dynamics 365 solutions.

## Technology Stack

- **Platform**: Microsoft Dynamics 365 / Dataverse
- **Power Platform**: Power Apps (Model-driven & Canvas), Power Automate, Power Pages
- **Custom Development**:
  - C# plugins and custom workflows
  - PCF (Power Apps Component Framework) controls
  - TypeScript for web resources and PCF
  - JavaScript client API libraries
- **Automation**: PowerShell build and export scripts
- **CI/CD**: Azure DevOps YAML pipelines
- **Configuration Management**: YAML-based package definitions

## Repository Structure

### StarterKits/

Contains modular starter kit solutions that can be independently packaged and deployed:

- **AIServiceConnector/** - AI service integration components
- **CCX/** - Contact Center Experience solution with portal components
- **MNPClientAPI/** - Shared client-side JavaScript API library

Each starter kit has:

- **Package.yml** - Configuration for versioning, build settings, and deployment
- **Solutions/** - Unpacked Dataverse solution components
- **Portals/** - Power Pages portal configuration (if applicable)

### SharedLibraries/

Reusable components shared across multiple projects:

- **ClientAPI/** - JavaScript libraries for Dynamics 365 forms
  - `mnp_Common.FormHelpers.js` - Form, field, and tab utilities
  - `mnp_Common.Translations.js` - Centralized translation management
  - `mnp_Common.Security.js` - Role-based security validation
  - `mnp_Common.Utilities.js` - General utility functions (age calculation, etc.)
- **dotnet/** - .NET shared libraries and utilities
- **LiquidRuleEngine/** - Custom rule engine using Liquid templating
- **PCF/** - Shared PCF component templates and utilities
- **PS-Modules/** - PowerShell modules for automation
  - `Azure-CLI.psm1` - Azure CLI helpers
  - `Build-Package.psm1` - Package building functions
  - `Dataverse-API.psm1` - Dataverse Web API functions
  - `Extract-Solution-Components.psm1` - Solution export/unpack utilities
  - `PP-CLI.psm1` - Power Platform CLI wrappers
  - `WebApi-Functions.psm1` - Web API helper functions
- **PS-Scripts/** - PowerShell helper scripts

### BuildScripts/

PowerShell automation for solution management:

- **Export-Solution.ps1** - Export and unpack solutions from Dataverse
- **Export-Data.ps1** - Export configuration data
- **Export-Portals.ps1** - Export Power Pages portal configuration
- **Build-Solution.ps1** - Build solution packages
- **Build-Plugins.ps1** - Compile plugin assemblies
- **Build-Data.ps1** - Build data packages
- **Build-Portals.ps1** - Build portal packages

### DeployScripts/

Deployment automation scripts:

- **UpdateConnectionReferences.ps1** - Update environment-specific connections
- **SetWorkflowsPlugins.ps1** - Configure workflow and plugin states
- **ActivateWorkflows.ps1** - Activate workflows post-deployment
- **CheckSolutionExists.ps1** - Validate solution presence

### DevOps-Pipelines/

Azure DevOps YAML pipeline definitions:

- **DevOps-Pipeline-Build.yml** - Main build pipeline for packaging
- **DevOps-Pipeline-BuildPullRequest.yml** - PR validation builds
- **DevOps-Pipeline-Export-Solution-PullRequest.yml** - Auto-export solutions on PR
- **DevOps-Pipeline-Export-Data-PullRequest.yml** - Auto-export data on PR
- **DevOps-Pipeline-Export-Portal-PullRequest.yml** - Auto-export portals on PR

### PCF/

Power Apps Component Framework controls:

- **MNPAG-Grid/** - Custom AG Grid PCF control
  - TypeScript-based PCF component
  - npm package management
  - ESLint configuration

### Portals/

Power Pages portal web resources:

- **SharedJS/** - Shared JavaScript libraries for portals
  - `mnp_common.js` - Common portal functions
  - `portalwebapiwrapper.js` - Portal Web API wrapper

### Plugins/

Custom C# plugin development for Dataverse business logic extensions.

## Development Guidelines

### Working with Starter Kits

1. **Package Configuration**: Each starter kit has a `Package.yml` defining:
   - Build settings (Solution, Portal, Data, Plugins)
   - Version numbers (Major/Minor)
   - Solution name
   - Portal IDs
   - DevOps organization settings

2. **Exporting Solutions**: Use PowerShell scripts or the `export-solution` skill

   ```powershell
   .\BuildScripts\Export-Solution.ps1 -targetEnvironment "yourorg" -starterKit "MNPClientAPI"
   ```

3. **Building Packages**: Use Build-Solution.ps1 to create deployment packages
   ```powershell
   .\BuildScripts\Build-Solution.ps1 -starterKit "CCX"
   ```

### Working with Dataverse Solutions

1. **Solution Analysis**: Use the `dataverse-solution-parser` skill to analyze Entity.xml, FormXml, and other solution components
2. **Flow Documentation**: Use the `dataverse-analyze-flows` skill to document Power Automate cloud flows
3. **Export Automation**: Use the `export-solution` skill for extracting solutions from Dataverse environments

### Git Workflow

Use the `git-commit` skill for intelligent commits:

- Analyzes changes and generates conventional commit messages
- Auto-detects commit type (feat, fix, docs, refactor, etc.)
- Intelligently groups related files
- Supports interactive commit with type/scope/description overrides

### Azure DevOps Backlog

Use the `ado-backlog` skill to view, manage, and update work items for this project.

**Project configuration:**

| Setting | Value |
|---|---|
| Organization | `MNPDigital` |
| Project | `DC-Delivery` |
| Project URL | `https://dev.azure.com/MNPDigital/DC-Delivery` |

Set these as CLI defaults once per session to avoid repeating them on every command:

```bash
az devops configure --defaults organization=https://dev.azure.com/MNPDigital project=DC-Delivery
```

**When to use the `ado-backlog` skill:**

- Browse and query backlog items (Epics, Features, User Stories, Tasks, Bugs)
- Create, update, or triage work items
- Check sprint progress and board status
- Link work items to other items via relations

**Example triggers:**

- "Show me the current sprint backlog"
- "Create a user story for the new claim validation feature"
- "What bugs are open in the current iteration?"
- "Update the status of work item #123"
- "Show me all active tasks assigned to me"

### Documentation Standards

1. **Technical Documentation**: Use the `doc-coauthoring` skill for structured documentation workflows
2. **Diagrams**:
   - Use the `mermaid-expert` skill for flowcharts, sequence diagrams, and visualizations
   - Use the `plantuml` skill for UML diagrams, ERD diagrams, and software architecture documentation
3. **Architecture Decision Records**: Document significant decisions in Documentation/

### Wiki Documentation

The `wiki/` folder is the main documentation hub, maintained with AI assistance. **All wiki files MUST strictly follow Azure DevOps wiki format — no exceptions.**

#### Structure Rules (ABSOLUTE)

- **Root page**: MUST be `wiki/Home.md` — this is the wiki home/landing page
- **Section pages**: A `.md` file at the root of `wiki/` named after the section (e.g., `wiki/Plugins.md`)
- **Sub-pages**: MUST be placed inside a folder with the same name as the parent page (e.g., `wiki/Plugins/My-Sub-Page.md`)
- **File names**: MUST use `PascalCase` or `Hyphenated-Names` for multi-word titles (e.g., `Linked-Services.md`)
- **NEVER use `README.md`**: Azure DevOps wiki does not support `README.md` — always use named `.md` files

#### Page Ordering (ABSOLUTE)

- Every folder containing wiki pages MUST have a `.order` file
- The `.order` file lists page names **without** the `.md` extension, one per line, in the desired display order

#### Special Wiki Tokens

- `[[_TOC_]]` — Inserts an auto-generated **table of contents** based on headings in the current page. Place at the top of long pages.
- `[[_TOSP_]]` — Inserts an auto-generated **table of sub-pages** for the current page. Place on section overview pages to list child pages.

#### Mermaid Diagrams (ABSOLUTE)

- MUST use `::: mermaid` / `:::` delimiters to render a diagram — backtick fences (` ```mermaid ``` `) are supported in Azure DevOps wiki but display the source as a code block, not as a rendered diagram
- MUST use `<br/>` for line breaks inside node labels — **NEVER use `\n`**

#### Folder Structure Pattern

```
wiki/
├── Home.md               ← Wiki root page
├── .order                ← Top-level nav order
├── SectionName.md        ← Section overview page
└── SectionName/          ← Sub-pages for that section
    ├── .order
    └── Sub-Page-Name.md
```

### Microsoft Technology Integration

1. **API Reference**: Use `microsoft-code-reference` skill to look up Microsoft API references and SDK code samples
2. **Documentation**: Use `microsoft-docs` skill for querying official Microsoft documentation for Power Platform, .NET, Azure, etc.

### Document Processing

Available skills for working with various document formats:

- **docx** - Word documents with tracked changes and comments
- **xlsx** - Excel spreadsheets with formulas and data analysis
- **pptx** - PowerPoint presentations
- **pdf** - PDF manipulation and form filling

### PCF Development

1. **Technology**: TypeScript, npm, ESLint
2. **Structure**: PCF components in PCF/ folder with standard PCF project structure
3. **Build**: Use npm scripts defined in package.json
4. **Integration**: PCF components are packaged in solution zip files

## Build and Deployment

### Build, test, and lint commands

- PCF (MNPAG-Grid) — run from src\PCF\MNPAG-Grid:
  - npm run build  — build the PCF control
  - npm run start  — run a local dev server/watch
  - npm run lint   — run ESLint
  - npm run lint:fix — auto-fix lint issues

- Solutions and packages (PowerShell scripts) — run from the repository root:
  - .\BuildScripts\Build-Solution.ps1 -starterKit "<name>"  — build deployment package for a starter kit
  - .\BuildScripts\Export-Solution.ps1 -targetEnvironment "<org>" -starterKit "<name>"  — export and unpack a solution from Dataverse
  - .\BuildScripts\Build-Plugins.ps1  — compile plugin assemblies (use dotnet SDK for project builds)

- .NET plugin projects:
  - dotnet build <path-to-project.csproj> -c Release  — build a plugin or library project
  - dotnet test <path-to-test-project.csproj>  — run tests for a test project (no test projects detected in this repo)

- Single-test guidance:
  - No dedicated test runner or test projects were found; for .NET tests use:
    dotnet test <test-project.csproj> --filter "FullyQualifiedName=Namespace.Class.Method"

## Build and Deployment

### Prerequisites

- **Power Platform CLI (pac)** - For solution operations
- **.NET SDK** - For plugin development
- **Node.js & npm** - For PCF and web resource development
- **PowerShell 7+** - For running build/export scripts
- **Azure DevOps** - For CI/CD pipelines

### Local Development Workflow

1. **Make changes** in your Dataverse environment
2. **Export solution** using Export-Solution.ps1 or `export-solution` skill
3. **Build package** using Build-Solution.ps1
4. **Commit changes** using `git-commit` skill for conventional commits
5. **Push to repository** to trigger DevOps pipelines

### CI/CD Pipeline

- **Build Pipeline**: Compiles all components and creates deployment artifacts
- **PR Pipelines**: Validate builds and auto-export solutions/data/portals
- **Environment-specific**: Pipelines support multiple target environments
- **Artifact Publishing**: Build artifacts published for release pipelines

### Package.yml Configuration

Key settings in Package.yml:

```yaml
BuildPackages:
  Solution: true # Enable solution build
  Portal: true # Enable portal build
  Data: true # Enable data export
  Plugins: true # Enable plugin build

MajorVersion: 1
MinorVersion: 0

DataverseDomain: crm3.dynamics.com
SolutionName: YourSolutionName

Portals:
  ModelVersion: 1
  PortalIds:
    - <portal-guid>
```

## Best Practices

1. **Modular Design**: Keep starter kits focused and independent
2. **Shared Libraries**: Use SharedLibraries/ for cross-cutting concerns
3. **Version Control**: Always export solutions to source control before deployment
4. **PowerShell Modules**: Leverage PS-Modules for reusable automation
5. **Package Configuration**: Keep Package.yml up to date with accurate versioning
6. **Client API**: Use MNP Common libraries for consistent client-side development
7. **Testing**: Test in lower environments before production deployment
8. **Documentation**: Document custom functionality and architecture decisions

## Common Tasks

### "Export a starter kit solution"

```powershell
.\BuildScripts\Export-Solution.ps1 -targetEnvironment "myorg" -starterKit "MNPClientAPI"
```

Or use the `export-solution` skill for guided export.

### "Build a deployment package"

```powershell
.\BuildScripts\Build-Solution.ps1 -starterKit "CCX"
```

### "Analyze solution components"

Use the `dataverse-solution-parser` skill to parse and document Entity.xml, FormXml, and other solution components.

### "Document Power Automate flows"

Use the `dataverse-analyze-flows` skill to generate comprehensive flow documentation.

### "Create technical documentation"

1. Use `doc-coauthoring` skill for structured docs
2. Use `mermaid-expert` or `plantuml` for diagrams
3. Store in Documentation/ folder

### "Research Power Platform APIs"

1. Use `microsoft-docs` for conceptual information
2. Use `microsoft-code-reference` for code samples and API details

### "Commit changes with conventional commits"

Use the `git-commit` skill to analyze changes and generate properly formatted commit messages.

## Available Skills

The following specialized skills are available for this project:

### Core Project Skills

- **export-solution** - Export and unpack Dynamics 365/Dataverse solutions using pac CLI
- **dataverse-solution-parser** - Parse and analyze Dataverse solution XML files (Entity.xml, FormXml, etc.)
- **dataverse-analyze-flows** - Analyze Power Automate cloud flows and generate documentation
- **git-commit** - Execute git commits with conventional commit messages and intelligent staging
- **ado-backlog** - View, query, create, and update Azure DevOps work items using the az CLI

### Documentation & Diagramming

- **doc-coauthoring** - Guide for co-authoring structured documentation
- **mermaid-expert** - Create flowcharts, sequence diagrams, class diagrams, and other Mermaid.js visualizations
- **plantuml** - Create UML diagrams, sequence diagrams, class diagrams, and other PlantUML visualizations

### Microsoft Technology

- **microsoft-code-reference** - Look up Microsoft API references, find code samples, and verify SDK code
- **microsoft-docs** - Query official Microsoft documentation (Azure, .NET, Power Platform, etc.)

### Document Processing

- **docx** - Create, edit, and analyze Word documents with tracked changes and comments
- **xlsx** - Create, edit, and analyze Excel spreadsheets with formulas and data analysis
- **pptx** - Create, edit, and analyze PowerPoint presentations
- **pdf** - Extract text, create PDFs, merge/split documents, and fill forms

### Communication & Development

- **internal-comms** - Write internal communications (status reports, updates, FAQs, etc.)
- **vscode-ext-commands** - Guidelines for contributing commands in VS Code extensions
- **vscode-ext-localization** - Guidelines for proper localization of VS Code extensions

### Meta

- **skill-creator** - Guide for creating new custom skills to extend GitHub Copilot capabilities

---

## Getting Help

When working with this repository:

1. Reference the appropriate skill based on your task
2. Check SharedLibraries/ for reusable components
3. Review Package.yml in each starter kit for configuration
4. Consult BuildScripts/ for automation capabilities
5. Review DevOps-Pipelines/README.md for CI/CD documentation

## Project Information

This is a modular starter kit framework for accelerating Dynamics 365 / Power Platform development by MNP Digital.
