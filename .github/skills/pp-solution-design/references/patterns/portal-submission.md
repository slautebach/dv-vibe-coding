# Pattern - Portal Submission

Wiki source: `wiki/Welcome/Platform-Delivery-Playbook/Solution-Design/Pattern-%2D-Portal-Submission.md`

> **Note:** This pattern page is currently a stub in the wiki. The guidance below synthesizes MNP standards from related patterns (authentication, web templates, basic/advanced form standards).

## WHY?

A consistent portal submission pattern ensures:
- Citizens and external users can submit data securely through Power Pages forms
- Multi-step submissions preserve state across pages
- Anonymous and authenticated flows are handled uniformly
- Submissions are reliably persisted to Dataverse with proper ownership assignment

## Submission Flow Types

| Flow Type | Description | Use When |
|---|---|---|
| **Anonymous** | User submits without logging in | Low-sensitivity intake; no account required |
| **Authenticated** | User must log in before submitting | Personalized dashboard, record ownership, re-entry |
| **Anonymous → Authenticated** | User starts anonymously, authenticates to save/resume | Progressive engagement; reduce friction for first-time users |
| **Invitation-based** | User receives reference number and redeems to claim a pre-created record | Internal staff pre-creates records; invites external users |

## Design Guidance

### Page Structure
- Use **Advanced Forms** (multi-step) for complex, multi-page submissions
- Use **Basic Forms** for single-page create/edit/review
- Group related pages under a common partial URL prefix:
  - `/application/` — summary/dashboard
  - `/application/add` — create new
  - `/application/edit` — edit in progress
  - `/application/review` — review before submit
  - `/application/confirmation` — success/confirmation

### Record Ownership
- For authenticated flows: use **Basic Form Metadata** → set `regardingobjectid` or owner field to **Current Portal User** on save
- For anonymous flows: link record to a system account or use the invitation/redeem pattern for later ownership transfer

### Confirmation and Email Notification
- Always redirect to a **Confirmation page** on successful submission
- Trigger a **Power Automate cloud flow** or **real-time workflow** on record create to send a confirmation email
- See [Pattern - Email Notification] for email standards

### Multi-step (Advanced Form) Submission
- Each step maps to a separate Basic Form
- Use **Advanced Form Steps** to define step sequence and branching
- Store intermediate data in Dataverse as the user progresses (auto-save per step)
- Use the **Previous** button and step branching conditions for complex flows

## Related Patterns
- [Pattern - Portal Authentication] — securing submission flows
- [Pattern - Redeem Invitation] — ownership transfer after anonymous submission
- [Pattern - Malware Protection] — scanning attachments on submission
- [Advanced Form Standards](../pp-standards/advanced-form-standards.md)
- [Basic Form Standards](../pp-standards/basic-form-standards.md)
