# Spec: Registration

## Overview
This feature implements the user registration process, allowing new users to create an account by providing their name, email, and password. This is a foundational step in the Spendly roadmap, enabling personalized expense tracking and secure data storage for each user. On success the user is shown with a success message and redirected to the login page. This is the entry point for all authenticated features that follow.

## Depends on
Step 1: Database Setup (Users and Expenses tables)

## Routes
- `GET /register` — Renders the registration form — public
- `POST /register` — Handles form submission, validates input, creates user account, and redirects to login — public

## Database changes
No database changes. The `users` table already exists with required fields (`name`, `email`, `password_hash`).

## Templates
- **Modify:** `templates/register.html` — Convert from a static placeholder to a functional form with appropriate `name` attributes for inputs and a POST method.

## Files to change
- `app.py` — Implement the `POST /register` route and update the `GET /register` route logic.
- `database/db.py` — Add a helper function to create a new user.
- `templates/register.html` — Update the HTML form.

## Files to create
No new files.

## New dependencies
No new dependencies. (Using `werkzeug.security` which is already a Flask dependency).

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`generate_password_hash`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate that the email is unique before inserting (handle `sqlite3.IntegrityError`)
- Use `flash()` messages to provide feedback to the user (success/error)

## Definition of done
- [ ] Navigating to `/register` renders the registration page.
- [ ] Submitting the form with valid data creates a new user in the `users` table.
- [ ] Passwords in the database are hashed, not plain text.
- [ ] Submitting a duplicate email results in an error message and the user remains on the registration page.
- [ ] Successful registration redirects the user to the login page with a success message.
- [ ] Form validation prevents empty submissions.
