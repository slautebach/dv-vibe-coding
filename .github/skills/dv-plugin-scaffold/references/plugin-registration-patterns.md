# Plugin Step Registration Patterns

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [Message + Stage + Mode Matrix](#message--stage--mode-matrix)
3. [Common Step Configurations](#common-step-configurations)
4. [Images](#images)
5. [Filtering Attributes](#filtering-attributes)
6. [Registration Summary Template](#registration-summary-template)

---

## Core Concepts

| Concept | Values | Notes |
|---|---|---|
| **Message** | Create, Update, Delete, Retrieve, Associate, Disassociate, custom action name | The Dataverse SDK message that triggers the plugin |
| **Stage** | 10 = Pre-Validation, 20 = Pre-Operation, 40 = Post-Operation | When in the pipeline the plugin fires |
| **Mode** | Synchronous, Asynchronous | Sync runs in the transaction; Async runs after commit |
| **Deployment** | Server only (standard) | IsolationMode = Sandbox (always use) |

### Stage Guidelines

| Stage | Use When |
|---|---|
| Pre-Validation (10) | Read-only checks before security; rarely needed |
| Pre-Operation (20) | Modify `Target` before save; validate and throw; pre-image required for delete |
| Post-Operation Sync (40) | React to the record ID just created; update related records within same transaction |
| Post-Operation Async (40) | Long-running work, external calls, notifications; runs outside transaction |

---

## Message + Stage + Mode Matrix

### Pre-Create (validate / enrich before insert)
```
Message:  Create
Entity:   mnp_yourEntity
Stage:    20 (Pre-Operation)
Mode:     Synchronous
Images:   None available (record not yet saved)
```
Use for: required-field validation, default-value population, duplicate detection.

### Post-Create Sync (react to new record in same transaction)
```
Message:  Create
Entity:   mnp_yourEntity
Stage:    40 (Post-Operation)
Mode:     Synchronous
Images:   Post-image available
```
Use for: create child records, update parent rollups, trigger same-transaction actions.

### Post-Create Async (fire-and-forget after create)
```
Message:  Create
Entity:   mnp_yourEntity
Stage:    40 (Post-Operation)
Mode:     Asynchronous
Images:   Post-image available
```
Use for: send emails, call external APIs, audit log entries.

### Pre-Update (validate / modify before update is saved)
```
Message:  Update
Entity:   mnp_yourEntity
Stage:    20 (Pre-Operation)
Mode:     Synchronous
Images:   Pre-image recommended (for before-value comparison)
Filtering: List only the attributes that should trigger the plugin
```
Use for: field-level validation, prevent invalid state transitions.

### Post-Update Sync (react to field changes in same transaction)
```
Message:  Update
Entity:   mnp_yourEntity
Stage:    40 (Post-Operation)
Mode:     Synchronous
Images:   Pre-image + Post-image available
Filtering: List only the attributes that should trigger the plugin
```
Use for: rollup calculations, cascade updates to related records.

### Post-Update Async (background processing after update)
```
Message:  Update
Entity:   mnp_yourEntity
Stage:    40 (Post-Operation)
Mode:     Asynchronous
Images:   Pre-image + Post-image available
Filtering: List only the attributes that should trigger the plugin
```
Use for: integrations, notifications, analytics.

### Pre-Delete (validate before delete / capture pre-image)
```
Message:  Delete
Entity:   mnp_yourEntity
Stage:    20 (Pre-Operation)
Mode:     Synchronous
Images:   Pre-image required (post-image not available for Delete)
```
Use for: cascading deletes, referential integrity checks.

### Post-Delete Async (cleanup after delete)
```
Message:  Delete
Entity:   mnp_yourEntity
Stage:    40 (Post-Operation)
Mode:     Asynchronous
Images:   Pre-image available
```
Use for: external system cleanup, audit.

---

## Images

Images capture a snapshot of entity attribute values at a specific moment.

| Image Type | Create | Update | Delete |
|---|---|---|---|
| Pre-Image | Not available | Available (values before update) | Available (values before delete) |
| Post-Image | Available (values after create) | Available (values after update) | Not available |

### Registering Images

- **Name**: Use `"PreImage"` and `"PostImage"` (MNP convention)
- **Attributes**: Specify only the attributes your plugin needs (performance best practice); leave blank for all
- **Pre-Operation stage**: Only Pre-Image is accessible
- **Post-Operation stage**: Both Pre-Image and Post-Image are accessible

### Accessing Images in Code

```csharp
Entity preImage = context.PreEntityImages.Contains("PreImage")
    ? context.PreEntityImages["PreImage"]
    : null;

Entity postImage = context.PostEntityImages.Contains("PostImage")
    ? context.PostEntityImages["PostImage"]
    : null;

// Safe attribute read helper
T GetValue<T>(Entity entity, string attribute, T defaultValue = default)
    => entity != null && entity.Contains(attribute)
       ? entity.GetAttributeValue<T>(attribute)
       : defaultValue;
```

---

## Filtering Attributes

For **Update** steps, always specify filtering attributes to prevent unnecessary plugin executions:

- In Plugin Registration Tool: set **Filtering Attributes** to a comma-separated list of logical attribute names
- Plugin only fires when at least one of the listed attributes is included in the update payload
- **Do not leave blank** unless the plugin genuinely must fire on every update

### Example Filtering Attributes
```
mnp_statuscode, mnp_applicationdate, mnp_assignedtoid
```

---

## Registration Summary Template

Generate this summary for every scaffold:

```
Assembly:   MNP.{Solution}.Plugins
Class:      {Action}Entity  (or {Action}Activity for workflow)
Step Name:  {Action} {Entity} {Message} {Stage}

Steps:
  1. Message: {Create|Update|Delete}
     Entity:  {logicalname}
     Stage:   {Pre-Operation|Post-Operation}
     Mode:    {Synchronous|Asynchronous}
     Filter:  {comma-separated attributes, or "(all)"}
     Pre-Image:  {name} - {attributes or "(all)"}
     Post-Image: {name} - {attributes or "(all)"}
```
