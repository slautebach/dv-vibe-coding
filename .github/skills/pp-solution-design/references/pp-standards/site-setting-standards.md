# Site Setting Standards

Wiki source: `wiki/Welcome/Platform-Delivery-Playbook/Implementation-Standards/Using-PowerPages/Site-Setting-Standards.md`

## WHY?
To be consistent with Power Pages site settings and to document key settings used across MNP projects.

## Common Site Settings

### Google Analytics
| Setting | Purpose |
|---|---|
| `GoogleAnalytics/TrackingID` | Google Analytics tracking ID (G-XXXXXXXX or UA-XXXXXXXX). Read by `mnp_common.js` to initialize GA. |

### Google Maps
| Setting | Purpose |
|---|---|
| `GoogleMaps/APIKey` | Google Maps JavaScript API key. Used by `mnp_common.js` for map rendering. |

### Azure Storage (Web Files in Cloud)
| Setting | Purpose |
|---|---|
| `WebFiles/CloudStorageAccount` | Azure Storage connection string for cloud-hosted web files |
| `WebFiles/StorageLocation` | Storage location type (`AzureBlobStorage`) |

### Authentication — Terms and Conditions
| Setting | Purpose |
|---|---|
| `Authentication/Registration/TermsAgreementEnabled` | Requires users to accept T&Cs before registering |
| `Authentication/Registration/TermsPublicationDate` | Date of current T&Cs version (users re-prompted after updates) |

### Authentication — General (see Portal Authentication pattern for full list)
| Setting | Purpose |
|---|---|
| `Authentication/Registration/ExternalLoginEnabled` | `true` — enables external IdP login |
| `Authentication/Registration/OpenRegistrationEnabled` | `false` — disables self-registration (production) |
| `Authentication/Registration/InvitationEnabled` | `true` — required for Invitation/Redeem pattern |
| `Authentication/LoginPath` | Default redirect path for unauthenticated users (e.g., `/en/login`) |
| `Authentication/LogoutCompletedPath` | Redirect after logout (e.g., `/en/ps-logout` to trigger IdP logout) |

## Managing Site Settings
Site settings can be managed in:
- **Power Pages admin center** (make.powerpages.microsoft.com) > Site settings
- **Dataverse Portal Management App** > Site Settings table
- **Directly in Dataverse** via the `adx_sitesetting` table

## Related
- [Pattern - Portal Analytics](../patterns/portal-analytics.md) — GoogleAnalytics/TrackingID usage
- [Pattern - Portal Authentication](../patterns/portal-authentication.md) — auth site settings
- [Content Snippet Standards](content-snippet-standards.md) — Tracking Code snippet references GA ID
