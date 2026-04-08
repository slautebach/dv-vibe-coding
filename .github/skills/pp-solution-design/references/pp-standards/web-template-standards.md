# Web Template Standards

Wiki source: `wiki/Welcome/Platform-Delivery-Playbook/Implementation-Standards/Using-PowerPages/Web-Template-Standards.md`

## WHY?
To be consistent with Power Pages web template implementation and to standardize validation and page layout.

## Design Guidance

### Naming Convention

`{Solution} {Area Template} - {Action}`

| Part | Purpose | Example |
|---|---|---|
| `{Solution}` | Distinguishes solution templates from ODS base templates | `QUARTS` |
| `{Area Template}` | Functional area the template is responsible for | `Application Page` |
| `{Action}` | Optional variant for a specific purpose | `No Breadcrumbs`, `Create Renewal` |

**Examples:**
- `QUARTS Application Page` — general application web page template
- `QUARTS Application Page - No Breadcrumbs` — application page without breadcrumb
- `QUARTS Application Page - Create Renewal` — application page with renewal-specific handling

### Template Hierarchy

Create these base templates for the solution (all extending from the ODS `ontario-Header`/`ontario-Footer` base):

| Template | Extends From | Purpose |
|---|---|---|
| `{Solution} Breadcrumbs` | — | HTML/Liquid to render breadcrumb line |
| `{Solution} Basic Page` | ODS Basic Page | Base layout for all solution templates — all solution templates extend from this |
| `{Solution} Basic Page - No Breadcrumbs` | `{Solution} Basic Page` | Empty breadcrumb block |
| `{Solution} Basic Page - No Title` | `{Solution} Basic Page` | Empty page header block |
| `{Solution} {Area} Page` | `{Solution} Basic Page` | Area-specific layout with additional handling |
| `{Solution} {Area} Page - No Breadcrumbs` | `{Solution} {Area} Page` | Area page without breadcrumbs |
| `{Solution} {Area} Page - {Variant}` | `{Solution} {Area} Page` | Variant for specific use case |

### Security and Validation in Web Templates

#### XSS Escaping (use Liquid escape filters)
```liquid
{{ record.mnp_name | escape }}               {# HTML-escape — use for all user-provided content #}
{{ record.mnp_html | html_safe_escape }}     {# Safe HTML fragment #}
{{ param | url_escape }}                     {# URI-escape for use in URLs #}
{{ value | xml_escape }}                     {# XML-escape for XML output #}
```

#### QueryString Parameter Naming
Use short (2-3 char) parameter names related to the source table:
- `aid` → Account Id
- `mid` → mnp_Municipality Id
- `apid` → Application Id

Ensure related Basic Forms and Advanced Forms use the **same parameter name**.

#### FetchXML-Based Record Validation
Always validate the query string parameter and record ownership before rendering:

```liquid
{% fetchxml my_query %}
<fetch top="1">
  <entity name="mnp_application">
    <attribute name="mnp_applicationid" />
    <attribute name="mnp_statecode" />
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

#### Conditional Rendering Patterns
- Show/hide sections based on record status (`app.statuscode.value`)
- Redirect to appropriate page based on record state (e.g., submitted → read-only review page)
- Personalize content using `{{ user }}` and FetchXML results

### Organizational Tip
Create a **personal view** in the Portal Management App to filter solution-specific web templates.

## Related
- [Web Page Standards](web-page-standards.md)
- [Pattern - Portal Web Template](../patterns/portal-web-template.md)
- [Pattern - Ontario ODS](../patterns/ontario-ods.md)
