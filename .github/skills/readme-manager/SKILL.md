---
name: readme-manager
description: Reviews and updates an existing README.md or creates a new README.md for a specified folder. Reads existing README and referenced documents for context, analyzes folder structure and files, loads related skills based on folder content, reviews recent git changes, and produces an up-to-date README. Use when asked to "review README", "update README", "create README", "document this folder", or "onboard developers to this folder". Do NOT use for documenting individual files (only folders) or for generating non-README documentation.
---

# Readme Manager

Reviews and updates existing README.md files, or creates new ones, to keep folder documentation accurate and useful for onboarding new developers and orienting existing ones.

## Workflow

Determine which path applies, then follow it:

**README exists?** → Follow [Update Existing README](#update-existing-readme)  
**README missing?** → Follow [Create New README](#create-new-readme)

---

## Update Existing README

1. **Read the existing README** — note its current structure, sections, and any linked documents
2. **Read all referenced documents** — load any files linked from the README for full context
3. **Analyze the folder** — use glob/view to survey the current folder structure and key files; note what has changed since the README was last written
4. **Check recent changes** — run `git log --oneline -20 -- <folder>` and `git diff HEAD~10 HEAD -- <folder>` to identify what has been added, removed, or modified
5. **Load related skills** — based on folder content, invoke relevant skills (e.g., `dataverse-solution-parser` for D365 solutions, `north52-formula-analyzer` for North52 formulas, `dataverse-analyze-flows` for Power Automate flows) to enrich context
6. **Identify gaps and stale content** — compare current folder state to README; flag missing components, outdated descriptions, and broken references
7. **Update the README** — apply targeted edits; preserve accurate sections; see [references/readme-structure.md](references/readme-structure.md) for structure guidance

---

## Create New README

1. **Analyze the folder** — use glob/view to map the full folder structure; identify sub-folders, key files, entry points, and patterns
2. **Check for child READMEs** — find any README.md files in sub-folders and read them to understand what is already documented
3. **Check recent git history** — run `git log --oneline -20 -- <folder>` to understand recent activity and purpose
4. **Load related skills** — based on folder content, invoke relevant skills to gain domain context before writing
5. **Write the README** — follow the structure in [references/readme-structure.md](references/readme-structure.md); link to child READMEs; focus on onboarding value

---

## Skill Loading Heuristics

Match folder content to skills:

| Folder contains | Load skill |
|-----------------|-----------|
| D365/Dataverse solution XML | `dataverse-solution-parser` |
| Power Automate cloud flows | `dataverse-analyze-flows` |
| North52 formula files | `north52-formula-analyzer` |
| `.docx` files | `docx` |
| `.xlsx` / `.csv` files | `xlsx` |
| `.pdf` files | `pdf` |
| Azure DevOps pipeline YML | `authoring-azure-devops-pipelines` |
| Mermaid diagram files | `mermaid-expert` |
| PlantUML files | `plantuml` |

---

## Quality Checklist

Before finalising the README, verify:

- [ ] Purpose of the folder is clear in the first paragraph
- [ ] All significant sub-folders and files are described
- [ ] Child README.md files are linked with a brief description
- [ ] Getting-started or setup steps are present where relevant
- [ ] No broken links or references to files that no longer exist
- [ ] Recent changes are reflected (nothing missing from git log)
