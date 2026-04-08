# MDA Standards: Messages

## WHY?

- Provides users with consistent messages
- Gives developers/analysts a consistent method to trace failing root objects

## Error Message Format

- Use the prefix **`ERROR:`**
- For portal-facing errors, use language appropriate for the portal audience
- **Avoid "You" or "Please" -- keep it concise**

### Examples

| Context | Format | Example |
|---|---|---|
| General | `ERROR: {description}. [{source}]` | `ERROR: Amount cannot be changed. [Project - Update]` |
| Plugin | `ERROR: {description} [{ClassName}.cs]` | `ERROR: This update is not allowed [Contact.cs]` |
| Workflow | `ERROR: {description} [{Workflow Name}]` | `ERROR: This update is not allowed [Contact - Update]` |

## Key Rules

- Always include the **source** (workflow name, plugin name) in brackets for traceability
- Plugin errors reference the `.cs` class name
- Workflow errors reference the workflow/action name
