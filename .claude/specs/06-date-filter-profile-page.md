# Spec: Date Filter for Profile Page

## Overview
This feature introduces a date range filter to the profile page, allowing users to view their spending habits and transactions for a specific period. Currently, the profile page shows all-time data; this update enables more granular analysis by filtering expenses and recalculating summary statistics based on the selected date range.

## Depends on
- 04-profile-page
- 05-profile-page-backend

## Routes
No new routes. The `GET /profile` route will be modified to accept optional `start_date` and `end_date` query parameters.

## Database changes
No database changes.

## Templates
- **Modify:** `templates/profile.html` — Add a date filter form (start date and end date inputs) and ensure the form submits via GET to the same page.

## Files to change
- `app.py` — Update the `profile` route to handle date filter parameters and pass them to DB helper functions.
- `database/db.py` — Update `get_user_expenses`, `get_user_stats`, and `get_category_breakdown` to support optional date range filtering.
- `templates/profile.html` — Add the UI for the date filter.

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Date inputs should use `type="date"` for native browser pickers.
- If no date range is provided, default to showing all expenses.

## Definition of done
- [ ] Profile page renders a date filter form with "Start Date" and "End Date" fields.
- [ ] Selecting a date range and submitting the filter updates the transaction list to only show expenses within that range.
- [ ] Total spent, transaction count, and top category statistics are recalculated based on the filtered date range.
- [ ] The category breakdown chart/list is recalculated based on the filtered date range.
- [ ] Clearing the filter or providing an empty range restores the view to all-time data.
- [ ] The page does not crash when provided with invalid date formats or ranges where start date is after end date (should ideally show no results or a helpful message).
