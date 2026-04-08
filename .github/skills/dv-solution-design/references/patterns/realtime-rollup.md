# Pattern: Real-Time Rollup Calculations & Data Syncing

## WHY?

Native Dataverse Rollup fields have significant drawbacks:
- Limited number of rollup fields per table
- Rollup refresh is asynchronous -- not real-time

This pattern enables **real-time rollup calculations** and **real-time data sync** between tables (including complex multi-join scenarios via FetchXML).

## Applications

**Parent-Child scenarios:**
- Real-time count of child records (for counting, or to signal a business rule like "at least one child of a specific type")
- `Parent.TotalAmount` = sum of `Child.Amount` in real-time
- `Parent.ChildNames` = concatenated string of `Child.Name` values (e.g. "Name1, Name2, Name3")

**Multi-level (GrandParent/Parent/Child) scenarios:**
- Sum totals across a specific category, program, or ledger

## Implementation Guide

### Step 1: Create the Target Rollup Field as a Simple Field

- Add the field to the **Record Details** tab in a hidden section (for tracing/debugging)

### Step 2: Register syncPushEntity Plugin Steps

Use the Plugin Registration Tool to register on the child table:

| Message | Stage | CallingUser |
|---|---|---|
| Create | PostOperation | SYSTEM |
| Update | PostOperation | SYSTEM -- add PreImage named "Target" |
| Delete | PostOperation | SYSTEM -- add PreImage named "Target" |

### Step 3: Create a `sync.{LogicalEntityName}` Configuration Record

Create a record in the **Base.Configuration** table (`mnp_configuration`):

| Field | Value |
|---|---|
| Name | `Sync - {LogicalEntityName}` |
| Code | `sync.{LogicalEntityName}` (e.g. `sync.mnp_portalparticipant`) |
| Type | `Memo` |
| Memo | Sync Push XML configuration (see below) |

### Sync Push XML Configuration Example

```xml
<updates debug="on">
  <!-- Roll up count of child records to parent -->
  <update mode='push' onUpdate='statuscode'>
    <mapping>
      <target primaryid='@mnp_portalintakeid'
              primaryidname='mnp_portalintakeid'
              entity='mnp_portalintake'>
        <attribute target='mnp_incidentrole1_count' source='count' processNullSetTo='0'/>
      </target>
    </mapping>
    <fetch distinct='false' mapping='logical' aggregate='true'>
      <entity name='mnp_portalparticipant'>
        <attribute name='mnp_portalintakeid' alias='count' aggregate='count'/>
        <filter type='and'>
          <condition attribute='mnp_portalintakeid' operator='eq' value='@mnp_portalintakeid'/>
          <condition attribute='statuscode' operator='eq' value='1'/>
        </filter>
      </entity>
    </fetch>
  </update>
</updates>
```

### XML Tag Reference

| Tag/Attribute | Description |
|---|---|
| `debug="on"` | Enables extended tracing in Plugin Trace Logs |
| `onUpdate` | Comma-separated list of attribute logical names that trigger the rollup |
| `primaryid` | GUID of the target record -- use `@{logicalattributename}` to reference from triggering record |
| `processNullSetTo` | Value to set if FetchXML result is null |
| `updateIfChanged='yes'` | Only update target if the value actually changed (performance) |
| `@{logicalattributename}` | Substitutes the value from the triggering record at runtime |

## See Also

- [MNP.Base.Plugin - Sync Push](../components/mnp-base-plugin.md) for full plugin documentation
