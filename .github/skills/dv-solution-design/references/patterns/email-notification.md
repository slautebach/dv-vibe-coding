# Pattern: Email Notification

## WHY?

Provides an extensible email notifications framework to:
- Change content without deactivating workflows
- Reuse email templates across multiple scenarios/triggers
- Globally action the email notification

## Applications

- **External notifications:** email when portal submission, email when balance goes below threshold
- **Internal notifications:** email when a specific threshold/condition is met

## Implementation Guide

### 1. Create Email Templates

- Always create as **Organization-scoped** Email Templates
- Naming: `{Solution} - {Template}` (groups and identifies solution-specific templates)
- Example: `Grants - Form Submitted`

### 2. Create a Global Action to Send the Email

See [Action Standards](../mda-standards/action-standards.md) for details.

- **Naming:** `Email - {Template} - Action - MNP`
  - Example: `Email - Form Submitted - Action - MNP`
- Set **Entity = None** to make the Action global
- Add an **Input Parameter** of type `EntityReference` for the entity used to create the email message
- Add steps to validate if the Email Address is populated
- Use the **Email Template** step to send the email
- Send **From** the Service Account

### 3. Call the Action from a Workflow

Call `Email - {Template} - Action - MNP` from the relevant Create/Update/Delete workflow.

This decouples the notification logic: if the email template changes, only the Action needs updating -- not every workflow that triggers it.
