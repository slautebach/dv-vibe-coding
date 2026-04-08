# Basic Form Standards

Wiki source: `wiki/Welcome/Platform-Delivery-Playbook/Implementation-Standards/Using-PowerPages/Basic-Form-Standards.md`

## WHY?
To be consistent with Power Pages basic form implementation and to standardize parameters, code, metadata, and layout.

## Naming Convention

`{Solution} - {Table} - {Action}`

| Part | Purpose | Example |
|---|---|---|
| `{Solution}` | Distinguishes from other solutions' forms | `QUARTS` |
| `{Table}` | Source table for the form | `Organization` |
| `{Action}` | Purpose or mode | `Create`, `Update`, `Review` |

**Examples:**
- `QUARTS - Organization - Create` — creates an Organization record
- `QUARTS - Organization - Update` — updates an Organization record using `ai=` query string parameter

## CRM Form Setup

- Create a **separate CRM Form** for the portal (isolates from Model-Driven App form)
- Create a **separate Tab** for this Basic Form; name the tab the same as the Basic Form
- **Tab naming**: `{Solution}_{Table}_{Action}`
- **Hide Tab Labels** (use Classic UI if needed)
- **Hide Section Labels** (use Classic UI if needed)
- CRM Form naming: `Portal - {Table}`

## Record Source Type and Query String Parameters

| Mode | Record Source Type | Parameter Naming |
|---|---|---|
| **Insert** | Query String | Parent/related record IDs in query string |
| **Edit** | Query String | Use 2-3 char param: `aid` for AccountId, `mid` for MunicipalityId |
| **Read Only** | Query String | Same 2-3 char param convention |

Parameter convention: 2-3 lowercase characters derived from the table name:
- `aid` → **A**ccount **Id**
- `mid` → mnp_**M**unicipality **Id**
- `apid` → **Ap**plication **Id**

## Custom JavaScript

Place all form JavaScript in the **Custom JavaScript** field of the Basic Form:

```javascript
$(document).ready(function() {
  // Field masking
  setPostalCodeMask('mnp_postalcode');
  setTelephoneMask('mnp_telephone1');

  // Validation
  ValidateTwoOptionField('mnp_termsaccepted', 'You must accept the terms.');

  // Show/Hide
  MakeRequired('mnp_firstname');
  pretendDisabledOn('#mnp_status');

  // Web API
  apiUpdate('mnp_application', recordId, { mnp_status: 120310001 });
});
```

- Use `mnp_common.js` helper functions (masks, validators, show/hide, Web API calls)
- For forms with Subgrids: apply JS customizations **after the subgrid has loaded**

## Basic Form Metadata

### Subgrid
- Use the **same View** for both **View Details** and **Edit** to enable the default link to open selection in Edit Form
- Use **Filter Criteria** to show/hide View and Edit actions
- **NOTE:** Filter Criteria for **Create** and **Associate/Disassociate** do **NOT** work

## Organizational Tip
Create a **personal view** in the Portal Management App to filter solution-specific Basic Forms.

## Related
- [Advanced Form Standards](advanced-form-standards.md)
- [Web Template Standards](web-template-standards.md)
- [Component - mnp_common.js](../components/mnp-common-js-portal.md)
