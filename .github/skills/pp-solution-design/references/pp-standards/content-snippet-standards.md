# Content Snippet Standards

Wiki source: `wiki/Welcome/Platform-Delivery-Playbook/Implementation-Standards/Using-PowerPages/Content-Snippet-Standards.md`

## WHY?
To provide best practices on existing snippets that need to be set, and to standardize the naming of new solution-specific snippets.

## Existing Standard Snippets (configure on every project)

| Snippet Name | Purpose |
|---|---|
| **Tracking Code** | JavaScript injected at the bottom of all pages — Google Analytics initialization, `initTimeouts()` call, loading spinner. Loaded from the portal footer. |
| **Head/Bottom** | Code added inside `<head></head>` — load CSS web files, `mnp_common.js`, and other global scripts |
| **Account/SignIn/PageCopy** | Login page copy (text shown above the login button) |
| **Account/Signin/TermsAndConditionsAgreementText** | "I Agree" button text for Terms & Conditions page |
| **Account/Signin/TermsAndConditionsHeading** | Page heading for Terms & Conditions page |
| **Account/Signin/TermsAndConditionsCopy** | Page copy for Terms & Conditions page |
| **Account/Signin/TermsAndConditionsButtonText** | Submit button text on Terms & Conditions page |
| **Browser Title Suffix** | Text appended to the browser `<title>` tag on all pages |

## MNP ODS Accelerator Snippets

| Snippet Name | Purpose |
|---|---|
| **Timeout Warning** | HTML content displayed in the warning modal (shown 2 minutes before session timeout — at 13 min of inactivity). Called from `Tracking Code`. |
| **Timeout Message** | HTML content displayed in the session-expired modal (shown at 15 min of inactivity). Called from `Tracking Code`. |

### Typical Tracking Code Snippet Content
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id={{ settings['GoogleAnalytics/TrackingID'] }}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '{{ settings["GoogleAnalytics/TrackingID"] }}');
</script>
<!-- Session Timeout Initialization -->
<script>
  $(document).ready(function() { initTimeouts(); });
</script>
```

## Solution-Specific Snippet Naming

`{Solution} - {Context} - {Type} - {Title}`

| Part | Description | Example |
|---|---|---|
| `{Solution}` | Solution prefix | `QUARTS` |
| `{Context}` | Grouping context | `Registration`, `Grant`, `Complaint` |
| `{Type}` | Content type | `JS`, `Text`, `HTML` |
| `{Title}` | Descriptive title | `Address Intro`, `Back to Overview` |

**Examples:**
- `QUARTS - Registration - Text - Address Intro` — common text for the Registration section
- `QUARTS - Registration - JS - Back to Overview` — JavaScript code for the Registration section (centralizes repetitive code)

### Benefits of Solution Snippets
- Centralizes text/content so changes are made in one place
- Allows content to be reused across Web Templates, Forms, and Entity Lists using `{{ snippets['QUARTS - Registration - Text - Address Intro'] }}`

## Organizational Tip
Create a **personal view** in the Portal Management App to filter solution-specific content snippets.

## Related
- [Pattern - Portal Analytics](../patterns/portal-analytics.md) — Tracking Code snippet
- [Pattern - Ontario ODS](../patterns/ontario-ods.md) — Timeout Warning/Message snippets
- [Component - mnp_common.js](../components/mnp-common-js-portal.md) — `initTimeouts()` function
- [Site Setting Standards](site-setting-standards.md) — `GoogleAnalytics/TrackingID` site setting
