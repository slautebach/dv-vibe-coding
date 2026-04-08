# Pattern - Portal Authentication

Wiki source: `wiki/Welcome/Platform-Delivery-Playbook/Solution-Design/Pattern-%2D-Portal-Authentication.md`

## WHY?

Power Pages portals expose sensitive program data to external users. A consistent authentication pattern ensures:
- Users are securely identified before accessing protected pages or submitting data
- Identity is delegated to a trusted provider (no passwords stored in the portal)
- Authenticated users are linked to a Dataverse **Contact** record for personalised dashboards and record ownership
- Ontario Government clients use **Public Secure** (provincial identity provider) without custom OAuth development
- Session lifecycle (timeout warnings, forced logouts) is handled uniformly

## Applications

| Scenario | Provider | Notes |
|---|---|---|
| Ontario Government citizen portals | Public Secure (SAML 2.0) | Use Ontario Account credentials |
| Enterprise / internal portals | Microsoft Entra ID (Azure AD) | Corporate SSO, MFA via Conditional Access |
| Invitation-only portals | Any + Redeem Invitation pattern | Only users with valid reference number can access |
| Anonymous + authenticated hybrid | Any | Start anonymous, authenticate to save/resume |

## Identity Provider Options

| Provider | Protocol | Use Case | Notes |
|---|---|---|---|
| **Public Secure** | SAML 2.0 | Ontario Government citizen portals | Requires provisioning session per environment |
| **Microsoft Entra ID (AAD)** | OIDC / SAML 2.0 | Staff/partner portals | Built-in provider in Power Pages |
| **Local sign-in** | ASP.NET Identity | Dev/test only | Not for production |
| **Other SAML 2.0** | SAML 2.0 | Custom IdP, AD FS | Configure via Other > SAML 2.0 |
| **OpenID Connect** | OIDC | Any OIDC-compliant IdP | Configure via Other > OpenID Connect |

> **Default for MNP Ontario projects:** Public Secure (SAML 2.0). Disable local sign-in and open registration in production.

## Design Guidance

1. **Disable open registration and local sign-in in production** — set Open registration: Off and External login: On
2. **One active SAML 2.0 provider per site** — SAML 2.0 and OIDC can each have one active configuration
3. **Contact mapping with email: always ON** — auto-links authenticated users to existing Dataverse Contact by email
4. **Plan EN/FR login pages** — configure separate redirect paths (`/en/login`, `/fr/login`) for bilingual portals
5. **Logout must redirect to the IdP** — add a Redirect (e.g., `/en/ps-logout`) that sends the user to the Public Secure sign-out URL with `fromURI` back to your portal home page

## Implementation Guide

### Configure General Authentication Settings
1. In Power Pages Studio: **Security** > **Identity providers** > **Authentication settings**
   - External login: **On**
   - Open registration: **Off** (production)
   - Require unique email: **On**
2. Save and restart site for immediate effect

### Configure SAML 2.0 Provider (Public Secure — Ontario Government)
1. Contact Public Secure provisioning team — provide the **Reply URL** for each environment (DEV, SIT, UAT, PROD)
   - Reply URL format: `https://{portal-domain}/signin-saml_{providername}`
2. In Power Pages Studio: **Security** > **Identity providers** > **+ New provider**
   - Login provider: **Other**
   - Protocol: **SAML 2.0**
   - Provider name: `Public Secure`
3. Copy the **Reply URL** and provide it to the Public Secure team; receive back the **Federation Metadata Document URL**
4. Enter:
   - Metadata address: `{PublicSecure Metadata URL}`
   - Authentication type: `entityID` from metadata document
   - Service provider realm: `https://{portal-domain}/`
   - Assertion consumer service URL: same as Reply URL
   - Contact mapping with email: **On**

### Add Public Secure Logout Redirects
Create portal **Redirect** records for each language:
- **Name:** Public Secure Logout (EN)
- **Inbound URL:** `/en/ps-logout`
- **Target URL:** `https://test2.signin.ontario.ca/login/signout?fromURI=https://{portalHomeURL}/en`

### Key Authentication Site Settings

| Site Setting | Example Value | Purpose |
|---|---|---|
| `Authentication/Registration/ExternalLoginEnabled` | `true` | Enable external IdP login |
| `Authentication/Registration/OpenRegistrationEnabled` | `false` | Disable self-registration (production) |
| `Authentication/Registration/InvitationEnabled` | `true` | Required for Invitation pattern |
| `Authentication/LoginPath` | `/en/login` | Redirect for unauthenticated users |
| `Authentication/LogoutCompletedPath` | `/en/ps-logout` | Redirect after logout (triggers IdP logout) |
| `Authentication/UserManager/UserValidator/RequireUniqueEmail` | `true` | Enforce unique email |

### Contact Linking
When a user authenticates with Contact mapping with email: On, Power Pages:
1. Extracts the email claim from the SAML assertion or OIDC token
2. Queries Dataverse for a **Contact** with matching `emailaddress1`
3. If found → links portal user to that Contact
4. If not found → creates a new Contact and links it

Access the linked Contact in Liquid: `{{ user }}` and `{{ user.id }}`

**Important:** Ensure pre-created Contact records have the correct `emailaddress1` before users authenticate for the first time.

## Authentication Flow (SAML 2.0 — Public Secure)

```
User -> Portal: Navigate to protected page
Portal -> User: 302 Redirect SAML AuthnRequest to IdP
User -> Public Secure: Follow redirect to Ontario Account login
Public Secure -> Portal: POST SAML Assertion to Reply URL
Portal -> Portal: Validate assertion signature and audience
Portal -> Dataverse: Query Contact by emailaddress1
  [found] -> Link portal user to Contact
  [not found] -> Create new Contact record
Portal -> User: Set auth cookie, redirect to original destination
```

## References
- [Configure authentication for your Power Pages site](https://learn.microsoft.com/en-us/power-pages/security/authentication/configure-site)
- [Configure a SAML 2.0 provider](https://learn.microsoft.com/en-us/power-pages/security/authentication/saml2-provider)
- [Configure an OpenID Connect provider](https://learn.microsoft.com/en-us/power-pages/security/authentication/openid-provider)
- [Power Pages site settings](https://learn.microsoft.com/en-us/power-pages/configure/configure-site-settings)

## Related
- [Pattern - Ontario ODS](ontario-ods.md)
- [Pattern - Redeem Invitation](redeem-invitation.md)
- [Pattern - Portal Submission](portal-submission.md)
