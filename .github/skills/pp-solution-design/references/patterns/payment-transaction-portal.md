# Pattern - Payment Transaction Portal

Wiki sources:
- `wiki/Welcome/Platform-Delivery-Playbook/Solution-Design/Pattern-%2D-Payment-Transaction.md` (stub)
- `wiki/Welcome/Platform-Delivery-Playbook/Solution-Design/Pattern-%2D-Payment-Transaction/CCPay-Integration-(Ontario-Government).md`
- `wiki/Welcome/Platform-Delivery-Playbook/Solution-Design/Pattern-%2D-Payment-Transaction/Moneris-Integration.md`

> **Note:** The Pattern - Payment Transaction page is currently a placeholder. Details below are based on CCPay and Moneris sub-pages.

## Overview

Power Pages portal payment flows integrate with external payment processors to collect fees during citizen-facing program submissions. MNP has implemented integrations for:

| Processor | Use Case |
|---|---|
| **CCPay** | Ontario Government programs (provincial payment gateway) |
| **Moneris** | General commercial payment processing |

---

## CCPay Integration (Ontario Government)

CCPay is the Ontario Government's standard payment gateway for citizen-facing portal transactions.

### Key Resources
- [CCPay Interface Specifications](https://ontariogov.sharepoint.com/:b:/r/sites/CSC-Intranet/BSSIM/...) (internal Ontario Gov link)
- CCPay REST API endpoint (staging): `https://ws.stage.gwy.apic.sus.gov.on.ca:443/ops/ops-partner/v1/ccpayrestservice`

### Configuration (mnp_MappingConfig Environment Variable)

The CCPay integration is configured via the `mnp_MappingConfig` environment variable:

```json
{
  "CCPay": {
    "Endpoint": "https://ws.stage.gwy.apic.sus.gov.on.ca:443/ops/ops-partner/v1/ccpayrestservice",
    "X-IBM-Client-Id": "{client-id}",
    "X-IBM-Client-Secret": "{client-secret}",
    "Passphrase": "{passphrase}",
    "AllowedRestClientUserAgentForTest": "vscode-restclient",
    "AllowedHttpRequestOrigin": "https://{portal-domain}.powerappsportals.com"
  }
}
```

### Integration Points
- CCPay transaction is initiated from the portal submission flow (typically after a review step)
- A Power Automate flow or Azure Function orchestrates the CCPay API call
- On successful payment, the submission record is updated in Dataverse and the user is redirected to a confirmation page
- On failure, an appropriate error page is shown

### Environment Separation
- Provide separate `X-IBM-Client-Id`, `X-IBM-Client-Secret`, and endpoint for each environment (DEV, SIT, UAT, PROD)
- Store credentials in environment variables (not hardcoded)

---

## Moneris Integration

Moneris is a commercial payment processor used for non-government programs.

### Key Resources
- [Moneris Developer Documentation](https://developer.moneris.com/Documentation/NA/E-Commerce%20Solutions/API)

### Integration Approach
- Use Moneris Hosted Pay Page (HPP) or Direct API integration depending on PCI compliance requirements
- Moneris credentials and API keys stored in environment variables
- Integration orchestrated via Power Automate or Azure Function (same pattern as CCPay)

---

## General Payment Flow Pattern

```
Portal User -> Review Step -> Initiate Payment
  -> Redirect to Payment Processor (or embedded iFrame)
  -> User enters payment details
  -> Processor -> Callback/webhook to portal backend
  -> Backend updates Dataverse record (payment status, transaction ID)
  -> Redirect user to Confirmation Page
```

## Related
- [Pattern - Portal Submission](portal-submission.md) — submission flow where payment is integrated
- [Pattern - Malware Protection](malware-protection.md) — if attachments accompany the payment submission
- [dv-solution-design] — Dataverse record updates triggered by payment callbacks
