# Pattern: Calling External Integrations (Logic App, Function App, REST)

## WHY?

Provides guidance on how a Model-Driven App should call an external service:
- HTTP-activated Power Automate or Azure Logic App
- HTTP-activated Azure Function App
- Generic REST API (abstracting into Logic App/Power Automate shields complexity from the MDA)

## Applications

- Integration with Financial Systems: post payments/journal entries, reconcile payments, fetch business partner info
- Integration with Payment Services: authorize credit card payments
- Loan/calculation services: amortization schedules, daily accrued interest

## Design Guidance

### Synchronous vs. Asynchronous

| Mode | UX Guidance |
|---|---|
| **Asynchronous** | Implement spinner + polling. Set an appropriate timeout to handle outages or data issues. |
| **Synchronous** | Implement spinner to show the process is in progress. |

### User Interaction Flow

1. User clicks a **Command Button** on the form/toolbar
2. Prompt: "Are you sure you want to...?"
3. On confirmation, display spinner (`Xrm.Utility.showProgressIndicator`)
4. Initiate the Action (via `Xrm.WebApi.online.execute`)
5. Poll/confirm the action completes, or timeout is exceeded
6. Prompt: "Successfully Completed" (or error message)
7. On confirmation, refresh the form

## Components Used

### UI Client API (JavaScript)

| API | Purpose |
|---|---|
| `Xrm.Navigation.openConfirmDialog` | Confirmation prompt before initiating |
| `Xrm.Utility.showProgressIndicator` | Show spinner |
| `Xrm.WebApi.online.execute` | Execute the Dataverse Action |
| `Xrm.Utility.closeProgressIndicator` | Dismiss spinner |
| `Xrm.Navigation.openAlertDialog` | Show success/error result |

### MNP.Base.Plugin Workflow Activities

| Activity | Purpose |
|---|---|
| `PrimaryIdActionInputParameterActivity` | Retrieves the GUID of a named EntityReference input parameter to pass to the HTTP integration |
| `RESTCallActivity` | Makes a REST call to initiate an HTTP-activated integration |

### Action Naming

`{Table} - {Integration} - Action`

- `{Table}`: the related table name, or `Global` if not entity-specific
- `{Integration}`: descriptive phrase for the purpose
- Example: `Project - RecalculateLoan - Action`

## Sample JavaScript Pattern (Polling)

```javascript
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function ExecuteIntegration(id) {
  var confirmStrings = { text: "This may take 2-10 min. Continue?", title: "Confirmation" };
  Xrm.Navigation.openConfirmDialog(confirmStrings, { height: 250, width: 450 }).then(
    async function (success) {
      if (success.confirmed) {
        Xrm.Utility.showProgressIndicator("Processing...");
        // Set action field to trigger the integration
        await Xrm.WebApi.updateRecord("mnp_entity", id, { "mnp_action": "MyIntegrationActivity" });
        await pollForCompletion(id);
      }
    }
  );
}

async function pollForCompletion(id) {
  var done = false;
  var i = 0;
  var timeout = 300; // ~10 min at 2s intervals
  while (!done) {
    await sleep(2000);
    var record = await Xrm.WebApi.retrieveRecord("mnp_entity", id, "?$select=mnp_action,mnp_action_result");
    if (!record.mnp_action || ++i > timeout) done = true;
  }
  Xrm.Utility.closeProgressIndicator();
  Xrm.Page.data.refresh(false);
}
```

## Azure Function App Setup

**Prerequisites:** Azure Subscription

**Reference:** https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview

## Azure Logic App Setup

**Prerequisites:** Azure Subscription + firewall rules for Logic App inbound/outbound IPs

**Reference:** https://learn.microsoft.com/en-us/azure/logic-apps/quickstart-create-first-logic-app-workflow

## RESTCallActivity Configuration (Environment Variable JSON)

```json
{
  "url": "",
  "verb": "POST",
  "contenttype": "application/json",
  "granttype": "client_credentials",
  "authority": "",
  "accesstokenurl": "",
  "clientid": "",
  "clientsecret": "",
  "tenantid": "",
  "scope": "",
  "clientname": "",
  "debug": ""
}
```
