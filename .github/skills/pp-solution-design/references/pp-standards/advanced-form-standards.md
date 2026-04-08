# Advanced Form Standards

Wiki source: `wiki/Welcome/Platform-Delivery-Playbook/Implementation-Standards/Using-PowerPages/Advanced-Form-Standards.md`

> **Note:** This standards page is currently a stub in the wiki. Guidance below is synthesized from MNP Power Pages conventions and Microsoft Power Pages documentation.

## WHY?
Advanced Forms (previously "Web Forms") support multi-step portal submissions where a single record is created/updated across multiple pages. Use them for complex workflows that exceed what a single Basic Form can handle.

## Naming Convention

`{Solution} - {Table} - {Action} - {Step Description}` (for individual steps)

Or name the Advanced Form overall:

`{Solution} - {Table} - {Workflow Name}`

**Examples:**
- `QUARTS - Application - Submit`
- `QUARTS - Application - Submit - Step 1: Applicant Info`
- `QUARTS - Application - Submit - Step 2: Project Details`

## Advanced Form Steps (Tabs/Steps)

- Each step maps to a **Basic Form** (same configuration conventions as Basic Form Standards)
- Define step **sequence** and **branching conditions** in Advanced Form Steps
- Use **Previous** button to allow backward navigation
- Store data to Dataverse on each step save (do not buffer in session only)

## Query String Parameters
- Same 2-3 char parameter conventions as Basic Forms
- Pass the primary record GUID through steps via query string (`apid`, `aid`, etc.)

## Step Branching
- Use **Condition** metadata on steps to branch based on field values (e.g., skip steps based on application type)
- Conditions evaluate against the record stored in Dataverse

## Custom JavaScript
- Same guidance as Basic Form Standards: use `$(document).ready(function() { ... })` and `mnp_common.js` helpers
- Add step-specific JS in the **Custom JavaScript** field of each step's associated Basic Form

## Success/Completion
- On the final step, redirect to a **Confirmation page** (not back to a form step)
- Trigger email notification via Power Automate or real-time workflow on final record status update

## Related
- [Basic Form Standards](basic-form-standards.md)
- [Pattern - Portal Submission](../patterns/portal-submission.md)
- [Component - mnp_common.js](../components/mnp-common-js-portal.md)
