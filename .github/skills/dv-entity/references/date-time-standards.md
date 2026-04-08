# Date & Time Field Behavior Selection Standard

Source: `wiki/Welcome/Platform-Delivery-Playbook/Implementation-Standards/Using-Model-Driven-Apps/Date-&-Time-field-behavior-selection-standard.md`

## Quick Reference

| Business Need | Recommended Behavior |
|---|---|
| User interaction should reflect their local timezone (e.g., meeting times) | **User Local** |
| Only calendar dates are necessary (e.g., deadlines without time context) | **Date Only** |
| System integrations depend on fixed time calculations or UTC timestamps | **Time-Zone Independent** |

## Behavior Definitions

### User Local
- Stored in UTC, **dynamically displayed** in the user's local timezone based on their D365 settings
- Example: New York user (UTC-5) sees times adjusted; London user (UTC+0) sees different display

### Date Only
- Only the **date portion** stored and displayed — no time data, no timezone
- Example: "December 15, 2023" deadline without a specific time

### Time-Zone Independent
- Stored in UTC with **no conversion** applied at display time — raw stored value shown
- Example: API integration timestamp that must remain consistent across systems

## Decision Guide

| Use **User Local** when | Use **Date Only** when | Use **Time-Zone Independent** when |
|---|---|---|
| Users across timezones interact with dates/times | Only calendar date matters | System integrations need fixed UTC timestamps |
| Task/deadline views should be personalized | Time is irrelevant to the use case | Back-end processing or auditing logs |
| Meeting scheduling across regions | Birthdays, anniversaries, due dates | External API payloads |
| Reporting aligned to individual timezones | Date range reporting without time | High-volume cross-region reporting (UTC) |

## Best Practices

1. **User-facing solutions**: Prefer **User Local** for intuitive UX
2. **Integrations**: Use **Time-Zone Independent** for consistency across systems
3. **Pure-date business logic**: Use **Date Only** to avoid timezone confusion
4. **Document the choice** in design decisions for long-term maintainability
5. **Test User Local** across multiple timezones before go-live

## Naming Convention Reminder

DateTime attributes must use the `on` suffix per MNP attribute standards:
- `mnp_submittedon` — past action date
- `mnp_submiton` — future/target action date
- `mnp_approvedon`, `mnp_closedon`, `mnp_reviewedon`
