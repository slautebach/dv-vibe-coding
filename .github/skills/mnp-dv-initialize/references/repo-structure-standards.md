# Repository Structure Standards

Source: wiki/Welcome/Platform-Delivery-Playbook/Delivery-Process/Using-Git-(Source-Control)/Repository-Structure.md

## Key Distinction: `docs/` vs `wiki/`

- **`docs/`** is the AI's working library — raw client artifacts, meeting notes, data exports, and AI-generated drafts that Copilot reads to understand the project. Internal, not published.
- **`wiki/`** is the official published documentation — reviewed, approved pages surfaced in Azure DevOps. Content flows *from* `docs/` *into* `wiki/` once reviewed.

## Standard Folder Structure

```
/
├── .github/
│   ├── copilot-instructions.md
│   ├── prompts/
│   │   ├── document-gathering.prompt.md
│   │   ├── solution-release-notes.prompt.md
│   │   └── portal-sync.prompt.md
│   └── skills/
│
├── docs/
│   ├── meeting-transcripts/
│   ├── requirements/
│   ├── client-docs/
│   ├── external-docs/
│   ├── decisions/
│   └── generated/
│       └── README.md
│
├── src/
│   ├── solutions/
│   ├── plugins/
│   ├── webresources/
│   └── powerpages/
│
├── wiki/                  <- git submodule -> ADO wiki repo
│
├── pipelines/
│   ├── build/
│   ├── export/
│   ├── deploy/
│   ├── templates/
│   └── scripts/
│
└── README.md
```

## Folder Purposes

### `.github/`
- `copilot-instructions.md` — Project-level instructions shaping Copilot behavior (overview, tech stack, conventions)
- `prompts/` — Reusable `.prompt.md` files for repeatable tasks
- `skills/` — Custom Copilot skills with instructions and supporting scripts

### `docs/`
AI working library. Raw input materials and AI-generated drafts.
- `meeting-transcripts/` — Workshop and meeting notes
- `requirements/` — Business and functional requirements
- `client-docs/` — Documents provided by the client
- `external-docs/` — Third-party and reference materials
- `decisions/` — Agreed decisions and approval records
- `generated/` — AI-generated docs staged for review (nothing published until promoted to wiki)

### `src/`
All solution source code tracked in git. Solutions unpacked via `pac solution unpack`.
- `solutions/` — Unpacked Dataverse solution folders, named after solution unique name
- `plugins/` — C# plugin and custom workflow activity projects
- `webresources/` — JS, TS, HTML, CSS web resources
- `powerpages/` — Power Pages portal source files

### `wiki/`
Git submodule pointing to the Azure DevOps Wiki repository (`<Project>.wiki`).
- Author pages directly in VS Code alongside source code
- Commit wiki changes *from within the submodule folder*, not the main repo
- Follow ADO wiki format: `.order` files, PascalCase page names, `::: mermaid` diagram blocks

### `pipelines/`
Azure DevOps YAML pipeline definitions:
- `build/` — Triggered on merges to `main`. Compiles plugins, packages solutions, produces artifacts.
- `export/` — Triggered by PRs or manually. Extracts and unpacks solutions from Dataverse.
- `deploy/` — Deploys packaged artifacts to target environments.
- `templates/` — Reusable YAML step templates shared across pipelines.
- `scripts/` — PowerShell scripts invoked by pipeline steps.

## Wiki Submodule Setup

```powershell
# Add wiki repo as a submodule
git submodule add https://<org>@dev.azure.com/<org>/<project>/_git/<project>.wiki wiki

# Pin to wikiMaster branch
cd wiki
git checkout wikiMaster
cd ..
git submodule set-branch --branch wikiMaster wiki

# Commit submodule registration
git add .gitmodules wiki
git commit -m "chore: add wiki as git submodule"
git push
```

**Initialize after cloning an existing repo:**
```powershell
git submodule update --init --recursive
```

## README.md

Root README should cover:
- Project name and brief description
- Prerequisites (tooling, permissions, environment access)
- How to clone and initialize the repo (including submodules)
- Links to key wiki pages and Azure DevOps project
- Contacts / team
