# MDA Standards: Actions

## Design Guidance

- Use Actions to **centralize features/validations/rules** used across multiple tables or workflows (polymorphism)
  - Example: if an email notification is called from multiple workflows, centralizing to **one Action** reduces maintenance

## Naming

`{Action} - Action - MNP`

- No `{Table}` prefix -- Actions are meant to be global/polymorphic
- Example: `Email - Form Submitted - Action - MNP`
- Exception: if explicitly table-scoped, use `{Table} - {Action} - Action`

## Parameters

- When passing entities as parameters, use **EntityReference** type (not Entity)

## Owner

- Ensure the **Service Account** owns all Actions

## See Also

- [MNP.Base.Plugin Workflow Activities](../components/mnp-base-plugin.md) for available workflow activities to use inside Actions
- [Email Notification Pattern](../patterns/email-notification.md) for the standard email action pattern
