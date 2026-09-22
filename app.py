from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db, create_user, get_user_by_email, get_user_by_id
import sqlite3

app = Flask(__name__)
app.secret_key = "spendly_secret_key_for_development"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.context_processor
def inject_user():
    user = None
    if session.get("user_id"):
        user = get_user_by_id(session["user_id"])
    return dict(current_user=user)

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not name or not email or not password or not confirm_password:
            flash("All fields are required.", "error")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("register.html")

        hashed_password = generate_password_hash(password)

        try:
            create_user(name, email, hashed_password)
            session["user_id"] = get_user_by_email(email)["id"]
            flash("Account created successfully! Welcome to Spendly.", "success")
            return redirect(url_for("profile"))
        except sqlite3.IntegrityError:
            flash("An account with this email already exists.", "error")
            return render_template("register.html")
        except Exception as e:
            flash("An unexpected error occurred.", "error")
            return render_template("register.html")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Email and password are required.", "error")
            return render_template("login.html")

        user = get_user_by_email(email)
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            flash("Welcome back!", "success")
            return redirect(url_for("profile"))

        flash("Invalid email or password.", "error")
        return render_template("login.html")

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    # Hardcoded data for Step 4 UI design
    user = {
        "name": "Demo User",
        "email": "demo@spendly.com",
        "member_since": "September 2026",
        "initials": "DU"
    }
    stats = {
        "total_spent": "₹ 2,450.00",
        "transaction_count": 12,
        "top_category": "Food"
    }
    transactions = [
        {"date": "2026-09-20", "desc": "Grocery Store", "cat": "Food", "amt": "₹ 450.00"},
        {"date": "2026-09-18", "desc": "Uber Ride", "cat": "Transport", "amt": "₹ 120.00"},
        {"date": "2026-09-15", "desc": "Netflix", "cat": "Entertainment", "amt": "₹ 499.00"},
        {"date": "2026-09-12", "desc": "Pharmacy", "cat": "Health", "amt": "₹ 300.00"},
    ]
    categories = [
        {"name": "Food", "amount": "₹ 1,200.00", "percent": 49},
        {"name": "Transport", "amount": "₹ 600.00", "percent": 24},
        {"name": "Entertainment", "amount": "₹ 650.00", "percent": 27},
    ]

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        transactions=transactions,
        categories=categories
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
