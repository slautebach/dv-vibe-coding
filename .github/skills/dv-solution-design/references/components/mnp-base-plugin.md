# Component: MNP.Base.Plugin

Git Repo: https://dev.azure.com/MNPDigital/DC-Delivery/_git/DC-MNP-Base_Solution

## Table of Contents

- [Plugins (Entity Plugins)](#plugins-entity-plugins)
- [Workflow Activities](#workflow-activities)

---

## Plugins (Entity Plugins)

### Clone Document Location (`CloneDocumentLocationEntity`)

Creates a `SharePointDocumentLocation` record cloned from a source configuration. Example: when `mnp_claim` is created, clone the `mnp_project` SharePointDocumentLocation.

Also supports cloning from parent to children when a new document location is created.

**Configuration XML (`mnp_configuration` memo):**
```xml
<config>
  <subscription target="mnp_recommendation">
    <documentlocation source="mnp_project" primaryid="mnp_projectid" name="" action="subscribe"/>
  </subscription>
</config>
```

**Plugin Steps needed:**
- Create step on the Entity (to clone from parent)
- Create step on SharePointDocumentLocation (to clone to child records)

---

### Create Document Location (`CreateDocumentLocationEntity`)

Creates default SharePoint folders when a DocumentLocation is created.

**Configuration:** `mnp_configuration.mnp_code = CreateMOSSFolder.{LogicalEntityName}`
```xml
<MOSS><Folders>
  <Folder Name="Agreement"/>
  <Folder Name="Assessments"/>
  <Folder Name="Claims"/>
</Folders></MOSS>
```

---

### Set Entity Name (`SetEntityName`)

Assigns the entity name (`mnp_name`) based on a format mask.

**Configuration:** `mnp_configuration.mnp_code = {LogicalEntityName}.{LogicalAttributeName}`
```xml
<Entity>
  <Target ID="mnp_name" Format="{0} - Agreement Batch [{1}]">
    <Field ID="mnp_batchno" Type="String"/>
    <Field ID="statuscode" Type="Status"/>
  </Target>
</Entity>
```

---

### Sync Pull (`baseSyncPullEntity`)

Pulls information onto a target record when a change occurs. Used to default values on create or update.

**Configuration:** `mnp_configuration.mnp_code = sync.{LogicalEntityName}`

**Triggers on field changes** defined in `onUpdate`, then executes a FetchXML and maps results to target attributes.

**Plugin Steps:** Create/Update/Delete on the Entity (PostOperation with PostImage; Delete uses PreOperation + PreImage)

---

### Sync Push (`baseSyncPushEntity`)

Pushes aggregated data from child records to a parent (target) record. Used for **real-time rollup calculations**.

**Configuration:** `mnp_configuration.mnp_code = sync.{LogicalEntityName}`

```xml
<updates debug="on">
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

**Plugin Steps:** Create/Update/Delete on the child table (PostOperation + PreImage on Update/Delete)

**XML Attributes:**
| Attribute | Description |
|---|---|
| `debug="on"` | Extended tracing in Plugin Trace Logs |
| `onUpdate` | Comma-separated attribute logical names that trigger the rollup |
| `primaryid` | Target record GUID -- use `@{attr}` to reference from triggering record |
| `processNullSetTo` | Value to set if result is null |
| `updateIfChanged='yes'` | Only update if value changed (performance) |

---

## Workflow Activities

### Add Working Days Activity
Adds N working days to a DateTime, respecting a Holiday Calendar (8-hour days assumed).
- **Input:** Date Time, Working Days to Add, Calendar
- **Output:** New Date Time

### Attribute Changed Activity
Checks if specified attributes changed in a Real-Time workflow.
- **Input:** Attribute Names (comma-separated), Mode (ALL/ANY)
- **Output:** Has Changed (bool)

### Attribute Update Activity
Executes FetchXML and updates an attribute with a result value. Supports aggregate functions.
- **Input:** Fetch Xml, Fetch Attribute, Update Attribute

### Bulk Attribute Update Activity
Same as Attribute Update but updates multiple attributes using `|` separator.
- **Input:** Fetch XML, Fetch Attribute to Update (pipe-separated), Value Attribute (pipe-separated)

### Create Related Entities Activity
Creates related entity records based on a FetchXML filter and a data map.
- **Input:** Related Entity, Related Entity Fetch Filter, Target Entity, Target Entity Data Map

### Date Activity
Manipulates dates: add days/months/years, calculate differences, extract day/month/year/week.
- **Output:** New Date, Total Days, Day of Week, Month, Year, Week of Year, etc.

### Delete Activity
Deletes the primary or a related entity.

### Find First Activity
Returns the first FetchXML result's specified attribute as a string.
- **Input:** Fetch Xml, Attribute

### Get Attribute Changed Activity
Returns a string list of changed attributes from the pipeline.
- **Output:** Changed Attributes (e.g. `[mnp_name],[mnp_status]`)

### Get Row Count Activity
Returns count of rows from a FetchXML.
- **Output:** Row Count

### Get Team Role Activity
Returns teams and roles for a specified user (use `"ExecutionUser"` for current user).
- **Output:** TeamsAndRoles (teams in `[]`, roles in `{}`)

### Get Value Activity
Returns a typed value from FetchXML.
- **Output:** String, Money, Decimal, DateTime, Float

### Malware Scan Activity
Scans Note Attachments for malware via a third-party service (configurable via Environment Variable JSON).
- **Output:** No Threats Found (bool)

### Math Activity
Evaluates mathematical expressions. Uses `@a` through `@z` as variables.
- **Output:** String, Money, Integer (truncated/rounded), Float

### Primary Id Action Input Parameter Activity
Returns the GUID of a named EntityReference input parameter in an Action.
- **Input:** Input Parameter Name
- **Output:** PrimaryId (string)

### REST Call Activity
Obtains an access token (optional) and makes a REST call. Used for external integrations.

**Environment Variable JSON:**
```json
{
  "url": "", "verb": "POST", "contenttype": "application/json",
  "granttype": "client_credentials",
  "authority": "", "accesstokenurl": "",
  "clientid": "", "clientsecret": "", "tenantid": "", "scope": ""
}
```
- **Output:** Response Body (string), Response Status Code (string)

### Set BPF Activity
Sets and moves the Business Process Flow stage for an entity.
- **Input:** BPF Table Logical Name, BPF Table Regarding Lookup Name, Entity Logical Name, Entity ID, No of Stages to Move, Stage Name, Reactivate BPF (Force)
- **Output:** Error Message (always check; plugin does not throw exceptions)

### Share Activity
Shares or unshares the primary entity with teams/users based on a FetchXML condition and configuration record.

### String Activity
Manipulates strings: capitalize, pad, replace, substring, regex, token compare, trim, upper/lower case.

### Updated Value Activity
Returns updated attribute values from the transaction pipeline.
- **Output:** String, Currency, DateTime, Boolean, Number, Is Updated (bool)

### Validation Activity
Executes a set of validations defined in an XML configuration record. Returns Valid (bool), ErrorMessage, SuccessMessage.

**Sample configuration XML:**
```xml
<validations separator=';' debug='on'>
  <fetchXML alias='test'>
    <fetch><entity name='contact'><all-attributes/>
      <filter><condition attribute='firstname' operator='eq' value='@firstname'/></filter>
    </entity></fetch>
  </fetchXML>
  <validation>
    <expression>"@test.firstname" == "Contact" || @preferredcontactmethodcode == 2</expression>
    <errorMessage>First name must be Contact</errorMessage>
    <successMessage>Validation passed</successMessage>
  </validation>
</validations>
```

### With Range Activity
Returns true if a value is within an absolute or relative range.
- **Input:** Value, Low Range, Low Range Type, High Range, High Range Type
- **Output:** Within Range (bool)
