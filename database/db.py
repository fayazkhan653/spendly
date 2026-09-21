import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = "spendly.db"

def get_db():
    """
    Opens a connection to the SQLite database.
    Sets row_factory to sqlite3.Row for dictionary-like access.
    Enables foreign key constraints.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """
    Creates the database tables if they do not exist.
    """
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
        """)
        conn.commit()

def seed_db():
    """
    Populates the database with demo data if it is empty.
    """
    with get_db() as conn:
        # Check if users table is empty to avoid duplicate seeding
        user = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
        if user:
            return

        # Create demo user
        password_hash = generate_password_hash("demo123")
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", password_hash)
        )
        user_id = cursor.lastrowid

        # Fixed categories list from specs
        categories = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]

        # Generate 8 sample expenses
        sample_expenses = [
            (user_id, 12.50, "Food", "2026-09-01", "Lunch at Cafe"),
            (user_id, 45.00, "Transport", "2026-09-02", "Weekly pass"),
            (user_id, 120.00, "Bills", "2026-09-03", "Internet Bill"),
            (user_id, 30.00, "Health", "2026-09-05", "Pharmacy"),
            (user_id, 15.00, "Entertainment", "2026-09-07", "Movie ticket"),
            (user_id, 60.00, "Shopping", "2026-09-10", "New Shirt"),
            (user_id, 10.00, "Other", "2026-09-12", "Miscellaneous"),
            (user_id, 25.00, "Food", "2026-09-15", "Dinner with friends"),
        ]

        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            sample_expenses
        )
        conn.commit()

def create_user(name, email, password_hash):
    """
    Creates a new user in the database.
    Returns the new user's ID.
    Raises sqlite3.IntegrityError if email is not unique.
    """
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash)
        )
        conn.commit()
        return cursor.lastrowid
