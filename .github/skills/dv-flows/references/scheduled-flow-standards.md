# Scheduled Flow Standards

Source: MNP Platform Delivery Playbook

## Purpose

- Make scheduled flows readable and understood by the entire team.
- Ensure resilience and correct behaviour when runs overlap or data is re-processed.
- Minimize false negatives by using Try-Catch-Finally or Terminate steps.

## Naming

Pattern: `{RecurrencePeriod} - {Action} - MNP`

| Part | Description | Examples |
|---|---|---|
| `{RecurrencePeriod}` | How often the flow runs | `Daily`, `Monthly`, `Yearly`, `Hourly`, `Weekly` |
| `{Action}` | What the flow does | `Sync Payments`, `Generate Reports`, `Expire Records` |

Full examples:
- `Daily - Sync Payments - MNP`
- `Monthly - Generate Invoices - MNP`

## Idempotency Requirement

Scheduled flows **must be idempotent** — running them multiple times for the same period must produce the same result.

### Design Patterns for Idempotency

- Use a **status/flag field** on records to track processing state (e.g., `Sync Status = Pending → Processed`).
- Filter records at the trigger query level: only fetch unprocessed records.
- Use **upsert** (Patch with alternate key) instead of Create to avoid duplicates.
- Record the last successful run timestamp and use it as a filter anchor.

## Run Overlap Handling

Power Automate does not prevent concurrent runs of the same scheduled flow by default.

| Setting | Recommendation |
|---|---|
| **Concurrency Control** | Enable with degree = **1** to prevent overlapping runs |
| **Waiting runs** | Set to a low value (e.g., 1–2) to avoid run pile-up |

> **Important:** Once Concurrency Control is turned on it **cannot be undone** without deleting and re-adding the trigger.

Platform limits for concurrency:
- With concurrency on: 1–100 concurrent runs (default 25 when enabled)
- Waiting runs limit: 10 + degree of parallelism

## Error Handling

Apply the standard **Try-Catch-Finally** Scope pattern (see general-standards.md).

Additional considerations for scheduled flows:
- Log failures to a Dataverse table or send an alert email — silent failures in batch jobs are critical risks.
- On catch: consider whether to **retry** the batch or **skip and log** (depends on idempotency guarantees).
- Use the **Terminate** action with Status = `Failed` in the Catch scope.

## Performance Considerations

- Minimum recurrence interval: **60 seconds**
- Maximum recurrence interval: **500 days**
- Flows without trigger activity for **90 days** may be suspended (owners notified at 60 days).
- Avoid processing large datasets in a single run — batch with pagination or child flows.

## References

- [Power Automate Limits and Config](https://learn.microsoft.com/en-us/power-automate/limits-and-config)
