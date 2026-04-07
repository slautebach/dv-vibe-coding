# XSD Schema Reference Index

This directory contains official Microsoft XSD schemas that define the structure and validation rules for Dynamics 365 solution XML files. These schemas are authoritative sources for understanding valid XML structures in Dataverse solutions.

## Schema Files Overview

### Core Solution Schemas

#### CustomizationsSolution.xsd

**Purpose**: Defines the complete solution package structure including Solution.xml and Customizations.xml  
**Validates**:
- Solution manifest (Solution.xml)
- Customizations aggregation (Customizations.xml)
- Entity definitions
- Option sets
- Web resources metadata
- Workflows references
- Root component definitions

**Key Elements**:
- `<ImportExportXml>`: Root container
- `<SolutionManifest>`: Solution metadata, publisher, version
- `<RootComponents>`: Component type codes and behavior
- `<EntityMetadata>`: Entity/table definitions
- `<optionset>`: Global choice field definitions

**Use when**: Validating solution packages, understanding root structure, checking component type codes

### Form Schemas

#### FormXml.xsd

**Purpose**: Defines form layout structure for model-driven apps  
**Validates**:
- Main forms
- Quick Create forms
- Quick View forms
- Card forms
- Form controls and events

**Key Elements**:
- `<form>`: Form root with tabs and sections
- `<tab>`: Tab containers
- `<section>`: Section containers within tabs
- `<cell>`: Control containers
- `<control>`: Field controls with parameters and events
- `<Library>`: JavaScript web resource references
- `<event>`: Form event handlers (OnLoad, OnSave, OnChange)

**Use when**: Validating form designs, understanding control types, debugging form import failures

**Related**: Includes RibbonCore.xsd for form ribbon definitions

### Query Schemas

#### Fetch.xsd

**Purpose**: Defines FetchXML query language syntax  
**Validates**:
- FetchXML queries in SavedQueries (system views)
- FetchXML in UserQuery (personal views)
- FetchXML in workflows and plugins
- Dashboard and report queries

**Key Elements**:
- `<fetch>`: Query root with paging and aggregate options
- `<entity>`: Primary table to query
- `<attribute>`: Columns to retrieve
- `<filter>`: WHERE clause conditions
- `<condition>`: Individual filter criteria
- `<link-entity>`: JOIN to related tables
- `<order>`: Sorting specifications

**Use when**: Validating queries, understanding filter operators, debugging view errors

**Important Attributes**:
- `aggregate`: Enable aggregation functions
- `distinct`: Remove duplicate rows
- `top`: Limit results (max 5,000)
- `page` + `count`: Pagination settings

### Navigation Schemas

#### SiteMap.xsd & SiteMapType.xsd

**Purpose**: Defines app navigation structure  
**Validates**:
- AppModuleSiteMaps (model-driven app navigation)
- Areas, groups, and subareas
- Navigation hierarchy

**Key Elements**:
- `<SiteMap>`: Root navigation container
- `<Area>`: Top-level navigation areas (e.g., Sales, Service)
- `<Group>`: Groupings within areas
- `<SubArea>`: Individual navigation items linking to entities or resources

**Use when**: Validating app navigation, understanding sitemap structure, configuring model-driven apps

### Ribbon Schemas

#### RibbonCore.xsd

**Purpose**: Core ribbon/command bar definitions  
**Validates**:
- Command definitions
- Button and tab structures
- Enable/display rules
- Actions and parameters

**Key Elements**:
- `<CommandDefinition>`: Command action definitions
- `<Button>`: Ribbon buttons
- `<EnableRules>`: When commands are enabled
- `<DisplayRules>`: When commands are visible

**Use when**: Customizing command bars, adding buttons, defining custom actions

#### RibbonTypes.xsd

**Purpose**: Ribbon component type definitions  
**Validates**:
- Control types and attributes
- Parameter structures
- UI element types

**Use when**: Understanding ribbon control types, validating complex ribbon customizations

#### RibbonWSS.xsd

**Purpose**: SharePoint-style ribbon extensions for Dynamics 365  
**Validates**:
- SharePoint-compatible ribbon elements
- WSS-specific controls

**Use when**: Working with SharePoint integration or legacy ribbon definitions

### Visualization Schemas

#### VisualizationDataDescription.xsd

**Purpose**: Defines chart and visualization configurations  
**Validates**:
- Dashboard charts
- Visualization XML in chart definitions
- Data series and axes
- Chart types and formatting

**Key Elements**:
- Chart data sources
- Series definitions
- Axis configurations
- Chart presentation options

**Use when**: Creating or validating dashboard charts, understanding chart XML structure

### Parameter and Configuration Schemas

#### ParameterXml.xsd

**Purpose**: Defines parameter passing for plugins and workflows  
**Validates**:
- Plugin step configurations
- Workflow parameter definitions
- Custom API parameters

**Use when**: Configuring plugin steps, passing parameters to custom code

#### isv.config.xsd

**Status**: **Deprecated** - Legacy schema  
**Purpose**: Original ISV extension configuration format  
**Modern Alternative**: Use RibbonXml for UI customizations

**Use when**: Working with very old solutions (< Dynamics CRM 2011 UR12)

#### reports.config.xsd

**Purpose**: Report configuration metadata  
**Validates**:
- Report definitions
- Report categories
- Report parameters

**Use when**: Working with SSRS reports in Dynamics 365

## Using XSD Schemas

### Validation Workflow

1. **Identify the XML file type** you're working with
2. **Locate the corresponding XSD** in this directory
3. **Open the XSD** to understand:
   - Required vs. optional elements (`minOccurs`, `maxOccurs`)
   - Required vs. optional attributes (`use="required"`)
   - Valid attribute values (`<xs:enumeration>`)
   - Pattern constraints (`<xs:pattern>`)
4. **Compare your XML** against schema rules
5. **Consult markdown references** (entity-schema.md, form-schema.md, etc.) for business context

### Reading XSD Definitions

**Element Definition:**
```xml
<xs:element name="tab" minOccurs="1" maxOccurs="unbounded">
```
- Element named "tab"
- At least 1 required (`minOccurs="1"`)
- Unlimited allowed (`maxOccurs="unbounded"`)

**Attribute Definition:**
```xml
<xs:attribute name="showlabel" type="xs:boolean" use="optional" default="true" />
```
- Attribute named "showlabel"
- Boolean type (true/false)
- Optional (can be omitted)
- Defaults to "true" if not specified

**Enumeration (Valid Values):**
```xml
<xs:attribute name="type">
  <xs:simpleType>
    <xs:restriction base="xs:string">
      <xs:enumeration value="and" />
      <xs:enumeration value="or" />
    </xs:restriction>
  </xs:simpleType>
</xs:attribute>
```
- Attribute "type" only accepts "and" or "or"

**Pattern (Regex Validation):**
```xml
<xs:attribute name="src">
  <xs:pattern value="(\$webresource:|/)(.)+"/>
</xs:attribute>
```
- Must start with either "$webresource:" or "/"
- Followed by one or more characters

### Common XSD Patterns

| Pattern | Meaning | Example |
|---------|---------|---------|
| `minOccurs="0"` | Optional element | May or may not appear |
| `minOccurs="1"` | Required element | Must appear at least once |
| `maxOccurs="1"` | Single occurrence | Can only appear once |
| `maxOccurs="unbounded"` | Multiple allowed | Can repeat unlimited times |
| `use="required"` | Required attribute | Must be present |
| `use="optional"` | Optional attribute | May be omitted |
| `type="xs:boolean"` | Boolean value | true/false or 1/0 |
| `type="xs:string"` | Text value | Any string |
| `type="xs:int"` | Integer | Whole numbers |

## Schema Dependencies

Some schemas reference other schemas:

- **FormXml.xsd** includes → **RibbonCore.xsd**
- **SiteMap.xsd** includes → **SiteMapType.xsd**
- **RibbonCore.xsd** includes → **RibbonTypes.xsd**

When validating XML, ensure you have access to all dependent schemas.

## Integration with Markdown References

The XSD schemas are **formal specifications**, while markdown references provide **context and examples**:

| Need | Use | For |
|------|-----|-----|
| Understand business concepts | Markdown (.md files) | What entities mean, workflow patterns |
| See structural rules | XSD (.xsd files) | Valid elements, required attributes |
| View examples | Markdown | Sample XML with annotations |
| Validate structure | XSD | Confirm XML conforms to schema |
| Debug errors | Both | XSD shows what's wrong, markdown shows what's right |

## Quick Lookup by File Type

| Your XML File | Primary XSD | Markdown Reference |
|---------------|-------------|-------------------|
| Solution.xml | CustomizationsSolution.xsd | solution-structure.md |
| Customizations.xml | CustomizationsSolution.xsd | solution-structure.md |
| Entity.xml | CustomizationsSolution.xsd | entity-schema.md |
| FormXml/*.xml | FormXml.xsd | form-schema.md |
| SavedQueries/*.xml | Fetch.xsd | fetchxml-reference.md |
| AppModuleSiteMaps/*.xml | SiteMap.xsd | (See XSD directly) |
| RibbonDiff.xml | RibbonCore.xsd | (See XSD directly) |
| Workflows/*.xaml | (XAML format) | workflow-schema.md |
| WebResources/*.data.xml | CustomizationsSolution.xsd | (Metadata only) |

## Additional Resources

**Microsoft Official Documentation:**
- [Customization Solutions File Schema](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/customization-solutions-file-schema)
- [FetchXML Reference](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/reference/)
- [Form XML Schema](https://learn.microsoft.com/en-us/power-apps/developer/model-driven-apps/customize-entity-forms)

**Schema Package Source:**
[Official Microsoft Schemas Download](https://download.microsoft.com/download/B/9/7/B97655A4-4E46-4E51-BA0A-C669106D563F/Schemas.zip)

---

**Note**: These schemas represent the Dynamics 365 solution format as of the schema package version. Microsoft may add new elements and attributes in future platform updates. Always refer to official Microsoft documentation for the latest schema definitions.
