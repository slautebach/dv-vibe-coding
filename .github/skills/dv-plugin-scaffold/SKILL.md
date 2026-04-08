---
name: dv-plugin-scaffold
description: Scaffold C# Dataverse plugin classes and workflow activities following MNP naming conventions and the MNP.Base.Plugin pattern. Generates plugin class stubs, IPlugin/CodeActivity wiring, pre/post image patterns, FakeXrmEasy unit test skeleton, and plugin step registration summary. Use when asked to "create a plugin", "scaffold a plugin", "create a workflow activity", "add a plugin step", or "set up a plugin project". Do NOT use for documenting existing plugin registrations (use dv-doc-plugin-steps skill).
---

# Dv Plugin Scaffold

## Overview

Scaffold MNP-standard Dataverse plugins and workflow activities: class stubs, base-class wiring, registration metadata, and FakeXrmEasy test skeletons.

## Reference Files

Read these before generating code:

- **`references/plugin-standards.md`** - Naming conventions, MNP.Base.Plugin pattern, LocalPluginContext API, plugin/workflow class structure, built-in catalogue
- **`references/plugin-registration-patterns.md`** - Step configurations for pre/post-create/update, images, filtering attributes, registration summary template
- **`references/action-standards.md`** - When to use Actions vs plugins vs workflow activities; naming; invocation patterns

## Assets

Copy and adapt from `assets/`:

| File | Purpose |
|---|---|
| `PluginBase.cs` | Drop-in PluginBase abstract class if the shared MNP.Base.Plugin assembly is unavailable |
| `WorkflowActivityBase.cs` | Drop-in WorkflowActivityBase for workflow activities |
| `PluginTest.cs` | FakeXrmEasy 3.x test skeleton with context helpers and example test patterns |

## Workflow

### 1. Gather Requirements

Ask the user for (or infer from context):
- **Type**: Plugin or Workflow Activity
- **Solution name** - becomes `MNP.{Solution}.Plugins` assembly
- **Entity logical name** (plugin) or activity purpose (workflow)
- **Message** - Create / Update / Delete / custom action
- **Stage** - Pre-Operation (20) or Post-Operation (40)
- **Mode** - Synchronous or Asynchronous
- **Logic brief** - what the plugin/activity should do

### 2. Generate Code

For a **plugin**, produce:
1. Class named `{Action}Entity` extending `PluginBase`
2. Constructor accepting `(string unsecureConfig, string secureConfig)`
3. `ExecuteDataversePlugin` implementation with:
   - Guard: null-check localContext and validate message/entity name
   - Pre/post image access where stage requires it
   - Core logic with `localContext.Trace(...)` at key steps
   - `InvalidPluginExecutionException` for user-visible errors

For a **workflow activity**, produce:
1. Class named `{Action}Activity` extending `WorkflowActivityBase`
2. Typed `InArgument<T>` / `OutArgument<T>` properties with `[Input]` / `[Output]` / `[RequiredArgument]` attributes
3. `ExecuteCrmWorkFlowActivity` implementation

### 3. Generate Registration Summary

Always output a registration block after the code:

```
Assembly:  MNP.{Solution}.Plugins
Class:     {ClassName}
Steps:
  Message:  Create|Update|Delete
  Entity:   logicalname
  Stage:    Pre-Operation|Post-Operation
  Mode:     Synchronous|Asynchronous
  Filter:   attributes or (all)
  Pre-Image:  PreImage - attributes or (all)
  Post-Image: PostImage - attributes or (all)
```

### 4. Generate Test Skeleton

Offer to generate a FakeXrmEasy test class (based on `assets/PluginTest.cs`):
- Happy-path test with valid Target
- Negative test for the main validation guard
- Pre-image test if the step uses Pre-Operation stage or pre-image

## Key Patterns

### Validation guard (pre-create/pre-update)
```csharp
if (!context.InputParameters.Contains("Target") || !(context.InputParameters["Target"] is Entity))
    return;

var target = (Entity)context.InputParameters["Target"];

if (!target.Contains("mnp_requiredfield") || target["mnp_requiredfield"] == null)
    throw new InvalidPluginExecutionException("Required Field is mandatory.");
```

### Coalesce Target + Pre-image (post-update)
```csharp
var preImage = localContext.GetPreImage("PreImage");
T GetVal<T>(string attr) =>
    target.Contains(attr)  ? target.GetAttributeValue<T>(attr) :
    preImage?.Contains(attr) == true ? preImage.GetAttributeValue<T>(attr) :
    default;
```

### Workflow activity parameter declaration
```csharp
[RequiredArgument]
[Input("Label shown in designer")]
[AttributeTarget("logicalentityname", "logicalattributename")]
public InArgument<string> MyInput { get; set; }

[Output("Result Label")]
public OutArgument<bool> IsValid { get; set; }
```

## NuGet Dependencies

| Package | Version | Purpose |
|---|---|---|
| `Microsoft.CrmSdk.CoreAssemblies` | latest stable | IPlugin, IOrganizationService, Entity |
| `Microsoft.CrmSdk.Workflow` | latest stable | CodeActivity, IWorkflowContext |
| `FakeXrmEasy.Core` | 3.x | Unit test fake context |
| `FakeXrmEasy.Plugins` | 3.x | ExecutePluginWith<T> extension |

Target: .NET Framework 4.6.2. Sign the assembly before registering.
