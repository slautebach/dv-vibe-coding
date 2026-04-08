# Pattern: Payment Transaction

## Overview

Placeholder for logical payment transaction model. Two integration implementations are documented below.

---

## CCPay Integration (Ontario Government)

**Interface Spec:** https://ontariogov.sharepoint.com (internal -- CCPay_Interface_Specs.pdf)

### Environment Variable: `mnp_MappingConfig`

```json
{
  "CCPay": {
    "Endpoint": "https://ws.stage.gwy.apic.sus.gov.on.ca:443/ops/ops-partner/v1/ccpayrestservice",
    "X-IBM-Client-Id": "<client-id>",
    "X-IBM-Client-Secret": "<client-secret>",
    "Passphrase": "<passphrase>",
    "AllowedHttpRequestOrigin": "https://<your-portal>.powerappsportals.com"
  }
}
```

### Key Implementation Notes

- Store all CCPay credentials in an **Environment Variable** (JSON format) -- never hardcode
- `AllowedHttpRequestOrigin` must match the portal domain
- Use `RESTCallActivity` from MNP.Base.Plugin to call the CCPay endpoint from a Workflow/Action
- Test mode vs. production endpoints differ -- use separate environment variables per environment

---

## Moneris Integration

**Developer Reference:** https://developer.moneris.com/Documentation/NA/E-Commerce%20Solutions/API

### Implementation Notes

- Moneris provides REST APIs for e-commerce payment processing
- Integrate via Azure Function App or Logic App as a middleware layer
- Store API credentials in Environment Variables
- Follow the [External Integration pattern](external-integration.md) for the MDA-side UX (confirm dialog, spinner, polling)
