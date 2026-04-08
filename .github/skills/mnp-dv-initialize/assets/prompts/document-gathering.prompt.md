---
mode: agent
description: Collect and organize client artifacts, meeting notes, requirements, and reference materials into the docs/ folder structure. Run when starting a new engagement or after receiving new materials from the client.
---

# Document Gathering

Your task is to help organize and catalogue project documents into the standard `docs/` folder structure.

## Steps

1. **Inventory what exists** — List all files currently in `docs/` and its sub-folders.

2. **Ask the user what new materials are available** — Prompt:
   > "Do you have any new documents to add? For each, tell me: (a) the file name or content, (b) what type it is (meeting notes, requirements, client doc, decision, external reference), and (c) any context about when it was created or what it covers."

3. **Classify each document** into the correct sub-folder:

   | Document Type | Sub-folder |
   |---|---|
   | Workshop or meeting notes / transcripts | `docs/meeting-transcripts/` |
   | Business or functional requirements, user stories, acceptance criteria | `docs/requirements/` |
   | Documents provided by the client | `docs/client-docs/` |
   | Third-party specs, vendor docs, integration guides | `docs/external-docs/` |
   | Agreed decisions, approval records, key email threads | `docs/decisions/` |
   | AI-generated drafts staged for review | `docs/generated/` |

4. **Suggest a file name** for each document using kebab-case with a date prefix where relevant:
   - Meeting notes: `YYYY-MM-DD-{topic}-notes.md`
   - Requirements: `{feature-area}-requirements.md`
   - Decisions: `YYYY-MM-DD-{decision-topic}.md`
   - Client docs: use original name, normalized to kebab-case

5. **Create or move the files** as directed by the user.

6. **Summarize** what was organized:
   - List each file with its destination path
   - Flag any documents that seem sensitive — remind the user: "Do not commit sensitive client data without approval."

## Guidelines

- If a document covers multiple types, place it in the most specific applicable folder and note the other topics it covers.
- For meeting transcripts, extract and save a brief summary at the top (participants, date, key outcomes, action items).
- For requirements docs, note the source (e.g., "from client workshop 2025-01-15") at the top.
- For decisions, use this template at the top:
  ```
  **Decision**: {one-line summary}
  **Date**: {date}
  **Decided by**: {names/roles}
  **Context**: {brief context}
  **Outcome**: {what was agreed}
  ```
