# Dataverse Flow Standards

Source: MNP Platform Delivery Playbook

## Purpose

- Dataverse has per-user and per-flow API request limits — flows must be designed to stay within them.
- Dataverse-triggered flows are **always asynchronous** — design accordingly (no synchronous response requirement).

## Naming

Pattern: `{Table} - {Action} - MNP`

| Part | Description | Example |
|---|---|---|
| `{Table}` | The Dataverse table triggering the flow | `Application`, `Contact`, `Invoice` |
| `{Action}` | What the flow does | `Process Submission`, `Submit to Financial` |

Full example: `Application - Process Submission - MNP`

## Get Record / List Records Standards

### Always Filter — Never Retrieve All Records

- Use **FetchXML** (preferred for Dataverse) or **OData** filter expressions on List Rows actions.
- Never retrieve all records and filter inside the flow — this wastes API quota and can hit throttling.
- FetchXML example (preferred in Dataverse context):

```xml
<fetch top="50">
  <entity name="mnp_application">
    <attribute name="mnp_applicationid"/>
    <attribute name="mnp_status"/>
    <filter>
      <condition attribute="mnp_status" operator="eq" value="1"/>
    </filter>
  </entity>
</fetch>
```

- OData filter example (use for SharePoint or non-Dataverse connectors):
  `statuscode eq 1 and statecode eq 0`

### Select Only Required Columns

- In **List Rows** and **Get a Row**, always specify the **Select Columns** parameter.
- Do not leave it blank (returns all columns, wastes bandwidth, increases token usage).

### Use Row Count

- Set **Row Count** on List Rows actions to cap results (e.g., top 1 for uniqueness validation).
- Prevents processing unexpected duplicates and reduces over-consumption of API quota.

## Apply to Each — Avoid on Large Datasets

- **Apply to Each** is synchronous by default — consider enabling parallelism (max 50 concurrent).
- For large datasets (thousands of records), use:
  - **Do Until** loops with pagination tokens
  - Child flows for batching
  - Dataverse batch operations or custom APIs instead of row-by-row processing
- Apply to Each limit: **100,000 items** (Low performance profile: **5,000**).

## Trigger Considerations

- Use **When a row is added, modified or deleted** trigger for Dataverse-triggered flows.
- Set **Trigger conditions** to filter at the trigger level (avoids unnecessary flow runs).
- Example trigger condition (only run when status changes to Submitted):
  `@equals(triggerOutputs()?['body/statuscode'], 3)`

## Connection Reference

- Always use the **Microsoft Dataverse** connection reference (not a hardcoded connection).
- Verify the correct shared connection reference exists in the solution before creating a new one.

## Dataverse API Limits Reference

| License | Daily Requests |
|---|---|
| Dynamics 365 Enterprise | 40,000 |
| Power Automate per flow | 250,000 |
| Power Apps per app / M365 | 6,000 |

- Flows running under a **service principal** (application user) get Unlimited Extended profile.
- Consistently throttled flows are turned off after **14 days** — assign Process license to dedicate capacity.

Reference: [Power Platform Request Limits](https://learn.microsoft.com/en-us/power-platform/admin/api-request-limits-allocations)
