---
name: dv-flows
description: Author and review Power Automate cloud flows following MNP standards -- naming conventions, connection references, error handling (Try-Catch-Finally), Dataverse limits, HTTP security, and scheduled flow patterns. Use when asked to "create a flow", "scaffold a cloud flow", "review a flow", "check flow standards", "name a flow", or "set up a Power Automate flow". Do NOT use for documenting existing flows from Dataverse (use dv-doc-flows skill).
---

# Dv Flows

## Overview

Author and review Power Automate cloud flows against MNP naming standards, connection reference rules, error handling patterns, and Dataverse limit guidance.

## Naming Convention (Quick Reference)

| Trigger | Pattern | Example |
|---|---|---|
| Dataverse / table | `{Table} - {Action} - MNP` | `Application - Process Submission - MNP` |
| HTTP (instant) | `HTTP - {Action} - MNP` | `HTTP - Submit to Financial - MNP` |
| Scheduled | `{RecurrencePeriod} - {Action} - MNP` | `Daily - Sync Payments - MNP` |

## Standards Checklist

When authoring or reviewing any flow, verify:

- [ ] **Name** matches the correct pattern for the trigger type
- [ ] **Connection References** used -- no hardcoded connections
- [ ] **Try-Catch-Finally** scopes implemented (Terminate in Catch with Status=Failed)
- [ ] **Step names** are plain English; notes added to non-obvious steps
- [ ] **Dataverse queries** use FetchXML/OData filters and select only required columns
- [ ] **Apply to Each** loops have concurrency configured and dataset is bounded
- [ ] **HTTP flows** have additional auth / trusted source validation
- [ ] **Scheduled flows** are idempotent and have concurrency control set to 1

## Workflow

### 1. Identify Flow Type

Determine the trigger to select naming and standards:
- **Dataverse trigger** (row added/modified/deleted) -> apply [dataverse-flow-standards.md](references/dataverse-flow-standards.md)
- **HTTP trigger** (instant/webhook) -> apply [http-flow-standards.md](references/http-flow-standards.md)
- **Recurrence trigger** (scheduled) -> apply [scheduled-flow-standards.md](references/scheduled-flow-standards.md)

All flow types also apply [general-standards.md](references/general-standards.md).

### 2. Apply General Standards

Read [general-standards.md](references/general-standards.md) for:
- Naming conventions for all trigger types
- Connection reference requirements
- Step naming and notes standards
- Try-Catch-Finally pattern with Terminate action
- Dataverse platform limits summary

### 3. Apply Type-Specific Standards

| Flow Type | Reference File | Key Concerns |
|---|---|---|
| Dataverse | [dataverse-flow-standards.md](references/dataverse-flow-standards.md) | FetchXML filters, column selection, row count, async design |
| HTTP | [http-flow-standards.md](references/http-flow-standards.md) | AAD auth, trusted source check, structured response |
| Scheduled | [scheduled-flow-standards.md](references/scheduled-flow-standards.md) | Idempotency, concurrency control=1, overlap handling |

### 4. Connection References

Read [connection-references.md](references/connection-references.md) for:
- Why to always use connection references (DEV/SIT/UAT/PROD portability)
- How to reuse existing ones (do not create duplicates)
- Naming convention: `{Connector} - {Context}` (e.g., `Dataverse - DC Starter Kit`)

### 5. Authoring a New Flow

When scaffolding a new flow:
1. Confirm the trigger type and derive the name.
2. Confirm the connection reference(s) needed -- verify existing ones in the solution.
3. Scaffold the outer Try-Catch-Finally scope structure first.
4. Add the trigger conditions (filter at trigger level for Dataverse flows).
5. Build the main logic inside the Try scope.
6. Add error logging / Terminate(Failed) in Catch.
7. Name all steps in plain English; add notes to non-obvious actions.

### 6. Reviewing an Existing Flow

When reviewing a flow definition:
1. Check the name against the naming pattern.
2. Verify all connectors use connection references (no direct connections).
3. Confirm Try-Catch-Finally with Terminate is present.
4. Check Dataverse queries for filters and column selection.
5. Check Apply to Each loops for concurrency settings.
6. For HTTP flows: verify auth mechanism.
7. For scheduled flows: verify idempotency design and concurrency=1.

## Example Prompts Handled

- "Create a Power Automate flow that triggers when an Application is submitted and sends a confirmation email"
  - Name: `Application - Send Confirmation Email - MNP`
  - Trigger: When a row is added (Application table)
  - Standards: Dataverse flow standards + general standards

- "Review this flow definition and flag any MNP standards violations"
  - Run through the Standards Checklist above

- "What is the correct naming for a daily scheduled flow that syncs payment records?"
  - `Daily - Sync Payments - MNP`

- "How should I handle errors in a Dataverse-triggered flow?"
  - Implement Try-Catch-Finally scopes; see general-standards.md for the full pattern