# Pattern - Ontario Portal Design System (ODS)

Wiki source: `wiki/Welcome/Platform-Delivery-Playbook/Solution-Design/Pattern-%2D-Ontario-Portal-Design-System-(ODS).md`

## WHY?

MNP has developed a set of Power Pages components (Web Templates, Content Snippets, Redirects, Web Link Sets, Web Files) to support the Ontario Government portal standard. This allows project teams to start faster and focus on functionality rather than building ODS-standard templates from scratch.

- UI design principles: [https://designsystem.ontario.ca/](https://designsystem.ontario.ca/)
- Service design principles: [https://www.ontario.ca/page/ontario-digital-service](https://www.ontario.ca/page/ontario-digital-service)

## ODS Component Inventory

### Styling
- **ODS Theme**: Implemented as a custom theme with `ODSTheme.css` as a web file
  - Overrides for Power Pages/Bootstrap: loading spinner, tabbed panel, dataTables, buttons, etc.
- **Supplementary CSS files**: `datatables.min.css`, `ontario-ds-theme.css`
- ODS web file assets loaded from the Ontario Design System [Complete Package](https://www.npmjs.com/package/@ontario-digital-service/ontario-design-system-complete-styles)

### ODS Web Templates

| Template | Purpose |
|---|---|
| `ontario-Header` | Header: logo, language toggle, 2 shortcuts, flyout menu (Primary Navigation Web Link Set) |
| `ontario-Footer` | Footer: standard links and copyright |
| `ODS Breadcrumbs` | Renders breadcrumb path |
| `ODS Page Copy` | Renders page copy content block |
| `ODS Page Header` | Renders page title |
| `ODS Basic Page` | Base layout: breadcrumb + copy + page header |
| `ODS Basic Page - No Breadcrumbs` | Extends ODS Basic Page; breadcrumb block empty |
| `ODS Basic Page - No Title` | Extends ODS Basic Page; page header block empty |

### Content Snippets

| Snippet | Purpose |
|---|---|
| `Browser Title Suffix` | Text appended to browser `<title>` |
| `Timeout Warning` | HTML content in 2-minute warning modal (appears at 13 min inactivity) |
| `Timeout Message` | HTML content in session-expired modal (appears at 15 min inactivity) |
| `Tracking Code` | JavaScript: timeout warning timer, logout redirect, loading spinner, Google Analytics init |

The `Tracking Code` snippet should call `initTimeouts()` from `mnp_common.js`.

### Site Settings

| Setting | Purpose |
|---|---|
| `GoogleMaps/APIKey` | Used by `mnp_common.js` for Google Maps JS API |
| `GoogleAnalytics/TrackingID` | Used by `mnp_common.js` for Google Analytics |

### Web Link Sets
- **Primary Navigation** — populates the flyout menu in `ontario-Header`
  - Link: **My Ontario Account** (Display Order 999) → `https://test2.signin.ontario.ca/enduser/settings`
  - Login/Logout link is rendered automatically by `ontario-Header` based on authentication state

### Web Files
Required ODS files (CSS, JS, images, fonts) uploaded from the Ontario Design System npm package.
Folder structure follows standard conventions — see [Web File Standards](../pp-standards/web-file-standards.md).

### JavaScript Library
The **`mnp_common.js`** web file is loaded from `Head/Bottom` and provides portal helper functions.
See [Component - mnp_common.js](../components/mnp-common-js-portal.md) for full API.

## Public Secure Integration

1. Complete a provisioning session with the Public Secure team to provide portal URLs for each environment (DEV, SIT, UAT, PROD)
2. Configure a new Identity Provider: **Other** type > **SAML 2.0**, using the Public Secure Metadata URL
3. Add **Redirect** records:
   - `Public Secure Logout (EN)`: `/en/ps-logout` → `https://test2.signin.ontario.ca/login/signout?fromURI=https://{portalHomeURL}/en`
   - `Public Secure Logout (FR)`: `/fr/ps-logout` → French home URL
4. Add **My Ontario Account** web link to the **Primary Navigation** Web Link Set

For full authentication configuration, see [Pattern - Portal Authentication](portal-authentication.md).

## Redirects
- Public Secure Logout (EN and FR) — see above

## References
- [Ontario Design System](https://designsystem.ontario.ca/)
- [Ontario Digital Service](https://www.ontario.ca/page/ontario-digital-service)
- [ODS Portal Accelerator Pipeline](https://dev.azure.com/MNPDigital/DC-Delivery/_build?definitionId=187)
