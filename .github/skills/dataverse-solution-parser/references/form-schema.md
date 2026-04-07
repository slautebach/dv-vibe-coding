# Form Schema Reference

## FormXml Structure

**Location**: `Entities/{EntityName}/FormXml/{formtype}/{guid}.xml`  
**Purpose**: Defines form layout, controls, events, and client-side resources.

## Form Types

Forms stored in subdirectories by type:

- **main**: Main forms (detailed view)
- **quick**: Quick Create forms (minimal fields)
- **quickView**: Quick View forms (read-only embedded views)
- **Preview**: Preview forms
- **AppointmentBook**: Appointment book forms (for activities)
- **card**: Card forms (mobile)

## Root Structure

```xml
<forms type="main">
  <systemform>
    <formid>{guid}</formid>
    <FormPresentation>0</FormPresentation>
    <IsCustomizable>1</IsCustomizable>
    <IntroducedVersion>1.0.0.0</IntroducedVersion>
    <LocalizedNames>
      <LocalizedName description="Information" languagecode="1033" />
    </LocalizedNames>
    <Descriptions>
      <Description description="Main form for Application" languagecode="1033" />
    </Descriptions>
    <form>
      ...
    </form>
    <FormXml>
      <forms>...</forms>
    </FormXml>
  </systemform>
</forms>
```

### FormPresentation Codes

| Value | Form Type |
|-------|-----------|
| 0 | Main |
| 1 | QuickCreate |
| 2 | QuickView |
| 5 | AppointmentBook |
| 6 | Preview |
| 7 | Card |

## Form Layout Hierarchy

```
form
├── tabs
│   ├── tab (id, name, expanded)
│   │   ├── labels
│   │   │   └── label (description, languagecode)
│   │   └── columns
│   │       └── column (width in %)
│   │           └── sections
│   │               └── section (id, name, showlabel, showbar)
│   │                   ├── labels
│   │                   └── rows
│   │                       └── row
│   │                           └── cell (id, showlabel, colspan, rowspan)
│   │                               └── control (id, classid, datafieldname)
│   │                                   ├── parameters
│   │                                   └── events
│   └── ...
└── ...
```

## tab Element

Container for form sections:

```xml
<tab id="{guid}" name="tab_general" expanded="true" showlabel="true" locklevel="0">
  <labels>
    <label description="General" languagecode="1033" />
  </labels>
  <columns>
    <column width="100%">
      <sections>
        ...
      </sections>
    </column>
  </columns>
</tab>
```

**id**: Unique GUID  
**name**: Programmatic name  
**expanded**: Tab expanded by default (true/false)  
**showlabel**: Display tab label (true/false)  
**visible**: Tab visibility (true/false)  
**locklevel**: Prevents customization (0=None)

### Multi-Column Layouts

Tabs can have multiple columns:

```xml
<columns>
  <column width="60%">
    <sections>...</sections>
  </column>
  <column width="40%">
    <sections>...</sections>
  </column>
</columns>
```

## section Element

Groups related fields:

```xml
<section 
  id="{guid}" 
  name="section_details" 
  showlabel="true" 
  showbar="false" 
  visible="true"
  IsUserDefined="0"
  layout="varwidth"
  columns="1"
  labelwidth="115"
  celllabelalignment="Left"
  celllabelposition="Left"
>
  <labels>
    <label description="Details" languagecode="1033" />
  </labels>
  <rows>
    ...
  </rows>
</section>
```

**showlabel**: Display section title  
**showbar**: Show section divider  
**layout**: `varwidth` (variable) or `fixedwidth`  
**columns**: Number of columns (1, 2, 3, 4)  
**labelwidth**: Label column width in pixels  
**celllabelalignment**: Left/Center/Right  
**celllabelposition**: Left/Top

## row and cell Elements

Field positioning:

```xml
<rows>
  <row>
    <cell id="{guid}" showlabel="true" colspan="1" rowspan="1" auto="false">
      <labels>
        <label description="Application Name" languagecode="1033" />
      </labels>
      <control id="mnp_name" classid="{4273EDBD-AC1D-40d3-9FB2-095C621B552D}" datafieldname="mnp_name" disabled="false">
        <parameters />
      </control>
    </cell>
    <cell id="{guid}" showlabel="true">
      <labels>
        <label description="Status" languagecode="1033" />
      </labels>
      <control id="mnp_status" classid="{3EF39988-22BB-4f0b-BBBE-64B5A3748AEE}" datafieldname="mnp_status">
        <parameters />
      </control>
    </cell>
  </row>
</rows>
```

**colspan**: Columns to span  
**rowspan**: Rows to span  
**auto**: Auto-place control  
**showlabel**: Show field label

## control Element

Field controls with type and configuration:

```xml
<control 
  id="mnp_name" 
  classid="{4273EDBD-AC1D-40d3-9FB2-095C621B552D}" 
  datafieldname="mnp_name" 
  disabled="false"
  visible="true"
  isunbound="false"
  indicationOfSubgrid="false"
>
  <parameters>
    <MaxLength>100</MaxLength>
    <RequiredLevel>Required</RequiredLevel>
  </parameters>
</control>
```

**id**: Control identifier  
**classid**: Control type (see Control ClassIds)  
**datafieldname**: Bound field logical name  
**disabled**: Read-only (true/false)  
**visible**: Control visibility  
**isunbound**: Not bound to data (true/false)

### Control ClassIds

Common control types:

| ClassId | Control Type | Used For |
|---------|-------------|----------|
| `{4273EDBD-AC1D-40d3-9FB2-095C621B552D}` | Text Box | Single line text, numbers |
| `{F9A8A302-114E-466A-B582-6771B2AE0D92}` | Multi-line Text | Memo fields |
| `{3EF39988-22BB-4f0b-BBBE-64B5A3748AEE}` | Option Set | Picklist/choice |
| `{270BD3DB-D9AF-4782-9025-509E298DEC0A}` | Lookup | Entity references |
| `{5D68B988-0661-4db2-BC3E-17598AD3BE6C}` | Date Time | Date/time picker |
| `{B0C6723A-8503-4fd7-BB28-C8A06AC933C2}` | Two Options | Boolean/checkbox |
| `{533B9E00-756B-4312-95A0-DC888637AC78}` | Currency | Money fields |
| `{AA987274-CE4E-4271-A803-66164311A958}` | Whole Number | Integer |
| `{C3EFE0C3-0EC6-42be-8349-CBD9079DFD8E}` | Decimal | Decimal numbers |
| `{E7A81278-8635-4d9e-8D4D-59480B391C5B}` | Subgrid | Related records grid |
| `{5546F7F5-56BE-45fb-B074-EF7DF87BF78A}` | Quick View | Embedded form |
| `{F3015350-44A2-4AA0-97B5-00166532B5E9}` | Web Resource | HTML/JavaScript |
| `{ADA2203E-B4CD-49be-9DDF-234642B43B52}` | iFrame | External content |
| `{71716B6C-711E-476c-8AB8-5D11542BFB47}` | Notes | Notes control |
| `{06375649-c143-495e-a496-c962e5b4488e}` | Action Cards | Activity feed |

### Control Parameters

Configures control behavior:

```xml
<parameters>
  <MaxLength>100</MaxLength>
  <RequiredLevel>Required</RequiredLevel>
  <IMEMode>auto</IMEMode>
</parameters>
```

Common parameters:
- **MaxLength**: Max character length
- **RequiredLevel**: None/Required/Recommended
- **IMEMode**: Input method (auto, active, inactive, disabled)
- **Format**: Display format
- **DefaultViewId**: Default view for lookups/subgrids
- **ViewIds**: Available views for lookups

### Subgrid Parameters

```xml
<control id="subgrid_applications" classid="{E7A81278-8635-4d9e-8D4D-59480B391C5B}">
  <parameters>
    <ViewId>{view-guid}</ViewId>
    <IsUserView>false</IsUserView>
    <RelationshipName>mnp_contact_mnp_application</RelationshipName>
    <TargetEntityType>mnp_application</TargetEntityType>
    <AutoExpand>Fixed</AutoExpand>
    <EnableQuickFind>true</EnableQuickFind>
    <EnableViewPicker>true</EnableViewPicker>
    <EnableJumpBar>false</EnableJumpBar>
    <RecordsPerPage>10</RecordsPerPage>
  </parameters>
</control>
```

### Quick View Parameters

```xml
<control id="quickview_contact" classid="{5546F7F5-56BE-45fb-B074-EF7DF87BF78A}">
  <parameters>
    <FormId>{form-guid}</FormId>
    <IsUserDefined>1</IsUserDefined>
    <TargetEntityType>contact</TargetEntityType>
  </parameters>
</control>
```

### Web Resource Parameters

```xml
<control id="webresource_map" classid="{F3015350-44A2-4AA0-97B5-00166532B5E9}">
  <parameters>
    <Url>mnp_/html/map.html</Url>
    <Border>false</Border>
    <PassParameters>false</PassParameters>
    <Security>false</Security>
    <Scrolling>no</Scrolling>
  </parameters>
</control>
```

## events Element

JavaScript event handlers:

```xml
<events>
  <event name="onchange" application="false" active="true">
    <Handlers>
      <Handler functionName="FieldValidation.onChange" libraryName="mnp_/scripts/validation.js" handlerUniqueId="{guid}" enabled="true" parameters="fieldName,requiredLevel" passExecutionContext="true" />
    </Handlers>
  </event>
</events>
```

### Event Types

**Field Events**:
- `onchange`: Field value changes
- `onload`: Field loads

**Form Events**:
- `onload`: Form loads
- `onsave`: Form saves
- `onclose`: Form closes (deprecated)

**Tab Events**:
- `tabstatechange`: Tab expands/collapses

**Business Process Flow**:
- `onstagechange`: BPF stage changes
- `onstageselected`: BPF stage selected

### Handler Attributes

**functionName**: JavaScript function to call  
**libraryName**: Web resource containing function  
**handlerUniqueId**: Unique identifier  
**enabled**: Handler active (true/false)  
**parameters**: Comma-separated parameters to pass  
**passExecutionContext**: Pass execution context (true/false)

## formLibraries Element

JavaScript libraries loaded on form:

```xml
<formLibraries>
  <Library name="mnp_/scripts/main.js" libraryUniqueId="{guid}" />
  <Library name="mnp_/scripts/validation.js" libraryUniqueId="{guid}" />
</formLibraries>
```

Libraries loaded in order listed.

## Header and Footer

Special sections for header and footer:

```xml
<header>
  <rows>
    <row>
      <cell id="header_ownerid" showlabel="false">
        <control id="header_ownerid" classid="{270BD3DB-D9AF-4782-9025-509E298DEC0A}" datafieldname="ownerid">
          <parameters />
        </control>
      </cell>
      <cell id="header_statecode" showlabel="false">
        <control id="header_statecode" classid="{3EF39988-22BB-4f0b-BBBE-64B5A3748AEE}" datafieldname="statecode">
          <parameters />
        </control>
      </cell>
    </row>
  </rows>
</header>
```

## Navigation

Form navigation (left side menu):

```xml
<Navigation>
  <NavBar>
    <NavBarByRelationshipItem RelationshipName="mnp_contact_mnp_application" TitleResourceId="mnp_application.Form.Navigation.mnp_applications" />
    <NavBarItem Id="navActivities" Area="Details" Sequence="101" Icon="/_imgs/navbar/Activities_24.png">
      <Titles>
        <Title LCID="1033" Title="Activities" />
      </Titles>
    </NavBarItem>
  </NavBar>
</Navigation>
```

**NavBarByRelationshipItem**: Related entity subgrid  
**NavBarItem**: Custom navigation item

## Business Rules

Form-level business rules:

```xml
<businessrules>
  <businessrule id="{guid}" name="ValidateAmount">
    ...
  </businessrule>
</businessrules>
```

## Parsing Strategy

When analyzing FormXml:

1. **Identify form type**: Main, QuickCreate, QuickView
2. **Map tab structure**: Tab names and order
3. **List sections**: Section grouping and columns
4. **Extract fields**: Which fields are on the form
5. **Note required fields**: RequiredLevel in parameters
6. **Identify JavaScript**: Libraries and event handlers
7. **Find subgrids**: Related entity grids and views
8. **Check visibility**: Hidden tabs/sections/fields
9. **Map navigation**: Related entities in nav bar
10. **Document business rules**: Form-level validation

## Common Patterns

**Three-column header**:
```xml
<header>
  <row><cell>Owner</cell><cell>Status</cell><cell>Priority</cell></row>
</header>
```

**Two-column section**:
```xml
<section columns="2">
  <rows>
    <row>
      <cell>Field1</cell>
      <cell>Field2</cell>
    </row>
  </rows>
</section>
```

**Full-width field**:
```xml
<row>
  <cell colspan="2">
    <control datafieldname="mnp_description" />
  </cell>
</row>
```

**Spacer cell**:
```xml
<cell id="{guid}" auto="false" />
```

**Conditional visibility** (via business rules or JavaScript):
- Not directly in XML, controlled by scripts
- Check event handlers for `setVisible()` calls
