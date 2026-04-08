# MNP Plugin Standards

## Table of Contents
1. [Naming Conventions](#naming-conventions)
2. [MNP.Base.Plugin Pattern](#mnpbaseplugin-pattern)
3. [Plugin Class Structure](#plugin-class-structure)
4. [Workflow Activity Structure](#workflow-activity-structure)
5. [Built-in Plugin Catalogue](#built-in-plugin-catalogue)
6. [Built-in Workflow Activity Catalogue](#built-in-workflow-activity-catalogue)

---

## Naming Conventions

### Assembly
- Pattern: `MNP.{Solution}.Plugins`
- Examples: `MNP.ROCS.Plugins`, `MNP.QUARTS.Plugins`, `MNP.Grants.Plugins`, `MNP.LicencingPermits.Plugins`

### Plugin Class
- Pattern: `{Action}Entity` — where `{Action}` represents the purpose/action
- Examples: `ProcessApplicationEntity`, `ValidateSubmissionEntity`, `CalculateTaxInvoiceEntity`
- Convention: verb + noun describing the domain entity being acted on

### Workflow Activity Class
- Pattern: `{Action}Activity`
- Examples: `GetFiscalYearActivity`, `CalculateBenefitActivity`, `FindFirstRowActivity`

### Namespace
- Convention: `MNP.{Solution}.Plugins`

---

## MNP.Base.Plugin Pattern

MNP.Base.Plugin is a shared base library that provides:
- A `PluginBase` abstract class implementing `IPlugin`
- A `LocalPluginContext` inner class pre-wired with all Dataverse services
- A `WorkflowActivityBase` abstract class implementing `CodeActivity`
- Consistent error handling and tracing patterns

Source: [DC-MNP-Base_Solution Git Repo](https://dev.azure.com/MNPDigital/DC-Delivery/_git/DC-MNP-Base_Solution)

### LocalPluginContext Services
When your plugin executes, `LocalPluginContext` provides:
- `IPluginExecutionContext` — execution context (entity, message, stage, images)
- `IOrganizationService` — org service scoped to triggering user
- `IOrganizationService` (admin) — org service scoped to system account
- `ITracingService` — write to plugin trace log
- Pre/post entity images via `PreEntityImages` and `PostEntityImages`

---

## Plugin Class Structure

```csharp
namespace MNP.{Solution}.Plugins
{
    // Register on: {Entity} - {Message} - {Stage} ({Sync/Async})
    // Pre-images:  "PreImage" - all / [attribute list]
    // Post-images: "PostImage" - all / [attribute list]
    public class {Action}Entity : PluginBase
    {
        public {Action}Entity(string unsecureConfig, string secureConfig)
            : base(typeof({Action}Entity), unsecureConfig, secureConfig)
        {
        }

        protected override void ExecuteDataversePlugin(ILocalPluginContext localContext)
        {
            if (localContext == null) throw new ArgumentNullException(nameof(localContext));

            var context = localContext.PluginExecutionContext;
            var service  = localContext.InitiatingUserOrganizationService;
            var trace    = localContext.TracingService;

            // Validate expected message / entity
            if (context.MessageName != "Create" || context.PrimaryEntityName != "mnp_entity")
                return;

            var target = (Entity)context.InputParameters["Target"];

            // --- your logic here ---
        }
    }
}
```

### Pre/Post Image Access

```csharp
// Pre-image (registered as "PreImage")
Entity preImage = null;
if (context.PreEntityImages.Contains("PreImage"))
    preImage = context.PreEntityImages["PreImage"];

// Post-image (registered as "PostImage")
Entity postImage = null;
if (context.PostEntityImages.Contains("PostImage"))
    postImage = context.PostEntityImages["PostImage"];
```

### Input/Output Parameters

```csharp
// Read input parameter
var target  = (Entity)context.InputParameters["Target"];
var entityRef = (EntityReference)context.InputParameters["Target"];

// Write output parameter (for custom actions)
context.OutputParameters["result"] = "value";
```

### Throwing User-Visible Errors

```csharp
throw new InvalidPluginExecutionException("Validation failed: field X is required.");
```

---

## Workflow Activity Structure

```csharp
namespace MNP.{Solution}.Plugins
{
    public class {Action}Activity : WorkflowActivityBase
    {
        // Input parameters
        [RequiredArgument]
        [Input("Input Label")]
        public InArgument<string> InputField { get; set; }

        // Output parameters
        [Output("Output Label")]
        public OutArgument<string> OutputField { get; set; }

        protected override void ExecuteCrmWorkFlowActivity(
            CodeActivityContext context,
            ILocalWorkflowContext localContext)
        {
            if (context == null)     throw new ArgumentNullException(nameof(context));
            if (localContext == null) throw new ArgumentNullException(nameof(localContext));

            var service = localContext.OrganizationService;
            var trace   = localContext.TracingService;
            var wfCtx   = localContext.WorkflowContext;

            string input = InputField.Get(context);

            // --- your logic here ---

            OutputField.Set(context, "result");
        }
    }
}
```

### Common Parameter Types

| C# Type | Workflow Designer Type |
|---|---|
| `InArgument<string>` | Text |
| `InArgument<bool>` | Yes/No |
| `InArgument<int>` | Whole Number |
| `InArgument<decimal>` | Decimal Number |
| `InArgument<DateTime>` | Date and Time |
| `InArgument<EntityReference>` | Record Reference |
| `InArgument<Money>` | Currency |
| `OutArgument<string>` | Text output |

---

## Built-in Plugin Catalogue

| Class | Trigger | Purpose |
|---|---|---|
| `CloneDocumentLocationEntity` | Create on entity / SharePointDocumentLocation | Clone SharePoint document location from parent |
| `CreateDocumentLocationEntity` | Create on SharePointDocumentLocation | Create default folders using `mnp_configuration` |
| `SetEntityNameEntity` | Create / Update | Assign formatted entity name via mask in `mnp_configuration` |
| `baseSyncPullEntity` | Create / Update / Delete | Pull field values from related records using FetchXML config |
| `baseSyncPushEntity` | Create / Update / Delete | Push/aggregate values to parent records using FetchXML config |

---

## Built-in Workflow Activity Catalogue

| Activity | Purpose |
|---|---|
| `AddWorkingDaysActivity` | Add N working days to a DateTime, respecting holiday calendars |
| `AttributeChangedActivity` | Detect if specified attributes changed (ALL/ANY mode) |
| `AttributeUpdateActivity` | Execute FetchXML and update attribute with first result |
| `BulkAttributeUpdateActivity` | Execute FetchXML and bulk-update multiple attributes |
| `CascadeUpdateActivity` | Sync statecode/statuscode to related records |
| `CreateRelatedEntitiesActivity` | Create related entity records from FetchXML and a data map |
| `DateActivity` | Date arithmetic: add days/months/years, return components |
| `DeleteActivity` | Delete primary or related entity record |
| `FindFirstActivity` | Return first FetchXML result attribute as string |
| `FindFirstUserActivity` | Return first systemuser result as EntityReference |
| `GetAttributeChangedActivity` | Return list of changed attribute logical names |
| `GetRowCountActivity` | Return count of FetchXML results |
| `GetTeamRoleActivity` | Return teams and roles for a specified user |
| `GetValueActivity` | Return typed values (string/money/decimal/datetime/float) from FetchXML |
| `GetYearActivity` | Return fiscal or calendar year from a DateTime |
| `MalwareScanActivity` | Scan note attachments for malware via third-party REST service |
| `MathActivity` | Evaluate mathematical expressions with variable substitution |
| `PreviousValueActivity` | Return pre-update value of an attribute |
| `PrimaryIdActivity` | Return primary GUID of triggering or related record |
| `RESTCallActivity` | Obtain OAuth token and execute REST call; return body/status |
| `SetBPFActivity` | Set or advance Business Process Flow stage |
| `ShareActivity` | Share/unshare primary record based on FetchXML config |
| `StartWorkflowActivity` | Start workflow(s) on FetchXML result set |
| `StringActivity` | Pad, replace, substring, regex, capitalize strings |
| `UpdatedValueActivity` | Return updated value from transaction pipeline |
| `ValidationActivity` | Process XML-configured validation rules; return pass/fail + messages |
| `WithRangeActivity` | Determine if a decimal value is within an absolute or percent range |
