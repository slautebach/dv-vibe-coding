# MNP Table & Attribute Naming Standards

Source: `wiki/Welcome/Platform-Delivery-Playbook/Implementation-Standards/Using-Model-Driven-Apps/Table-&-Attribute-Standards.md`

## Table Standards

| Property | Rule |
|---|---|
| **Logical Name** | `{prefix}_{genericterm}` — use generic, reusable terms. Use `mnp_registration` NOT `mnp_buildingregistration` |
| **Display Name** | Business-user-facing label |
| **Description** | Always required — concise purpose statement |
| **Record Ownership** | Default: **User or Team**. Use **Organization** only for global static reference/lookup tables (e.g., Province, States) |
| **Auditing** | Always **ON**. If client declines, disable at Global Auditing settings in PROD only |

## Attribute Standards

| Property | Rule |
|---|---|
| **Logical Name** | Generic terms, no project-specific names. Use `mnp_registrationno` NOT `mnp_bcinno` |
| **Do NOT repeat table name** | Use `mnp_type` NOT `mnp_registrationtype` |
| **Display Name** | Business-user-facing label |
| **Description** | Always required |
| **Auditing** | Always **ON** |

## Data Type Naming Rules

### Lookup Fields
- Pattern: `{prefix}_{relatedtable}id`
  - `mnp_contactid` — lookup to `contact`
  - `mnp_accountid` — lookup to `account`
- Multiple lookups to same table: add context prefix `{prefix}_{context}{relatedtable}id`
  - `mnp_billingaccountid` — billing context
  - `mnp_shippingaccountid` — shipping context
- Lookup to SystemUser: `{prefix}_{action}by` (append **By** suffix)
  - `mnp_approvedby`, `mnp_submittedby`

### DateTime Fields
- Always use `on` suffix: `{prefix}_{action}on`
  - `mnp_submittedon` — date/time it *was* submitted
  - `mnp_submiton` — date/time it *needs to be* submitted

### Currency Fields
- Always use `amount` suffix: `{prefix}_{field}amount`
  - `mnp_grantamount` NOT `mnp_grant`

### Boolean Fields
- Always use `is` prefix: `{prefix}_is{field}`
  - `mnp_isapproved` NOT `mnp_approved`
- Use only when Null is not an option (binary yes/no)

### Option Set Fields
- Always use **global** option sets
- Warn if local option sets are proposed

## Grouping Tags

Use `{prefix}_{tag}_{field}` to group related attributes on a table that isn't itself about that concept:

- `mnp_loan_terminmonths`, `mnp_loan_interestrate`, `mnp_loan_startson` — loan attributes on a Payment table
- `mnp_portal_name` — portal-facing record name
- `mnp_portal_name_fr` — French portal name
- `mnp_name_fr` — French version of a record name (use `_fr` suffix for French variants)

## Behaviour Rules

- **No behaviour tags** in logical names (reduces flexibility to change behaviour)
  - Use `mnp_approvedamount` NOT `mnp_approvedamount_calc`
- **Avoid acronyms** in logical names

## Validation Checklist

Before creating any entity/attribute, verify:

- [ ] Logical name uses generic terms (not project-specific)
- [ ] Table name NOT repeated in attribute logical name
- [ ] Lookup uses `id` suffix (or `by` for SystemUser)
- [ ] DateTime uses `on` suffix
- [ ] Currency uses `amount` suffix
- [ ] Boolean uses `is` prefix
- [ ] Option sets are global (not local)
- [ ] No `_calc` or behaviour suffixes
- [ ] Description provided
- [ ] Auditing will be enabled
