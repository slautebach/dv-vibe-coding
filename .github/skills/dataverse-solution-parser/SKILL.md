---
name: dataverse-solution-parser
description: Parse and analyze Dynamics 365 Dataverse solution XML files including Entity.xml (table metadata), FormXml (form layouts), FetchXML (queries), Customizations.xml, Solution.xml, workflows, and web resources. Use when working with D365 solutions, analyzing entity definitions, understanding form structures, reviewing FetchXML queries, or documenting Dataverse components.
---

# Dataverse Solution Parser

Parse and analyze Dynamics 365 Dataverse solution XML files to extract metadata, understand structure, and document components.

## When to Use

Trigger this skill when:

- User mentions "Dataverse solution", "D365 solution", "Entity.xml", "FormXml", "FetchXML", "Customizations.xml"
- Analyzing table (entity) definitions or field metadata
- Understanding form layouts and UI structure
- Reviewing data queries (SavedQueries, views)
- Documenting solution components or workflows

## Solution File Structure

Dataverse solutions follow this pattern:

```
SolutionName/
├── Other/
│   ├── Solution.xml              # Solution manifest, root components
│   ├── Customizations.xml        # Aggregates all customizations
│   ├── Relationships.xml         # Entity relationships index
│   └── Relationships/{name}.xml  # Individual relationship definitions
├── Entities/{EntityName}/
│   ├── Entity.xml                # Table metadata, fields, relationships
│   ├── FormXml/{type}/{guid}.xml # Form layouts
│   ├── SavedQueries/{guid}.xml   # System views with FetchXML
│   └── RibbonDiff.xml           # Ribbon customizations
├── OptionSets/{name}.xml         # Global choice fields
├── Roles/{name}.xml              # Security role privileges
├── Workflows/{guid}.xaml         # Process definitions
├── WebResources/{name}.data.xml  # Client resources (JS, CSS, HTML, images)
├── CanvasApps/{name}.meta.xml    # Power Apps metadata
├── AppModules/{name}.xml         # Model-driven app definitions
└── AppModuleSiteMaps/{name}.xml  # Navigation structure
```

## XSD Schema References

This skill includes official Microsoft XSD schemas that define the structure and validation rules for Dynamics 365 solution XML files. These schemas are located in `references/xsd-schemas/` and provide authoritative definitions for validating and understanding XML structure.

📘 **Comprehensive Guide**: See [xsd-schemas.md](references/xsd-schemas.md) for detailed documentation of all XSD schemas, validation workflows, and usage patterns.

### Available Schemas

| XSD File                                                   | Validates                        | When to Use                                                                      |
| ---------------------------------------------------------- | -------------------------------- | -------------------------------------------------------------------------------- |
| **CustomizationsSolution.xsd**                             | Customizations.xml, Solution.xml | Validate solution manifests, understand root structure and component definitions |
| **Fetch.xsd**                                              | FetchXML queries                 | Validate queries in SavedQueries, UserQuery, workflows, and code                 |
| **FormXml.xsd**                                            | Form layouts                     | Validate form designs, understand control types and event structures             |
| **SiteMap.xsd** & **SiteMapType.xsd**                      | AppModuleSiteMaps                | Validate navigation structures and area definitions                              |
| **RibbonCore.xsd**, **RibbonTypes.xsd**, **RibbonWSS.xsd** | Ribbon customizations            | Validate command bars, buttons, and ribbon definitions                           |
| **VisualizationDataDescription.xsd**                       | Chart definitions                | Validate dashboard charts and visualization XML                                  |
| **ParameterXml.xsd**                                       | Plugin/workflow parameters       | Validate parameter passing in custom code                                        |
| **isv.config.xsd**                                         | ISV configuration                | Legacy ISV.config files (deprecated, use RibbonXml instead)                      |
| **reports.config.xsd**                                     | Report configurations            | Report metadata and configuration                                                |

### When to Use XSD Schemas

**Use XSD schemas when you need to:**

- **Validate XML structure**: Confirm XML files conform to Microsoft's schema
- **Understand element hierarchy**: See what child elements are allowed
- **Check attributes**: Verify required vs. optional attributes
- **Find valid values**: Discover enumeration constraints (e.g., FormPresentation codes)
- **Understand data types**: Learn about field types, patterns, and restrictions
- **Debug parsing errors**: Identify schema violations causing import failures

**Use Markdown references when you need to:**

- **Understand business concepts**: Learn what entities, forms, and fields mean
- **See examples**: Review sample XML with annotations
- **Follow workflows**: Step-by-step guidance for common tasks
- **Quick reference**: Lookup tables for codes, types, and patterns

**Best approach**: Start with markdown references for context, then consult XSD schemas for detailed structural validation.

### Reading XSD Schemas

XSD schemas define:

- **Elements**: `<xs:element>` - What XML elements are allowed
- **Attributes**: `<xs:attribute>` - What attributes elements can have
- **Types**: `<xs:complexType>`, `<xs:simpleType>` - Structure and constraints
- **Enumerations**: `<xs:enumeration>` - Valid values for attributes
- **Patterns**: `<xs:pattern>` - Regular expressions for validation
- **Cardinality**: `minOccurs`, `maxOccurs` - How many times elements can appear

**Example from FormXml.xsd:**

```xml
<xs:element name="internaljscriptfile" minOccurs="0" maxOccurs="100000">
  <xs:attribute name="src" use="required">
    <xs:pattern value="(\$webresource:|/)(.)+"/>
  </xs:attribute>
</xs:element>
```

This defines that:

- JavaScript file includes are optional but can have up to 100,000 entries
- The `src` attribute is required
- The `src` must start with `$webresource:` or `/` followed by at least one character

## Core Workflow

### 1. Identify File Type

Determine which XML file you're working with and load appropriate references:

**For Solution and Customization Files:**

- **Markdown**: [solution-structure.md](references/solution-structure.md) - Context and examples
- **XSD**: [CustomizationsSolution.xsd](references/xsd-schemas/CustomizationsSolution.xsd) - Formal schema

**For Entity Definitions:**

- **Markdown**: [entity-schema.md](references/entity-schema.md) - Field types and patterns
- **XSD**: Defined within CustomizationsSolution.xsd

**For Form Layouts:**

- **Markdown**: [form-schema.md](references/form-schema.md) - Control types and structure
- **XSD**: [FormXml.xsd](references/xsd-schemas/FormXml.xsd) - Form element validation

**For FetchXML Queries:**

- **Markdown**: [fetchxml-reference.md](references/fetchxml-reference.md) - Operators and patterns
- **XSD**: [Fetch.xsd](references/xsd-schemas/Fetch.xsd) - Query structure validation

**For Workflows:**

- **Markdown**: [workflow-schema.md](references/workflow-schema.md) - Process definitions
- **XSD**: Defined within CustomizationsSolution.xsd (XAML structure)

**For Navigation and Ribbons:**

- **XSD**: [SiteMap.xsd](references/xsd-schemas/SiteMap.xsd), [RibbonCore.xsd](references/xsd-schemas/RibbonCore.xsd)
- Use XSD schemas directly for these specialized components

### 2. Locate Files in Workspace

Dataverse solutions in this workspace are at: `c:\Dev\Sask\src\D365Solution\`

**Find specific entities:**

```
src/**/{SolutionName}/Entities/{EntityLogicalName}/Entity.xml
```

**Find forms for an entity:**

```
src/**/{SolutionName}/Entities/{EntityLogicalName}/FormXml/main/{guid}.xml
```

**Find views for an entity:**

```
src/**/{SolutionName}/Entities/{EntityLogicalName}/SavedQueries/{guid}.xml
```

**Find web resources (including North52):**

```
src/**/{SolutionName}/WebResources/{name}.data.xml
```

### 3. Parse Key Information

When analyzing files, extract:

**From Entity.xml:**

- Logical name and display names
- Custom vs. system fields (IsCustomField)
- Field types, required levels, max lengths
- Relationships (1:N, N:1, N:N)
- Option sets and their values

**From FormXml:**

- Form type (Main=0, QuickCreate=1, QuickView=2)
- Tab and section structure
- Field controls and their configuration
- JavaScript event handlers and libraries
- Required fields and visibility rules

**From FetchXML (in SavedQueries):**

- Primary entity and attributes
- Filters and conditions
- Linked entities (joins)
- Sorting and aggregation

**From Solution.xml:**

- Root components and their types
- Publisher and customization prefix
- Solution version
- Component dependencies (behavior attribute)

### 4. Key Patterns to Recognize

**Naming Conventions:**

- **LogicalName**: lowercase, API identifier (e.g., `mnp_application`)
- **PhysicalName**: PascalCase, database column (e.g., `mnp_ApplicationId`)
- **DisplayName**: User-facing label in localized names

**Custom Components:**

- Custom entities: prefixed with publisher prefix (e.g., `mnp_`)
- Custom fields: `IsCustomField="1"`
- Option set values: start with publisher option value prefix (e.g., `120310001`)

**Component Type Codes** (in Solution.xml RootComponents):

- 1: Entity
- 29: Workflow
- 60: WebResource
- 61: Role
- 62: AppModule
- 80: SiteMap

**Relationship Types:**

- OneToManyRelationship (1:N)
- ManyToOneRelationship (N:1)
- ManyToManyRelationship (N:N)

**Field Types** (common):

- `lookup`: Related entity reference
- `picklist`: Option set (choice)
- `nvarchar`: Single line text
- `memo`: Multi-line text
- `datetime`: Date/time
- `bit`: Two options (boolean)
- `money`: Currency
- `decimal`/`double`: Numbers

### 5. Extract Dependencies

When documenting components, identify:

- **Form dependencies**: JavaScript web resources in `<Library>` elements
- **View dependencies**: Related entities in FetchXML `<link-entity>`
- **Field dependencies**: Lookups reference other entities
- **Web resource dependencies**: `<DependencyXml>` in WebResource files

## Advanced Scenarios

### North52 Formula Analysis

North52 formulas are stored as web resources (WebResourceType=4, XML):

```
src/**/IncomeAssistanceNorth52/WebResources/mnp_/N52/Formula/...
```

When analyzing North52 formulas, also reference the **north52-formula-analyzer** skill for formula-specific parsing.

### FetchXML in Multiple Contexts

FetchXML appears in:

- **SavedQueries**: System views
- **UserQuery**: Personal views
- **Workflows**: Data retrieval steps
- **Dashboards**: Chart and grid queries
- **JavaScript**: Dynamic queries in web resources

### Multi-Language Support

Localized content is in `<LocalizedNames>` and `<LocalizedLabels>`:

```xml
<LocalizedNames>
  <LocalizedName description="Application" languagecode="1033" />
</LocalizedNames>
```

Language code 1033 = English (US).

## Integration with Other Tools

**For schema validation**: Use XSD files in `references/xsd-schemas/`:

- See [xsd-schemas.md](references/xsd-schemas.md) for complete schema reference
- Validate XML structure before importing solutions
- Understand valid elements, attributes, and constraints
- Debug schema violations causing import failures

**For official documentation**: Use **microsoft-docs** skill to query:

- Schema definitions: "Dataverse customization solutions file schema"
- FetchXML syntax: "FetchXML operators" or "FetchXML aggregate functions"
- Entity references: "WebResource entity reference" or "savedquery entity"

**For code samples**: Use **microsoft-code-reference** skill for SDK usage:

- Entity retrieval
- FetchXML execution
- Metadata queries

**For formula analysis**: Use **north52-formula-analyzer** skill when web resource name contains `/N52/Formula/`.

## Common Tasks

**Validate XML structure:**

1. Identify the XML file type (Form, FetchXML, Solution, etc.)
2. Read the corresponding XSD from `references/xsd-schemas/`
3. Check for required elements and attributes
4. Verify enumeration values and patterns match schema constraints
5. Cross-reference with markdown docs for business context

**Document entity structure:**

1. Read Entity.xml from `Entities/{name}/Entity.xml`
2. Load [entity-schema.md](references/entity-schema.md) for attribute parsing
3. Extract fields with types, required levels, and descriptions
4. List relationships with related entities

**Analyze form layout:**

1. Read FormXml from `Entities/{name}/FormXml/{type}/{guid}.xml`
2. Load [form-schema.md](references/form-schema.md) for control types
3. Extract tabs → sections → fields hierarchy
4. Note JavaScript libraries and event handlers

**Understand view query:**

1. Read SavedQueries from `Entities/{name}/SavedQueries/{guid}.xml`
2. Load [fetchxml-reference.md](references/fetchxml-reference.md) for operators
3. Parse FetchXML: entity, filters, linked entities
4. Extract layoutxml for column configuration

**Map solution components:**

1. Read Solution.xml from `Other/Solution.xml`
2. Load [solution-structure.md](references/solution-structure.md) for component types
3. List all root components with type codes
4. Identify managed vs. unmanaged (Managed=0 for unmanaged, 1 for managed, 2 for both)

## Quick Reference

**File Extensions & Formats:**

- `.xml`: Metadata, forms, views, entities
- `.xaml`: Workflows (Windows Workflow Foundation)
- `.data.xml`: Web resource metadata

**Always Case-Sensitive:**

- Logical names in queries and code
- Element names in XML
- Attribute names in XML

**Version Tracking:**

- `<IntroducedVersion>`: When component was added
- Used for ALM and upgrade scenarios

## Schema Validation

This skill includes official Microsoft XSD schemas for validating Dynamics 365 solution XML files. These schemas are located in `references/xsd-schemas/` and can be used to:

- **Validate XML structure** before importing solutions
- **Understand valid elements and attributes** when creating custom XML
- **Debug import errors** by identifying schema violations
- **Ensure compliance** with Microsoft's solution format

### Using XSD Schemas for Validation

When analyzing solution files or debugging import issues:

1. **Identify the file type** (e.g., FormXml, SavedQuery, Solution.xml)
2. **Locate the corresponding XSD** in `references/xsd-schemas/`
3. **Check for structural violations**: Missing required attributes, invalid element nesting, unsupported values
4. **Consult markdown references** for business context and examples

### Common Validation Scenarios

**Form Import Failures:**

- Check [FormXml.xsd](references/xsd-schemas/FormXml.xsd) for valid control types and event structures
- Validate JavaScript library references follow the `$webresource:` pattern

**Query Syntax Errors:**

- Validate FetchXML against [Fetch.xsd](references/xsd-schemas/Fetch.xsd)
- Verify operators and aggregate functions are correctly structured

**Solution Import Errors:**

- Check [CustomizationsSolution.xsd](references/xsd-schemas/CustomizationsSolution.xsd) for valid component types
- Ensure root components have required attributes

**Ribbon Customization Issues:**

- Validate against [RibbonCore.xsd](references/xsd-schemas/RibbonCore.xsd) for command definitions
- Check button and tab structures in RibbonTypes.xsd

### Schema Files Source

The XSD schemas in this skill are official Microsoft schemas from the [Dynamics 365 Customization Solutions Schema Package](https://download.microsoft.com/download/B/9/7/B97655A4-4E46-4E51-BA0A-C669106D563F/Schemas.zip). They provide authoritative definitions for all solution XML formats.

## Output Guidelines

When documenting Dataverse components:

- Use entity display names for user-facing documentation
- Use logical names for technical specifications
- Include field types and required levels
- Note custom vs. system components
- List dependencies and relationships
- Provide context about business purpose where evident
