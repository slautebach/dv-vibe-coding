# Solution Structure Reference

## Solution.xml (Solution Manifest)

**Location**: `Other/Solution.xml`  
**Purpose**: Defines solution metadata, publisher information, and root components.

### Root Element

```xml
<ImportExportXml 
  version="9.2.x.x" 
  SolutionPackageVersion="9.2"
  languagecode="1033"
  generatedBy="CrmLive">
  <SolutionManifest>
    ...
  </SolutionManifest>
</ImportExportXml>
```

### Key Elements

#### UniqueName

Solution identifier (system name):

```xml
<UniqueName>IncomeAssistanceCore</UniqueName>
```

#### LocalizedNames

Display name per language:

```xml
<LocalizedNames>
  <LocalizedName description="Income Assistance Core" languagecode="1033" />
</LocalizedNames>
```

Language code 1033 = English (US).

#### Version

Semantic version (major.minor.build.revision):

```xml
<Version>1.0.0.212</Version>
```

#### Managed

Solution type:
- `0`: Unmanaged
- `1`: Managed
- `2`: Both (allows both managed and unmanaged import)

```xml
<Managed>2</Managed>
```

#### Publisher

Publisher metadata including customization prefixes:

```xml
<Publisher>
  <UniqueName>mnp</UniqueName>
  <LocalizedNames>
    <LocalizedName description="MNP" languagecode="1033" />
  </LocalizedNames>
  <CustomizationPrefix>mnp</CustomizationPrefix>
  <CustomizationOptionValuePrefix>12031</CustomizationOptionValuePrefix>
  <Addresses>...</Addresses>
</Publisher>
```

**CustomizationPrefix**: Applied to custom entities and fields (e.g., `mnp_application`)  
**CustomizationOptionValuePrefix**: Applied to option set values (e.g., `120310001`)

#### RootComponents

Lists all solution components:

```xml
<RootComponents>
  <RootComponent type="1" schemaName="mnp_application" behavior="0" />
  <RootComponent type="29" schemaName="Process_12345" behavior="0" />
  <RootComponent type="60" schemaName="mnp_/scripts/main.js" behavior="0" />
  <RootComponent type="61" id="{guid}" behavior="0" />
</RootComponents>
```

**type**: Component type code (see Component Types below)  
**schemaName**: Component identifier (for named components)  
**id**: GUID identifier (for components without schema names)  
**behavior**: Subcomponent handling:
- `0`: Include subcomponents
- `1`: Include selected subcomponents only
- `2`: Do not include subcomponents

### Component Type Codes

| Code | Component Type | Example |
|------|---------------|---------|
| 1 | Entity (Table) | `mnp_application` |
| 2 | Attribute (Field) | `mnp_name` |
| 9 | Option Set | `mnp_applicationstatus` |
| 10 | Entity Relationship | `mnp_application_contact` |
| 11 | Entity Key | `mnp_application_keys` |
| 24 | Form | `{guid}` |
| 26 | View (SavedQuery) | `{guid}` |
| 29 | Workflow | `ProcessName` |
| 31 | Report | `ReportName` |
| 35 | Business Rule | `{guid}` |
| 36 | Dashboard | `{guid}` |
| 60 | Web Resource | `mnp_/scripts/main.js` |
| 61 | Security Role | `{guid}` |
| 62 | Field Security Profile | `{guid}` |
| 66 | Custom Control | `CustomControlName` |
| 80 | App Module | `AppModuleName` |
| 84 | SiteMap | `SiteMapName` |
| 91 | Canvas App | `AppName` |
| 95 | Connection Reference | `ConnectionReferenceName` |
| 380 | Environment Variable Definition | `VariableName` |

## Customizations.xml (Solution Content Container)

**Location**: `Other/Customizations.xml`  
**Purpose**: Aggregates references to all customization types in the solution.

### Structure

```xml
<?xml version="1.0" encoding="utf-8"?>
<ImportExportXml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Entities />
  <Roles />
  <Workflows />
  <FieldSecurityProfiles />
  <Templates />
  <EntityMaps />
  <EntityRelationships />
  <OrganizationSettings />
  <optionsets />
  <CustomControls />
  <EntityDataProviders />
  <Languages>
    <Language>1033</Language>
  </Languages>
</ImportExportXml>
```

### Key Sections

#### Entities

References to all entity definitions. Actual definitions in `Entities/{name}/Entity.xml`:

```xml
<Entities>
  <Entity>
    <Name LocalizedName="Application" OriginalName="">mnp_application</Name>
    <EntityInfo>
      ...
    </EntityInfo>
  </Entity>
</Entities>
```

#### Roles

Security role definitions. Detailed definitions in `Roles/{name}.xml`:

```xml
<Roles>
  <Role id="{guid}" name="Case Worker">
    <RolePrivileges>
      ...
    </RolePrivileges>
  </Role>
</Roles>
```

#### Workflows

Process references. Full definitions in `Workflows/{guid}.xaml`:

```xml
<Workflows>
  <Workflow WorkflowId="{guid}" Name="Application Approval">
    ...
  </Workflow>
</Workflows>
```

#### optionsets

Global choice field definitions:

```xml
<optionsets>
  <optionset Name="mnp_applicationstatus">
    <IsGlobal>1</IsGlobal>
    <OptionSetType>picklist</OptionSetType>
    <options>
      <option value="120310000">
        <labels>
          <label description="Draft" languagecode="1033" />
        </labels>
      </option>
    </options>
  </optionset>
</optionsets>
```

#### EntityRelationships

Relationship references. Detailed definitions in `Other/Relationships/{name}.xml`:

```xml
<EntityRelationships>
  <EntityRelationship Name="mnp_application_contact">
    ...
  </EntityRelationship>
</EntityRelationships>
```

#### Languages

Available language codes:

```xml
<Languages>
  <Language>1033</Language>
  <Language>1036</Language>
</Languages>
```

Common language codes:
- `1033`: English (US)
- `1036`: French (France)
- `3084`: French (Canada)
- `1031`: German

## Solution Dependencies

Solutions can depend on other solutions. Dependencies tracked in:

```xml
<MissingDependencies>
  <MissingDependency>
    <Required key="" type="60" displayName="WebResourceName" solution="">
    </Required>
    <Dependent key="" type="1" displayName="EntityName" solution="">
    </Dependent>
  </MissingDependency>
</MissingDependencies>
```

## Parsing Strategy

When working with Solution.xml:

1. **Extract solution metadata**: UniqueName, Version, Publisher
2. **List root components** by type code
3. **Identify custom components** by checking customization prefix
4. **Map component references** to actual files in solution structure
5. **Note dependencies** for deployment planning

When working with Customizations.xml:

1. **Overview of included components**: Quick scan of what's in the solution
2. **Navigate to detailed files**: Use references to find Entity.xml, FormXml, etc.
3. **Understand relationships** between components
4. **Check language support** in Languages section
