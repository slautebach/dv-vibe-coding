# Web Page Standards

Wiki source: `wiki/Welcome/Platform-Delivery-Playbook/Implementation-Standards/Using-PowerPages/Web-Page-Standards.md`

## WHY?
To be consistent with the implementation of Power Pages web pages.

## Design Guidance

### General
- Create both **English** (and **French** if required) content web pages

### Custom JavaScript
- Scope of page-level JS should be on the **Copy (HTML)** or for coordinating between Basic Form, Entity List, and Advanced Form
- **Avoid page-level JS if there is a Basic Form, Entity List, or Advanced Form** — add JS at the form/list level instead for ease of reference and dependency checking

### Custom CSS
- Scope of page-level CSS is on the **Copy (HTML)**
- Preference is to add solution-specific CSS to a **{Solution}-specific CSS file** (web file)

### Existing Standard Web Pages
- **Home** — secure this page if you need to force login for the entire site

### Solution-Specific Pages

| Field | Guidance |
|---|---|
| **Partial URL** | Group related pages under a common prefix (e.g., `/registration/`, `/registration/add`) |
| **Title** | Language-specific heading — used by the Page Template/Web Template for browser title and page heading |
| **Copy (HTML)** | Page content — dependent on whether the Web Template renders this field. Use Lorem Ipsum as placeholder text during development. |
| **Parent Page** | Used to create URL hierarchy (breadcrumb path) |
| **Page Template** | Controls layout and rendering |

### Naming / Organizational Tip
Create a **personal view** in the Portal Management App to filter solution-specific web pages.

## Related
- [Web Site Standards](web-site-standards.md)
- [Web Template Standards](web-template-standards.md)
