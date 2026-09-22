# Spec: Profile Page Backend

## Overview
The profile page currently uses hardcoded demo data to showcase the UI. This feature replaces that static data with real-time information fetched from the database for the currently logged-in user. It transforms the profile page from a static mockup into a functional dashboard showing the user's actual spending habits.

## Depends on
- User Authentication (Step 02/03)
- Database Schema (Users and Expenses tables)

## Routes
- `GET /profile` — Fetches real user data, total spending, transaction history, and category breakdowns — access level: logged-in.

## Database changes
No database changes. The existing `users` and `expenses` tables are sufficient.

## Templates
- **Modify:** `templates/profile.html` — Update to use dynamic variables passed from the route instead of the current hardcoded structure (though the variable names should remain consistent to minimize HTML changes).

## Files to change
- `app.py` — Update the `/profile` route to call new database helper functions.
- `database/db.py` — Add helper functions to fetch user statistics and expenses.

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
- Ensure `get_db()` is used for all database connections to maintain foreign key enforcement.

## Definition of done
- [ ] Logged-in user sees their actual name and email on the profile page.
- [ ] "Total Spent" accurately reflects the sum of the user's expenses in the DB.
- [ ] "Transaction Count" matches the number of entries for that user.
- [ ] "Top Category" correctly identifies the category with the highest total spend.
- [ ] The transaction list displays the user's actual expenses from the database.
- [ ] The category breakdown accurately calculates the amount and percentage per category.
- [ ] A user with no expenses sees zeroed stats and an empty transaction list without crashing.
