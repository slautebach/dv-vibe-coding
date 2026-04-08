# Pattern - Portal Web Template

Wiki source: `wiki/Welcome/Platform-Delivery-Playbook/Solution-Design/Pattern-%2D-Portal-Web-Template.md`

> **Note:** This pattern page is currently a stub in the wiki. Guidance below is synthesized from Web Template Standards and the ODS pattern.

## WHY?

Web templates provide the layout, security validation, and Liquid logic layer for Power Pages portal pages. A consistent web template pattern ensures:
- Uniform page layout and branding (ODS header/footer)
- Security and ownership checks before rendering sensitive content
- Reusable template inheritance hierarchy reduces duplication

## Template Inheritance Hierarchy

All solution web templates should follow this hierarchy:

```
ODS Basic Page (MNP ODS Accelerator base)
  └── {Solution} Basic Page           ← solution base; defines all blocks
        ├── {Solution} Basic Page - No Breadcrumbs
        ├── {Solution} Basic Page - No Title
        └── {Solution} {Area} Page    ← area-specific layout (e.g., Application Page)
              ├── {Solution} {Area} Page - No Breadcrumbs
              └── {Solution} {Area} Page - {Variant}  (e.g., Create Renewal)
```

## Naming Convention

`{Solution} {Area Template} - {Action}`

- `{Solution}` — distinguishes solution-specific templates from ODS base templates
- `{Area Template}` — functional area (e.g., Application Page, Registration Page)
- `{Action}` — optional variant (e.g., No Breadcrumbs, Create Renewal)

**Examples:**
- `QUARTS Application Page`
- `QUARTS Application Page - No Breadcrumbs`
- `QUARTS Application Page - Create Renewal`

## Security and Validation in Web Templates

Always apply these patterns in solution web templates:

### 1. XSS Escaping (Liquid filters)
```liquid
{{ record.mnp_projectname | escape }}           {# HTML-escape #}
{{ record.mnp_html_content | html_safe_escape }}  {# Safe HTML fragment #}
{{ param | url_escape }}                         {# URI-escape #}
```

### 2. QueryString Parameter Validation
- Use short (2-3 char) parameter names related to the source table:
  - `aid` → AccountId
  - `mid` → mnp_MunicipalityId
  - `apid` → ApplicationId
- Validate parameters with FetchXML before rendering; redirect on invalid/missing

### 3. FetchXML-based Record Retrieval and Conditions
```liquid
{% fetchxml my_query %}
<fetch top="1">
  <entity name="mnp_application">
    <attribute name="mnp_applicationid" />
    <attribute name="mnp_status" />
    <filter>
      <condition attribute="mnp_applicationid" operator="eq" value="{{ request.params['apid'] | escape }}" />
      <condition attribute="mnp_portaluserid" operator="eq" value="{{ user.id }}" />
    </filter>
  </entity>
</fetch>
{% endfetchxml %}

{% assign app = my_query.results.entities[0] %}
{% if app == null %}
  {% redirect '/en/access-denied' %}
{% endif %}
```

### 4. Conditional Rendering
- Show/hide sections based on record status
- Redirect to appropriate page based on record state (e.g., submitted → read-only review)

## ODS Base Templates (MNP ODS Accelerator)

| Template | Purpose |
|---|---|
| `ontario-Header` | Header with logo, language toggle, Primary Navigation flyout |
| `ontario-Footer` | Footer with standard links and copyright |
| `ODS Breadcrumbs` | Breadcrumb path rendering |
| `ODS Page Copy` | Page copy content block |
| `ODS Page Header` | Page title block |
| `ODS Basic Page` | Base layout: breadcrumb + copy + title |
| `ODS Basic Page - No Breadcrumbs` | Extends ODS Basic Page, empty breadcrumb block |
| `ODS Basic Page - No Title` | Extends ODS Basic Page, empty title block |

## Related
- [Web Template Standards](../pp-standards/web-template-standards.md)
- [Pattern - Ontario ODS](ontario-ods.md)
- [Pattern - Portal Authentication](portal-authentication.md)
