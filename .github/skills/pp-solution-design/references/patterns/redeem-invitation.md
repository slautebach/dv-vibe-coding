# Pattern - Redeem Invitation

Wiki source: `wiki/Welcome/Platform-Delivery-Playbook/Solution-Design/Pattern-%2D-Redeem-Invitation.md`

## WHY?

Allow a portal user to claim ownership of a pre-existing record using a **reference number** and **challenge answer** — similar to how Air Canada links a booking by Booking Reference + Last Name. Used when:
- An internal user pre-creates a case/record and invites the external user to take ownership
- An anonymous user creates a portal record, leaves the site, and returns later to complete it

## Applications

### Application 1: Anonymous User Resumes Their Own Submission
1. Anonymous user creates a new portal record (e.g., Case) and provides email/postal code as the Challenge Answer, then leaves before submitting
2. User receives a confirmation email with a reference number and redemption instructions
3. User returns to the **Redeem** page, enters the Reference # and Challenge Answer
4. On successful validation, user is redirected to continue updating the record

### Application 2: Internal Staff Pre-Creates and Invites External User
1. Internal user pre-creates a Case, sets the email address as the Challenge Answer
2. Internal user sends the portal user an email with the Case Number and challenge instructions
3. Portal user follows the Redemption URL, enters the Case Number
4. Portal user is redirected to the Confirmation page and enters the Challenge Answer
5. If valid, the Case is reassigned to the current portal user

## Implementation Guide

### 1. Portal Intake Record Fields
Add the following fields to the table being redeemed/reassigned:
- `mnp_number` (string) — unique reference number
- `mnp_challenge_answer` (string) — challenge answer (e.g., email address or postal code)
- `mnp_emailaddress` (string) — or other comparable field used as the challenge

### 2. CRM Form for Redeem Confirmation Web Page
- Display Reference No (read only)
- Add Challenge Answer field (relabelled to match the requested information, e.g., "Email Address", "Postal Code")

### 3. Redeem Confirmation Basic Form
- **Record Source Type:** Query String
- On success: redirect to a "My Dashboard" page to show the reassigned/redeemed record
- **Basic Form Metadata:**
  - Challenge Answer field: required
  - `AssignedTo` (or owner field): set **On Save Value** to **Current Portal User > contactid** — this reassigns the record on successful save

### 4. Validation Workflow (Real-Time)
Create a real-time workflow triggered on the redemption form save:
- If `mnp_challenge_answer != {expected answer}` → Stop Workflow with error: "Unable to process redemption."
- This prevents incorrect challenge answers from completing the redemption

### 5. Redeem Invitation Web Template
Handles the redemption flow logic in Liquid:

```
IF Reference No in queryString AND Portal Intake found AND unclaimed:
  -> Redirect to Redeem Confirmation Page (with ReferenceNo + Portal Intake GUID in queryString)
IF Reference No AND Portal Intake GUID in queryString:
  -> Let Basic Form handle the confirmation
OTHERWISE:
  -> Render HTML:
     - Input field for Reference No
     - Search button that redirects to itself with ReferenceNo in queryString
```

### 6. Web Pages
- **Redeem Page** (`../redeem`): uses the Redeem Invitation Page template as the landing page
- **Redeem Confirmation Page** (`../redeem/confirmation`): uses the Redeem Invitation Page template, assigns the Redeem Confirmation basic form

## Related
- [Pattern - Portal Authentication](portal-authentication.md)
- [Pattern - Portal Submission](portal-submission.md)
- [Basic Form Standards](../pp-standards/basic-form-standards.md)
