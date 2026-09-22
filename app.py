from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db, create_user, get_user_by_email, get_user_by_id, get_user_expenses, get_user_stats, get_category_breakdown
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

    # Get user details
    user = get_user_by_id(session["user_id"])
    if not user:
        abort(404)

    # Format user data for template
    user_data = {
        "name": user["name"],
        "email": user["email"],
        "member_since": "September 2026", # Simplified for now
        "initials": user["name"][:2].upper() if user["name"] else "???"
    }

    # Get real user stats from DB
    user_stats = get_user_stats(session["user_id"])

    total = user_stats["total"]
    count = user_stats["count"]
    top_cat = user_stats["top_category"]

    stats = {
        "total_spent": f"₹ {total:.2f}" if total is not None else "₹ 0.00",
        "transaction_count": count if count is not None else 0,
        "top_category": top_cat if top_cat else "N/A"
    }

    # Get real expenses from DB
    expense_rows = get_user_expenses(session["user_id"])
    transactions = [
        {
            "date": row["date"],
            "desc": row["description"],
            "cat": row["category"],
            "amt": f"₹ {row['amount']:.2f}"
        }
        for row in expense_rows
    ]

    # Get category breakdown and total spend
    category_rows = get_category_breakdown(session["user_id"])
    overall_total = sum(row["total"] for row in category_rows)

    categories = [
        {
            "name": row["category"],
            "amount": f"₹ {row['total']:.2f}",
            "percent": int((row["total"] / overall_total) * 100) if overall_total > 0 else 0
        }
        for row in category_rows
    ]

    return render_template(
        "profile.html",
        user=user_data,
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
