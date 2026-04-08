# Component: CRM Client API JavaScript Libraries

**Source:** https://dev.azure.com/MNPDigital/DC-Delivery/_git/DC-StarterKits_Solution?path=/SharedLibraries/ClientAPI

## Overview

Four shared JavaScript libraries for Dynamics 365 Model-Driven App form scripting. Always pass `executionContext` as the first parameter. Reference via `mnp_common.library.js` web resource.

---

## mnp_Common.FormHelpers.js

Utilities for controlling form fields, tabs, sections, option sets, lookups, and notifications.

### Constants

| Constant | Description |
|---|---|
| `CRM_FORM_TYPE_CREATE` | Create form type |
| `CRM_FORM_TYPE_UPDATE` | Update form type |
| `CRM_FORM_TYPE_READONLY` | Read-only form type |
| `CRM_FORM_TYPE_DISABLED` | Disabled form type |
| `CRM_FORM_REQUIREDLEVEL_NONE` | Field required level: none |
| `CRM_FORM_REQUIREDLEVEL_REQUIRED` | Field required level: required |
| `CRM_FORM_REQUIREDLEVEL_RECOMMENDED` | Field required level: recommended |
| `CRM_FORM_SUBMITMODE_ALWAYS` | Field submit mode: always |
| `CRM_FORM_SUBMITMODE_NEVER` | Field submit mode: never |
| `CRM_FORM_SUBMITMODE_DIRTY` | Field submit mode: dirty |

### Functions

| Function | Signature | Description |
|---|---|---|
| `enableBusinessProcessFlow` | `(executionContext, businessProcessFlowName)` | Enable a specific BPF on the form |
| `disableEnableField` | `(executionContext, fieldName, isDisable)` | Disable or enable a field |
| `showHideField` | `(executionContext, fieldName, isShow)` | Show or hide a field |
| `hideFieldIfEmpty` | `(executionContext, fieldName)` | Hide a field if it has no value |
| `getFieldValue` | `(executionContext, fieldName)` | Get a field's value |
| `setFieldValue` | `(executionContext, fieldName, value)` | Set a field's value |
| `getFieldLabel` | `(executionContext, controlName)` | Get a field's label |
| `setLabel` | `(executionContext, controlName, value)` | Set a field's label |
| `showHideSection` | `(executionContext, tabName, sectionName, isShow)` | Show or hide a section |
| `showHideTab` | `(executionContext, tabName, isShow)` | Show or hide a tab |
| `showHideNavItemByItemId` | `(executionContext, navItemId, isShow)` | Show or hide a nav item by ID |
| `showHideNavItemByName` | `(executionContext, navName, isShow)` | Show or hide a nav item by name |
| `setRequired` | `(executionContext, fieldName, requiredLevel)` | Set required level using `CRM_FORM_REQUIREDLEVEL_*` constants |
| `setSubmitMode` | `(executionContext, fieldName, mode)` | Set submit mode using `CRM_FORM_SUBMITMODE_*` constants |
| `getSubmitMode` | `(executionContext, fieldName)` | Get the submit mode of a field |
| `autoSubmitMode` | `(executionContext, fieldName)` | Force a disabled field to always submit |
| `isDisabled` | `(executionContext, fieldName)` | Returns whether a field is disabled |
| `getFormType` | `(executionContext)` | Returns the current form type |
| `closeForm` | `(executionContext)` | Closes the form |
| `getOptionSetText` | `(executionContext, controlName)` | Get the text value of an option set |
| `getOptions` | `(executionContext, fieldName)` | Return all options in an option set |
| `removeOption` | `(executionContext, controlName, value)` | Remove an option from an option set |
| `clearOptions` | `(executionContext, fieldName)` | Clear all options from an option set |
| `addOption` | `(executionContext, controlName, option)` | Add an option: `{ text: "Label", value: 123 }` |
| `setLookupValue` | `(executionContext, fieldName, id, name, entityType)` | Set a lookup field value |
| `getLookupId` | `(executionContext, fieldName)` | Get the GUID from a lookup field |
| `getEntityId` | `(executionContext)` | Get the current entity record ID |
| `setFocus` | `(executionContext, fieldName)` | Set focus on a field |
| `lockEditableGrid` | `(executionContext)` | Lock all fields in an editable grid |
| `lockFieldsonEditableGrid` | `(executionContext, disableFields[])` | Lock specific fields in an editable grid |
| `getClientUrl` | `(executionContext)` | Get the server URL |
| `validateStartAndEndDate` | `(executionContext, startdate, endDate)` | Validate start date is before end date |
| `disableAllFields` | `(executionContext)` | Lock all fields on the form |
| `formRedirect` | `(executionContext, requiredFormName)` | Redirect to another form by name |
| `lockFieldIfPopulated` | `(executionContext, fieldName)` | Lock a field if it has a value |
| `mandatoryFieldIfPopulated` | `(executionContext, fieldName)` | Make a field mandatory if it has a value |
| `disableFieldsInTab` | `(executionContext, tabName)` | Disable all fields in a tab |
| `setCurrencyFieldsZero` | `(executionContext, fields[])` | Default currency fields to 0 |
| `showAndMakeFieldMandatory` | `(executionContext, fieldName)` | Show and make a field mandatory |
| `clearAndHideField` | `(executionContext, fieldName, clearRequiredLevel?)` | Hide and clear a field (default clears required level) |
| `checkDateTime` | `(executionContext, dateField, condition)` | Validate date: condition = `"PASTONLY"` or `"FUTUREONLY"` |
| `recordIsActive` | `(executionContext)` | Check if the current record is active |
| `setValueInLockedField` | `(executionContext, fieldName, value)` | Unlock, set value, relock a field |
| `setToday` | `(executionContext, dateField, createOnly?)` | Set date to today (createOnly default: true) |
| `showFormNotification` | `(executionContext, messageid, message, level)` | Show notification: level = `"ERROR"`, `"WARNING"`, `"INFO"` |
| `clearFormNotification` | `(executionContext, messageid)` | Clear a form notification by ID |

---

## mnp_Common.Security.js

Role-based security helpers for form scripting.

| Function | Signature | Description |
|---|---|---|
| `currentUserRoles` | `()` | Returns the list of security roles the current user has |
| `hideFieldsByRoles` | `(executionContext, hideFromRoles[], targetFields[])` | Hide fields if the user has any of the specified roles |
| `currentUserHasRole` | `(roleName, roles?)` | Check if the user has a given role; optionally pass a roles array |

---

## mnp_Common.Translations.js

Centralized label/translation management for bilingual (EN/FR) forms.

| Item | Description |
|---|---|
| `translationEnabled` (variable) | Check this before calling translation functions to see if the library is loaded |
| `getLabel(key, lcid)` | Returns the translated label for the given key and LCID (language code) |

---

## mnp_Common.Utilities.js

General-purpose utilities.

| Function | Signature | Description |
|---|---|---|
| `calculateAge` | `(birthDate, compareDate)` | Calculate age in years between two dates |
| `isBetween` | `(num, lower, upper)` | Check if a number is between two values |
| `GetEnvironmentVariableDefaultValue` | `(name)` | Retrieve the default value of an Environment Variable |
| `GetEnvironmentVariableValue` | `(name)` | Retrieve the current value of an Environment Variable |
| `showAlertDialog` | `(alertStrings, success, fail)` | Show an alert dialog; `alertStrings = { text, title?, confirmButtonLabel? }` |
| `showConfirmDialog` | `(confirmStrings, success, fail)` | Show a confirm dialog; success callback has `confirmed` property |
| `showErrorDialog` | `(message, errorcode, error, success, fail)` | Show an error dialog with error code and details |
