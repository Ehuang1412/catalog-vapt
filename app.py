from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True  
app.secret_key = "dev-only-secret-change-in-production"

DATABASE = "catalog.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        # Add a default admin user (in a real app, hash the password!)
        try:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                ("admin", "admin123")
            )
        except sqlite3.IntegrityError:
            pass  # User already exists
        conn.commit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("q", "")
    conn = get_db()
    if query:
        # ⚠️ VULNERABLE: f-string directly in SQL — SQL Injection here
        sql = f"SELECT * FROM items WHERE name LIKE '%{query}%'"
        results = conn.execute(sql).fetchall()
    else:
        results = []
    return render_template("search.html", results=results, query=query)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        conn = get_db()
        # Note: using parameterized query here (safe)
        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()
        if user:
            session["admin"] = True
            return redirect(url_for("admin"))
        else:
            return "Invalid credentials", 401
    if not session.get("admin"):
        return render_template("login.html")
    return render_template("admin.html")

@app.route("/admin/add", methods=["POST"])
def add_item():
    if not session.get("admin"):
        return "Unauthorized", 401
    name = request.form.get("name")
    description = request.form.get("description")
    price = request.form.get("price")
    conn = get_db()
    conn.execute(
        "INSERT INTO items (name, description, price) VALUES (?, ?, ?)",
        (name, description, price)
    )
    conn.commit()
    return redirect(url_for("admin"))

if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)
