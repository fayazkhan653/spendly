---
# Spec: Login and Logout

## Overview
This feature implements the authentication flow for Spendly, allowing users to securely log into their accounts and log out. This is a critical step in the roadmap as it enables user-specific data access for the profile and expense tracking features that follow.

## Depends on
- Step 02: Registration (User accounts must exist to log in)

## Routes
- `GET /login` — Renders the login page — public
- `POST /login` — Authenticates user and starts session — public
- `GET /logout` — Ends the user session — logged-in

## Database changes
No database changes.

## Templates
- **Modify:** `login.html` — Ensure it has a POST form with `email` and `password` fields.
- **Modify:** `base.html` — Add conditional navigation links (e.g., show "Login" when logged out, "Logout" and "Profile" when logged in).

## Files to change
- `app.py` — Implement authentication logic and session management.
- `templates/base.html` — Update navigation for auth state.
- `templates/login.html` — Update for form submission.

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
- Use Flask `session` for maintaining user state.
- Ensure `check_password_hash` from `werkzeug.security` is used for verification.

## Definition of done
- [ ] User can successfully log in with a registered email and correct password.
- [ ] User is redirected to the landing page upon successful login.
- [ ] User sees an error message upon providing an incorrect password or non-existent email.
- [ ] User can log out, and the session is cleared.
- [ ] Navigation bar updates dynamically based on whether the user is logged in or not.
---
