# README Structure Guide

## Table of Contents

- [Core Principles](#core-principles)
- [Recommended Structure](#recommended-structure)
- [Section Guidance](#section-guidance)
- [Folder-Type Variations](#folder-type-variations)
- [Linking Child READMEs](#linking-child-readmes)

---

## Core Principles

- **Open with the "why"** — first paragraph answers: what is this folder and why does it exist?
- **Audience is developers** — assume technical readers; skip business context unless it aids understanding
- **Keep it scannable** — use headings, tables, and bullet lists; avoid long prose paragraphs
- **Reflect reality** — only document what exists; remove references to deleted or moved things
- **Link, don't repeat** — link to child READMEs and external docs rather than duplicating content

---

## Recommended Structure

Use your judgment about which sections are relevant; not every folder needs every section.

```markdown
# <Folder Name>

Brief (1–3 sentence) description: what this folder contains and its role in the project.

## Contents

Overview of the folder's structure — sub-folders and important files.

## Getting Started

Steps a new developer needs to take to work with this folder
(setup, install, run, etc.). Omit if no setup is required.

## Key Concepts

Domain knowledge or architecture notes needed to understand the code.
Omit if self-evident from code or documented elsewhere.

## Sub-Folders

Links to child README.md files with one-line descriptions.

## Related Documentation

Links to broader project docs, wikis, or external references.
```

---

## Section Guidance

### Opening description
- One paragraph, 1–3 sentences
- Answer: what lives here, and why?
- Example: *"Contains the unpacked Dynamics 365 Core solution. This is the primary solution component including entities, forms, views, and business rules."*

### Contents / Folder Structure
- Use a table or bullet list
- Describe each significant sub-folder and file
- Skip generated/build artifacts unless developers need to know about them

```markdown
| Path | Description |
|------|-------------|
| `scripts/` | Deployment and utility scripts |
| `references/` | Reference documentation loaded by skills |
| `SKILL.md` | Skill definition and workflow |
```

### Getting Started
Include only when there is actual setup or onboarding work:
- Prerequisites (tools, access, environment)
- Install / build steps
- How to run or test
- Common first tasks

### Key Concepts
Include domain knowledge that is not obvious from code:
- Architecture decisions
- Data model overview
- Integration patterns
- Important conventions or constraints

### Sub-Folders (Child READMEs)
Always list child READMEs when they exist:

```markdown
## Sub-Folders

- [IncomeAssistanceCore/](IncomeAssistanceCore/README.md) — Core entities, forms, views, and business logic
- [IncomeAssistanceNorth52/](IncomeAssistanceNorth52/README.md) — North52 Decision Suite formula components
```

---

## Folder-Type Variations

### Source code / plugin folders
Emphasise: entry points, build commands, test commands, key classes or namespaces.

### D365 solution folders
Emphasise: solution purpose, key components (entities, workflows, web resources), dependencies on other solutions.

### Documentation folders
Emphasise: what is documented, how documentation is organised, how to contribute or update docs.

### Pipeline / CI-CD folders
Emphasise: what each pipeline does, when it runs, required variables and secrets, deployment targets.

### Integration folders
Emphasise: what systems are integrated, direction of data flow, authentication approach, key message types.

### Data migration folders
Emphasise: what data is migrated, source/target systems, how to run migrations, rollback approach.

---

## Linking Child READMEs

When child README.md files exist, always include a **Sub-Folders** section that:
1. Lists each child folder that has a README.md
2. Provides a relative link to the child README
3. Includes a one-line description of what the child folder contains

Do not reproduce content from child READMEs — link to them instead.
