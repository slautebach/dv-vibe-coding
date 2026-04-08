# Connection References in Power Automate

Source: MNP Platform Delivery Playbook + Microsoft Docs

## What is a Connection Reference?

A **connection reference** is a solution component that contains a reference to a connection for a specific connector. Solution-aware flows bind to a connection reference instead of directly to a connection.

- **Connection**: The stored authentication credential (e.g., OAuth token for SharePoint).
- **Connection reference**: A named pointer to that connection, stored inside the solution.

During solution import, the target environment provides its own connection for each connection reference — this is how one solution zip file works across DEV, SIT, UAT, and PROD without modification.

## Why Always Use Connection References

| Without Connection References | With Connection References |
|---|---|
| Connections are hardcoded to the maker's account | Connections are environment-agnostic |
| Flows break on import to another environment | Flows turn on automatically after import |
| Hard to audit which connections flows use | Easy to audit and swap connections centrally |
| Each environment needs manual flow repair | One-time setup per environment |

## MNP Rule: Use Existing, Don't Create New

1. **Before using any connector** in a flow, check the solution for an existing connection reference for that connector.
2. If one exists, reuse it — do **not** create a duplicate.
3. Only create a new connection reference if none exists for that connector type.

Power Automate automatically tries to reuse existing connection references from the current solution or other solutions when you add an action.

## How to Add a Connection Reference

1. Open the solution in Power Apps / Power Automate.
2. Add the action to the flow — Power Automate will prompt to select a connection reference.
3. Select an existing connection reference or create one.
4. If creating: use a clear display name, e.g., `Dataverse - DC Starter Kit`, `SharePoint - Document Library`.

## Connection Reference Naming Convention

Format: `{Connector} - {Context}`

Examples:
- `Dataverse - DC Starter Kit`
- `SharePoint - Project Documents`
- `Office 365 Outlook - Notifications`

## Updating Flows to Use Connection References

If a flow was built outside a solution (uses direct connections):
1. Move the flow into a solution.
2. The **Flow Checker** will warn: _"Use connection references"_.
3. Select **Remove connections so connection references can be added**.
4. Re-connect using connection references.

Alternatively, export as unmanaged solution and re-import — connections are stripped and replaced with connection references automatically.

## References

- [Use a connection reference in a solution - Microsoft Learn](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-connection-reference)
