# Spec: Add Expense

## Overview
This feature allows logged-in users to record new expenses. It provides a form to input the amount, category, date, and an optional description, ensuring users can track their spending in real-time.

## Depends on
- Step 01: User Registration
- Step 02: User Login/Logout

## Routes
- `GET /expenses/add` — Renders the "Add Expense" form — logged-in
- `POST /expenses/add` — Processes the form submission and saves the expense to the DB — logged-in

## Database changes
No database changes. The `expenses` table already contains the necessary columns: `user_id`, `amount`, `category`, `date`, and `description`.

## Templates
- **Create:** `templates/add_expense.html`
- **Modify:** `templates/base.html` (Ensure navigation to "Add Expense" is present if applicable)

## Files to change
- `app.py`: Implement the `GET` and `POST` handlers for `/expenses/add`.
- `database/db.py`: Add a helper function `add_expense(user_id, amount, category, date, description)` to handle the insertion.

## Files to create
- `templates/add_expense.html`: The form for adding a new expense.
- `static/css/expenses.css`: (Optional) Page-specific styles for the expense form.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate that the amount is a positive number.
- Ensure the date is in a valid YYYY-MM-DD format.
- Categories should be restricted to the set defined in `seed_db()`: ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"].

## Definition of done
- [ ] Logged-in user can access `/expenses/add` and see a form.
- [ ] Non-logged-in user is redirected to `/login` when accessing `/expenses/add`.
- [ ] Form submission with valid data successfully saves an expense to the database.
- [ ] Form submission with invalid data (e.g., negative amount, missing required fields) shows an error message.
- [ ] After successful addition, the user is redirected to the profile page where the new expense is visible.
- [ ] The expense is correctly linked to the `user_id` of the currently logged-in session.
