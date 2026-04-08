# Component: North52 Business Process Activities (BPA)

**References:**
- North52 Functions: https://support.north52.com/knowledgebase/functions/
- [Mastering North52 Formulas Guide](../../wiki/Welcome/Platform-Delivery-Playbook/Solution-Design/Component-%2D-North-52/Mastering-North52-Formulas.md)

## WHY?

North52 fills the gap between native Business Rules (too simple) and C# plugins (too heavyweight). Use it for:
- Complex synchronous calculations and validations that require server-side enforcement
- Logic that changes frequently and must be updated without a full compile/deploy cycle
- Scenarios where a Business Analyst or consultant needs to maintain the rules

## Suite Modules

| Module | Purpose |
|---|---|
| **Formula Manager** | Core engine -- defines, stores, and executes business logic in an Excel-like language |
| **Decision Tables** | Tabular editor for complex multi-condition rules; preferred over nested If() statements |
| **Process Genie** | Custom workflow activity that invokes a North52 Formula from a Classic Workflow/Action |
| **Scheduler** | Executes formulas on a schedule against a FetchXML-targeted set of records |
| **WebFusion** | Connects formulas to external REST services (validation, document generation, SMS) |
| **xCache** | In-memory cache for configuration values (API keys, tax rates, reusable FetchXML) |
| **Smart Flow** | Orchestrates multi-step processes with variables within a single formula |

## Formula Record Fields

| Field | Description |
|---|---|
| **Name** | Descriptive identifier: `{Entity} - {Formula Type} - {Description}` (e.g. `App Section - Validate - CRC CV Funding`) |
| **Formula Type** | `Save - To Current Record`, `Save - Perform Action`, `ClientSide - Perform Action`, `Validation`, `AutoNumber` |
| **Source Entity** | Table that triggers the formula |
| **Source Property** | Specific fields whose change triggers the formula (critical performance optimization -- always set for Update events) |
| **Target Entity / Property** | Destination table/field for the result (used with `Save - To Current Record`) |
| **Mode** | `Client Side`, `Server Side`, or `Client & Server Side` |
| **Pipeline Stage** | `Pre-Validation`, `Pre-Operation`, `Post-Operation (Sync)`, `Post-Operation (Async)` |
| **Category / Subcategory** | Group related formulas (e.g. all App Section validation formulas tagged together) |
| **Deployment Solution** | Target Dataverse solution for the formula's XML web resource (enables ALM) |

## Execution Modes

| Mode | Use Case |
|---|---|
| **Client Side** | UI enhancements: show/hide fields, form notifications. Fast, no server round-trip. Never use alone for security-critical rules. |
| **Server Side** | Enforcement regardless of how data is modified (UI, API, import). Must use for data integrity. |
| **Client & Server Side** | Best practice for validation: instant feedback client-side + guaranteed enforcement server-side. |

## Best Practices

### Design for Maintainability
- Name formulas: `{Entity} - {Formula Type} - {Description}`
- Use **Category/Subcategory** to group related formulas
- Store config values (API endpoints, reusable FetchXML) in **xCache** -- never hardcode
- Prefer **Decision Tables** over nested `If()` for complex conditional logic
- Always use option set **integer values** (not text) in conditions to support multi-language

### Performance Optimization
- **Always set Source Property** on Update event formulas -- prevents running on every save
- Minimize redundant `Find*` calls -- use `SetVar()` to store values used multiple times
- Choose the right Mode -- avoid `Client & Server Side` unless both are truly needed

### Debugging
- Set **Tracing Level = Information** in the North52 Configuration record during development
- **Client-side errors:** check browser Developer Tools (F12) Console
- **Server-side errors:** set Tracing Level to `Information(Show Exception Details)`; enable Plugin Trace Log in System Settings

### ALM Deployment
1. Set **Deployment Solution** on the Formula record to the current release solution
2. Save -- North52 automatically creates/updates an XML web resource in that solution
3. Export and deploy the solution through the standard Dataverse ALM pipeline
