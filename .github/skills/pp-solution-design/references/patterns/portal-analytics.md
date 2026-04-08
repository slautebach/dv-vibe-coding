# Pattern - Portal Analytics

Wiki source: `wiki/Welcome/Platform-Delivery-Playbook/Solution-Design/Pattern-%2D-Portal-Analytics.md`

> **Note:** This pattern page is currently a stub in the wiki. Guidance below is synthesized from the ODS pattern and Content Snippet standards.

## WHY?

- Track user behaviour, form abandonment, and page performance on Power Pages portals
- Provide session timeout warnings to users to prevent data loss
- Support Ontario Government analytics requirements (Google Analytics)

## Google Analytics Integration

Google Analytics is integrated via the **Tracking Code** Content Snippet, which is injected into every portal page.

### Setup
1. Obtain a Google Analytics **Tracking ID** (G-XXXXXXXX or UA-XXXXXXXX)
2. Add a **Site Setting**: `GoogleAnalytics/TrackingID` = your tracking ID
3. The `mnp_common.js` library reads this site setting and initializes GA automatically via the **Tracking Code** content snippet

### Tracking Code Content Snippet
The **Tracking Code** snippet (loaded from `Head/Bottom` or footer) should:
- Initialize Google Analytics with the tracking ID from `GoogleAnalytics/TrackingID`
- Call `initTimeouts()` from `mnp_common.js` to activate session timeout warnings
- Set up the loading spinner

**Example Tracking Code snippet content:**
```javascript
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id={{ settings['GoogleAnalytics/TrackingID'] }}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '{{ settings["GoogleAnalytics/TrackingID"] }}');
</script>
<!-- Session Timeout -->
<script>
  $(document).ready(function() { initTimeouts(); });
</script>
```

## Session Timeout

Session timeouts protect sensitive data by warning users and forcing re-authentication after inactivity.

Managed via **Content Snippets** (set up as part of the ODS template):

| Content Snippet | Purpose |
|---|---|
| **Timeout Warning** | HTML shown in warning modal 2 minutes before timeout (at 13 min) |
| **Timeout Message** | HTML shown after session expires (at 15 min) |
| **Tracking Code** | JavaScript that drives timeout timer via `initTimeouts()` from `mnp_common.js` |

### `initTimeouts()` function (mnp_common.js)
- Warning modal fades in at **13 minutes** of inactivity
- Session expired modal fades in at **15 minutes** of inactivity
- Redirect to logout URL after timeout

## Related
- [Pattern - Ontario ODS](ontario-ods.md) — ODS template and Tracking Code snippet
- [Content Snippet Standards](../pp-standards/content-snippet-standards.md)
- [Site Setting Standards](../pp-standards/site-setting-standards.md)
- [Component - mnp_common.js](../components/mnp-common-js-portal.md) — `initTimeouts()` function
