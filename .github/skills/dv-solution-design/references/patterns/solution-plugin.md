# Pattern: Solution Plugin

Git Repo: https://dev.azure.com/MNPDigital/DC-Delivery/_git/DC-MNP-Base_Solution

## WHY?

- Provide guidance on creating solution plugins / workflow plugins that are solution/project specific
- Provide sample templates to accelerate plugin development

## How to Use

### Execution Flow

Solution plugins extend MNP.Base.Plugin base classes. The execution flow follows the standard Dataverse plugin pipeline.

### Generate Early Bound Classes

- Use **XrmToolBox - Early Bound Generator V2** (by D La B)
- The `DLab.Settings.xml` file stores regeneration settings -- **save it with the Visual Studio project/repo**
- Reminders:
  - Use the `MNP.Base.Plugin` namespace
  - Only include the required set of objects to optimize class size (whitelist tables, option sets, etc.)
  - Use NuGet packages for **crmsdk**

## Helper Functions

| Helper | Purpose |
|---|---|
| `PluginHelper` | Plugin context and execution helpers |
| `XrmHelper` | Dataverse/CRM interaction helpers |
| `XmlHelper` | XML parsing and manipulation helpers |

## Plugin Types

| Plugin Class | Usage |
|---|---|
| `AssignEntity` | Reassign entity ownership |
| `ValidateEntity` | Validate entity data before save |
| `ProcessEntity` | Execute business process logic on entity events |
| `SetStateEntity` | Change entity status/statecode programmatically |

## See Also

- [MNP.Base.Plugin component](../components/mnp-base-plugin.md) for shared plugin activities (syncPush, syncPull, etc.)
