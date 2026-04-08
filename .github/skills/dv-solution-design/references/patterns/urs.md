# Pattern: Universal Resource Scheduling (URS)

**References:**
- https://learn.microsoft.com/en-us/dynamics365/field-service/universal-resource-scheduling-for-field-service
- https://learn.microsoft.com/en-us/dynamics365/common-scheduler/schedule-anything-with-universal-resource-scheduling

## WHY?

- Reuse native D365 scheduling features to meet business requirements
- Reduce complexity of custom development
- Leverage Microsoft investments and ongoing improvements

## Key Components

| Component | Description |
|---|---|
| **Bookable Resource** | Anything that can be scheduled: person, equipment, facility, account, contact |
| **Resource Requirement** | The "ask" for a resource -- defines duration, skills, location, time constraints. URS matches requirements to available resources. |
| **Organizational Units** | Business groups/cost centers used to group resources by department, location, or billing rate |
| **Bookable Resource Booking** | The confirmed assignment of a resource to a time slot -- the result of fulfilling a requirement |
| **Business Closures** | Org-wide dates/times when scheduling is blocked (statutory holidays, closures) |
| **Security Model** | Security roles controlling who can create/read/update/delete URS entities |

## Configuration Setup Order

> These are admin/config records created once to stand up the system, not per-transaction records.

1. **Security Model** -- define and assign security roles first; everything else depends on who can create/read/write URS records
2. **Organization Units** -- bookable resources reference them; set up before creating resources
3. **Business Closures** -- define statutory holidays and closure dates before resources go live
4. **Bookable Resource** -- create facility/person resources referencing the org unit; set working hours
5. **Resource Requirement Template** -- define defaults so each new request creates a consistent requirement record
6. **Bookable Resource Booking** -- only created at runtime after a requirement exists and availability is confirmed

---

## Sub-Pattern: Book a Timeslot

### WHY?

For scenarios where there are predefined timeslots a user/client can book -- e.g. appointments, venue reservations. The system must ensure one-and-only-one booking per timeslot.

### Design

Uses standard URS tables with pre-created "Open" bookings.

#### Daily Flow: Create Bookable Resource Bookings

- Runs daily to create `Bookable Resource Booking` records with **Booking Status = Open**
- Use an Environment Variable or custom table to store timeslot preferences (e.g. 9am, 11am, 1pm with durations)
- Create bookings N days into the future (e.g. 60 days)
- Use a **Child Flow** per resource type (Ceremonies, Appointments, Events) for readability

#### Optional: M365 Shared Calendar Integration

- Use Outlook connector to create a corresponding Calendar Event
- Store `EventId` on the Bookable Resource Booking for conflict detection/reconciliation

#### Optional: Conflict Detection Flow (Daily)

`Daily - Bookable Resource Bookings - Conflict Detection`

- For each Bookable Resource Booking, check the M365 Shared Calendar for conflicts via Outlook connector
- If the related Calendar Event is missing or cancelled, update the Booking status to "Cancelled"
- **Note:** Deletion of Bookable Resource Bookings is not supported by Flow -- use status changes instead
