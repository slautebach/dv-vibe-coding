# Component - mnp_common.js (Portal)

Wiki source: `wiki/Welcome/Platform-Delivery-Playbook/Solution-Design/Component-%2D-mnp_common.js-(Portal).md`

Source code: [mnp_common.js in Git](https://dev.azure.com/MNPDigital/DC-Delivery/_git/DC-Delivery?path=/Accelerator/Portal/ODS%20Portal/web-files/mnp_common.js)

Loaded automatically from the `Head/Bottom` content snippet on all portal pages (part of the ODS Accelerator).

## Table of Contents
- [Web API](#web-api)
- [Field Visibility and State](#field-visibility-and-state)
- [Section Visibility](#section-visibility)
- [Validation and Masks](#validation-and-masks)
- [Date Validators](#date-validators)
- [Utility Functions](#utility-functions)
- [Session Timeout](#session-timeout)

---

## Web API

### `apiUpdate(entity, id, updates)`
Updates a Dataverse table record using Web API (HTTP PATCH).
- `entity` — logical name of the entity
- `id` — GUID of the record
- `updates` — JSON object with field values (standard Web API format)
- See: [Power Pages Web API how-to](https://learn.microsoft.com/en-us/power-pages/configure/webapi-how-to)

---

## Field Visibility and State

### `MakeRequired(fieldName, bookmark)`
Makes a field required. `bookmark` (optional) — alternate field name for validation summary.

### `MakeNotRequired(fieldName)`
Removes required validators from a field.

### `MakeDisabled(fieldName)`
Makes a field read-only (same as Read Only on CRM Form). Use `pretendDisabledOn()` instead where possible.

### `MakeEnabled(fieldName)`
Enables a field for editing.

### `pretendDisabledOn(id)`
Simulates disabled appearance (adds `.pretend-disabled` class, blocks keyboard input except Tab). Allows JS to still update the value.

### `pretendDisabledOff(id)`
Removes the pretend-disabled simulation.

### `showAttribute(id)` / `hideAttribute(id)`
Show/hide an attribute control by CSS selector.

### `showAttribute_info(id)` / `hideAttribute_info(id)`
Show/hide the info line of an attribute control.

### `showAttribute_control(id)` / `hideAttribute_control(id)`
Show/hide the input element of an attribute control.

### `showAttribute_description(id)` / `hideAttribute_description(id)`
Show/hide the description line of an attribute control.

### `showAttributeRow(id)` / `hideAttributeRow(id)`
Show/hide the entire table row (`<tr>`) containing an attribute control.

### `setDescription(id, content)`
Sets the description line HTML content of an attribute control.

---

## Section Visibility

### `showSection(sectionName)` / `hideSection(sectionName)`
Show/hide an entire form section.

### `setSectionTitle(sectionName, title)`
Updates the title of a form section.

### `setSectionIntro(sectionName, content)`
Updates the content below the section title.

---

## Validation and Masks

### `ValidateTelephone(controlName)`
Validates North American telephone format. Use `setTelephoneMask()` instead (sets mask + validates).
- Pattern: `(999) 999-9999 x9999`

### `ValidateTelephoneExtension(controlName)`
Validates telephone extension (4 digits). Recommend not separating telephone and extension into 2 fields.

### `ValidatePostalCode(controlName)`
Validates Canadian postal code format. Use `setPostalCodeMask()` instead.
- Pattern: `H0H 0H0`

### `ValidateTwoOptionField(fieldName, errormessage)`
Validates a Boolean/Two-Option field has been set to True/1.

### `CreateValidation(fieldName, regex)`
Creates a custom regex validator. Calls `regex.test(controlName.val())`.

### `RemoveValidator(validatorId)`
Removes a validator by its ID. Inspect form HTML to find the validator ID.

### `makeRequiredForRadioButtonListField(fieldname)`
Makes an option-set field rendered as radio buttons required.

### `setValueForRadioButtonListField(fieldname)`
Sets the value of an option-set field rendered as radio buttons.

### `clearMask(fieldname)` 
Clears the input mask for a field.

### `setPostalCodeMask(fieldname)`
Sets Canadian postal code mask (`A9A 9A9`) and validator.

### `setZipCodeMask(fieldname)`
Sets US zip code mask (`99999`) and validator.

### `setMobilePhoneMask(fieldname)` / `setFaxPhoneMask(fieldname)` / `setTelephoneMask(fieldname)`
Sets phone number masks and validators. Telephone mask: `(999) 999-9999 x99999`.

### `formatCurrency(selector)` / `formatCurrencyDollarsOnly(selector)`
Formats a field as CAD currency (`en-ca`). Dollars-only variant ignores decimals.

### `parseCurrency(currency)`
Returns a Number from a currency-formatted string. Example: `"$22,231.03"` → `22231.03`.

### `AutoResizeAllTextarea()`
Adjusts height of all textarea controls to fit content.

---

## Date Validators

### `CreateStartEndDateValidator(startControlName, endControlName, message)`
Validates start date is before or equal to end date.

### `CreatePastDateValidator(controlName, message)`
Validates date is in the past.

### `CreatePastAndNowDateValidator(controlName, message, bookmark)`
Validates date is in the past or today.

### `CreatePastOrCurrentYearValidator(controlName, message)`
Validates date is in the current year or earlier.

### `CreateFutureDateValidator(controlName, message)`
Validates date is in the future.

### `setNow(fieldname)`
Sets a date picker field to the current date/time.

---

## Utility Functions

### `getQueryStringParameterValues(param)`
Returns the value of a query string parameter.
- Example: `?id=1288282&uid=12938372` → `getQueryStringParameterValues('uid')` returns `12938372`

---

## Session Timeout

### `initTimeouts()`
Initializes session timeout warning and message timers.
- Warning modal (Timeout Warning content snippet) fades in at **13 minutes** of inactivity
- Session expired modal (Timeout Message content snippet) fades in at **15 minutes** of inactivity

Call from the **Tracking Code** content snippet:
```javascript
$(document).ready(function() { initTimeouts(); });
```

---

## Usage in Basic Forms

Always wrap JavaScript in:
```javascript
$(document).ready(function() {
  // mnp_common.js functions available here
  setPostalCodeMask('mnp_postalcode');
  MakeRequired('mnp_firstname');
  pretendDisabledOn('#mnp_status');
});
```

For forms with subgrids, apply customizations after the subgrid has loaded.
