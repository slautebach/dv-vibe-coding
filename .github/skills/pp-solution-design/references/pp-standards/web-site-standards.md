# Web Site Standards

Wiki source: `wiki/Welcome/Platform-Delivery-Playbook/Implementation-Standards/Using-PowerPages/Web-Site-Standards.md`

## WHY?
To be consistent with the implementation of a Power Pages web site.

## Design Guidance

1. Enable both **English** (and **French** if required) languages on the site
2. **Rename the Header and Footer templates** when there are multiple Power Pages web sites in the same environment (to avoid naming collisions)
3. Implement a clear URL structure using the **Partial URL** field, grouping related pages under the same prefix:

   | Partial URL | Purpose |
   |---|---|
   | `/registration/` | Summary page showing a list of registrations |
   | `/registration/add` | Page to add a new registration |
   | `/registration/edit` | Page to edit a selected registration |
   | `/registration/review` | Page to review before submitting or viewing history |

## Related
- [Web Page Standards](web-page-standards.md)
- [Web Template Standards](web-template-standards.md)
