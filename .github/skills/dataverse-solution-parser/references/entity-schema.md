# Entity Schema Reference

## Entity.xml Structure

**Location**: `Entities/{EntityName}/Entity.xml`  
**Purpose**: Complete table definition including fields, relationships, keys, and metadata.

## Root Structure

```xml
<Entity>
  <Name LocalizedName="Application" OriginalName="">mnp_application</Name>
  <EntityInfo>
    <entity Name="mnp_application">
      <LocalizedNames>
        <LocalizedName description="Application" languagecode="1033" />
      </LocalizedNames>
      <Descriptions>
        <Description description="Represents an application..." languagecode="1033" />
      </Descriptions>
      <attributes>...</attributes>
      <EntitySetName>mnp_applications</EntitySetName>
      <IsBPFEntity>0</IsBPFEntity>
      <IsActivity>0</IsActivity>
      <PrimaryIdAttribute>mnp_applicationid</PrimaryIdAttribute>
      <PrimaryNameAttribute>mnp_name</PrimaryNameAttribute>
      ...
    </entity>
  </EntityInfo>
</Entity>
```

## Key Entity Properties

### Naming

- **Name** (attribute): LogicalName (lowercase, e.g., `mnp_application`)
- **LocalizedName**: Display name shown to users
- **EntitySetName**: OData collection name (plural, e.g., `mnp_applications`)
- **PrimaryIdAttribute**: Primary key field (e.g., `mnp_applicationid`)
- **PrimaryNameAttribute**: Display field (e.g., `mnp_name`)

### Entity Types

**IsBPFEntity**: Business Process Flow entity (0=No, 1=Yes)  
**IsActivity**: Activity entity like email/task (0=No, 1=Yes)  
**IsCustomEntity**: Custom vs. system entity (0=System, 1=Custom)  

### Ownership

**OwnershipType**:
- `0`: None
- `1`: UserOwned
- `2`: TeamOwned
- `3`: OrganizationOwned

## Attributes (Fields)

Located in `<attributes>` section:

```xml
<attributes>
  <attribute PhysicalName="mnp_Name">
    <Type>nvarchar</Type>
    <Name>mnp_name</Name>
    <LogicalName>mnp_name</LogicalName>
    <RequiredLevel>ApplicationRequired</RequiredLevel>
    <DisplayMask>ValidForAdvancedFind|ValidForForm|ValidForGrid</DisplayMask>
    <ImeMode>auto</ImeMode>
    <ValidForUpdateApi>1</ValidForUpdateApi>
    <ValidForCreateApi>1</ValidForCreateApi>
    <ValidForReadApi>1</ValidForReadApi>
    <CanModifySearchSettings>1</CanModifySearchSettings>
    <IsCustomField>1</IsCustomField>
    <IsAuditEnabled>1</IsAuditEnabled>
    <MaxLength>100</MaxLength>
    <Format>Text</Format>
    <LocalizedNames>
      <LocalizedName description="Name" languagecode="1033" />
    </LocalizedNames>
    <Descriptions>
      <Description description="The name of the application" languagecode="1033" />
    </Descriptions>
    <IntroducedVersion>1.0.0.0</IntroducedVersion>
  </attribute>
</attributes>
```

### Common Field Types

#### Text Fields

**nvarchar** (Single Line):
```xml
<Type>nvarchar</Type>
<MaxLength>100</MaxLength>
<Format>Text</Format>  <!-- Text, Email, Url, Phone -->
```

**memo** (Multi-line):
```xml
<Type>memo</Type>
<MaxLength>2000</MaxLength>
```

#### Numeric Fields

**int**:
```xml
<Type>int</Type>
<MinValue>0</MinValue>
<MaxValue>100</MaxValue>
<Format>None</Format>  <!-- None, Duration, TimeZone, Language -->
```

**decimal** / **money** / **double**:
```xml
<Type>money</Type>
<Precision>2</Precision>
<PrecisionSource>0</PrecisionSource>  <!-- 0=Attribute, 1=Currency, 2=Organization -->
```

#### Date/Time

```xml
<Type>datetime</Type>
<Format>DateAndTime</Format>  <!-- DateOnly, DateAndTime -->
<DateTimeBehavior>UserLocal</DateTimeBehavior>  <!-- UserLocal, DateOnly, TimeZoneIndependent -->
<ImeMode>auto</ImeMode>
```

#### Boolean (Two Options)

```xml
<Type>bit</Type>
<optionset>
  <TrueOption value="1">
    <labels>
      <label description="Yes" languagecode="1033" />
    </labels>
  </TrueOption>
  <FalseOption value="0">
    <labels>
      <label description="No" languagecode="1033" />
    </labels>
  </FalseOption>
</optionset>
```

#### Choice (Option Set / Picklist)

**Local option set**:
```xml
<Type>picklist</Type>
<optionset>
  <IsGlobal>0</IsGlobal>
  <OptionSetType>picklist</OptionSetType>
  <options>
    <option value="120310000" Color="#FF0000">
      <labels>
        <label description="Draft" languagecode="1033" />
      </labels>
      <Descriptions>
        <Description description="Application is in draft" languagecode="1033" />
      </Descriptions>
    </option>
    <option value="120310001">
      <labels>
        <label description="Submitted" languagecode="1033" />
      </labels>
    </option>
  </options>
</optionset>
```

**Global option set reference**:
```xml
<Type>picklist</Type>
<OptionSetName>mnp_applicationstatus</OptionSetName>
```

#### Lookup (Related Entity)

```xml
<Type>lookup</Type>
<LookupStyle>single</LookupStyle>
<LookupTypes>
  <LookupType id="2">contact</LookupType>
</LookupTypes>
<Targets>
  <Target>contact</Target>
</Targets>
<relationshipname>mnp_contact_mnp_application</relationshipname>
```

### Field Properties

#### Required Level

**RequiredLevel**:
- `None`: Optional
- `SystemRequired`: Always required (cannot be changed)
- `ApplicationRequired`: Required by customization (can be changed)
- `Recommended`: Not required but recommended

#### Validation

**ValidForCreateApi**: Can be set on create (0=No, 1=Yes)  
**ValidForUpdateApi**: Can be updated (0=No, 1=Yes)  
**ValidForReadApi**: Can be read (0=No, 1=Yes)  

#### Search and Display

**DisplayMask**: Where field appears:
- `ValidForAdvancedFind`: Advanced find queries
- `ValidForForm`: Forms
- `ValidForGrid`: Views/grids

**CanModifySearchSettings**: Can searchability be changed (0=No, 1=Yes)  
**IsAuditEnabled**: Field auditing enabled (0=No, 1=Yes)  

#### Security

**IsSecured**: Field-level security enabled (0=No, 1=Yes)  
**IsCustomField**: Custom vs. system field (0=System, 1=Custom)  

#### Versioning

**IntroducedVersion**: Version when field was added (e.g., `1.0.0.0`)  
Used for ALM and upgrade tracking.

## Relationships

### One-to-Many (1:N)

Parent entity has multiple related child records:

```xml
<EntityRelationship Name="mnp_application_activity_parties">
  <EntityRelationshipType>OneToMany</EntityRelationshipType>
  <IsCustomizable>1</IsCustomizable>
  <IntroducedVersion>1.0.0.0</IntroducedVersion>
  <IsHierarchical>0</IsHierarchical>
  <ReferencingEntityName>activityparty</ReferencingEntityName>
  <ReferencedEntityName>mnp_application</ReferencedEntityName>
  <CascadeAssign>NoCascade</CascadeAssign>
  <CascadeDelete>NoCascade</CascadeDelete>
  <CascadeReparent>NoCascade</CascadeReparent>
  <CascadeShare>NoCascade</CascadeShare>
  <CascadeUnshare>NoCascade</CascadeUnshare>
  <ReferencingAttributeName>partyid</ReferencingAttributeName>
  <RelationshipBehavior>0</RelationshipBehavior>
  <IsCustomRelationship>0</IsCustomRelationship>
  <AssociatedMenuConfiguration>
    <Behavior>DoNotDisplay</Behavior>
    <Group>Details</Group>
    <Order>10000</Order>
  </AssociatedMenuConfiguration>
</EntityRelationship>
```

**ReferencingEntityName**: Child entity (contains the lookup)  
**ReferencedEntityName**: Parent entity (referenced by lookup)  
**ReferencingAttributeName**: Lookup field in child entity

### Many-to-One (N:1)

Child entity references parent (inverse of 1:N):

```xml
<EntityRelationship Name="lk_mnp_application_createdby">
  <EntityRelationshipType>ManyToOne</EntityRelationshipType>
  <ReferencingEntityName>mnp_application</ReferencingEntityName>
  <ReferencedEntityName>systemuser</ReferencedEntityName>
  <ReferencingAttributeName>createdby</ReferencingAttributeName>
</EntityRelationship>
```

### Many-to-Many (N:N)

Intersect entity connects two entities:

```xml
<EntityRelationship Name="mnp_application_contact">
  <EntityRelationshipType>ManyToMany</EntityRelationshipType>
  <IsCustomizable>1</IsCustomizable>
  <Entity1LogicalName>mnp_application</Entity1LogicalName>
  <Entity1IntersectAttribute>mnp_applicationid</Entity1IntersectAttribute>
  <Entity2LogicalName>contact</Entity2LogicalName>
  <Entity2IntersectAttribute>contactid</Entity2IntersectAttribute>
  <IntersectEntityName>mnp_application_contact</IntersectEntityName>
  <Entity1NavigationPropertyName>mnp_application_contact</Entity1NavigationPropertyName>
  <Entity2NavigationPropertyName>mnp_application_contact</Entity2NavigationPropertyName>
</EntityRelationship>
```

### Cascade Behavior

Controls what happens to child records when parent changes:

- **NoCascade**: No action on children
- **Cascade**: Action cascades to children
- **Active**: Cascade only to active children
- **UserOwned**: Cascade only to user-owned children
- **RemoveLink**: Remove relationship but keep records

Applies to:
- **CascadeAssign**: Parent ownership changes
- **CascadeDelete**: Parent is deleted
- **CascadeReparent**: Parent hierarchy changes
- **CascadeShare**: Parent is shared
- **CascadeUnshare**: Parent sharing is removed

## Entity Keys

Alternate keys for records:

```xml
<keys>
  <key>
    <LogicalName>mnp_applicationnumber_key</LogicalName>
    <Name>Application Number Key</Name>
    <IsCustomizable>1</IsCustomizable>
    <IntroducedVersion>1.0.0.0</IntroducedVersion>
    <KeyAttributes>
      <KeyAttribute>
        <LogicalName>mnp_applicationnumber</LogicalName>
      </KeyAttribute>
    </KeyAttributes>
  </key>
</keys>
```

## Parsing Strategy

When analyzing Entity.xml:

1. **Extract entity metadata**: Names, type, ownership
2. **List all attributes** with types and required levels
3. **Identify custom fields**: `IsCustomField="1"`
4. **Parse option sets**: Local vs. global, values and labels
5. **Map relationships**: 1:N, N:1, N:N with cascade behavior
6. **Note keys**: Alternate keys for integration
7. **Track versioning**: IntroducedVersion for ALM
