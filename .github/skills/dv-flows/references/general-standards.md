# General Standards for Power Automate Flows

Source: MNP Platform Delivery Playbook

## Purpose

- Make flows easily readable and understood by the entire team
- Create better-executing flows from a performance, resilience, extensibility, and quality standpoint
- Minimize false negatives by using Try-Catch-Finally or Terminate steps

## Naming Conventions

| Trigger Type | Pattern | Example |
|---|---|---|
| Dataverse / table-triggered | `{Table} - {Action} - MNP` | `Application - Process Submission - MNP` |
| HTTP (instant / webhook) | `HTTP - {Action} - MNP` | `HTTP - Submit to Financial - MNP` |
| Scheduled (recurrence) | `{RecurrencePeriod} - {Action} - MNP` | `Daily - Sync Payments - MNP` |

Recurrence period values: **Daily**, **Monthly**, **Yearly**, etc.

> **Note:** HTTP flows carry inherent risks when called from untrusted networks. Always add protection to ensure calls originate from trusted sources.

## Connection References

- **Always use Connection References** — never hardcode connections directly into flow actions.
- Connection references enable portability across environments: DEV → SIT → UAT → PROD.
- Do **not** create new connection references arbitrarily; verify the correct existing one is used.
- See [connection-references.md](connection-references.md) for detailed guidance.

## Flow Step Standards

- **Name every step in plain English** to improve readability (e.g., "Get Application Record", not "Get row by ID").
- **Add Notes to steps** to provide additional context or explain non-obvious logic.

## Dataverse Request Limits

Always be aware of platform limits. Key thresholds:

| Limit | Value |
|---|---|
| Actions per workflow | 500 |
| Max nesting depth | 8 levels |
| Apply to Each array size | 100,000 items (5,000 for Low profile) |
| Apply to Each concurrency | 1–50 (default 1) |
| Run duration | 30 days |
| Concurrent runs (with concurrency on) | 1–100 (default 25) |
| Daily requests — Dynamics 365 Enterprise user | 40,000 |
| Daily requests — Power Automate per flow plan | 250,000 |

Reference: [Power Automate Limits and Config](https://learn.microsoft.com/en-us/power-automate/limits-and-config)

## Try-Catch-Finally Pattern

Every flow must implement error handling using a Scope-based Try-Catch-Finally pattern to prevent silent failures.

### Structure

```
Scope: Try
  └─ [Main flow logic]

Scope: Catch
  Run after: Try → has failed / has timed out / was skipped
  └─ [Error handling: log, notify, or compensate]
  └─ Terminate action (Failed) — mark flow run as failed explicitly

Scope: Finally  
  Run after: Try → succeeded; Catch → succeeded/failed/skipped
  └─ [Cleanup or always-run tasks]
```

### Key Rules

- Set **Run After** on Catch scope to trigger on: `has failed`, `has timed out`, `has been skipped`.
- Always include a **Terminate** action inside Catch with Status = `Failed` — do not let failed flows appear as succeeded.
- Use Finally for guaranteed cleanup steps (e.g., releasing locks, sending completion signals).
- Flows that silently succeed despite errors create harder-to-diagnose data quality issues.
