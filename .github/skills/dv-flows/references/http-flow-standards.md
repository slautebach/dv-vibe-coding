# HTTP Flow Standards

Source: MNP Platform Delivery Playbook

## Purpose

- Provide a secure method to initiate an instant/HTTP-triggered flow.
- HTTP flows have inherent security risks, especially when called from untrusted networks.

## Naming

Pattern: `HTTP - {Action} - MNP`

| Part | Description | Example |
|---|---|---|
| `HTTP` | Fixed prefix — indicates instant flow via HTTP trigger (GET or POST) | — |
| `{Action}` | What the flow does | `Process Application`, `Submit to Financial` |

Full example: `HTTP - Process Application - MNP`

## Security Requirements

HTTP-triggered flows **must** implement additional authentication. Never rely solely on the trigger URL being secret.

### Authentication Options (Power Automate HTTP trigger)

| Method | Description | When to Use |
|---|---|---|
| **Azure Active Directory (OAuth)** | Caller must present a valid AAD bearer token | Preferred for M365 / Azure callers |
| **API Key / SAS** | Shared secret passed in header | Simple internal integrations |
| **IP Restriction** | Restrict calls to known IP ranges via Azure API Management | Network-level trust boundary |
| **Azure API Management** | Route HTTP trigger through APIM for policy enforcement, rate limiting, auth | Enterprise / external-facing flows |

### Recommended Approach for MNP Projects

1. **Enable AAD authentication** on the HTTP trigger where possible.
2. If calling from Power Pages / portals, use a **service principal with least-privilege permissions**.
3. Validate the caller identity inside the flow (check `claims` or a shared secret header).
4. Add a **condition** at the start: if auth fails → terminate with `Failed` immediately.

### Checking Trusted Source Inside the Flow

```
Condition: Is caller trusted?
  If no → Terminate (Failed, "Unauthorized caller")
  If yes → [Continue flow logic]
```

## Error Handling

Apply the standard **Try-Catch-Finally** Scope pattern (see general-standards.md).

For HTTP flows, always return a structured response:
- **200 OK** with a JSON body on success
- **400 / 500** response using the **Response** action on failure inside the Catch scope

## Performance Considerations

- HTTP flows are **synchronous** — the caller waits for a response (default timeout: 2 minutes for synchronous, 30 days async).
- For long-running operations, return a **202 Accepted** immediately and process asynchronously.
- Keep the trigger payload small; validate and sanitize all inputs.

## References

- [Power Automate HTTP trigger authentication](https://learn.microsoft.com/en-us/azure/connectors/connectors-native-reqres)
- [Logic Apps HTTP endpoint guide](https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-http-endpoint)
