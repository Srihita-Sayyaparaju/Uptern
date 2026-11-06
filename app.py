import sqlite3
from flask import Flask, render_template, request, redirect, session
from database.db import create_table
from chatbot.chatbot import ask_ai
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = "uptern_secret_key"
# Create the database table when the app starts
create_table()

@app.route("/")
def home():

    return render_template("landing.html")

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("index.html")

from math import ceil

@app.route("/internships")
def internships():

    if "user_id" not in session:
        return redirect("/login")
    
    page = request.args.get("page", 1, type=int)
    per_page = 20

    search = request.args.get("search", "")
    location = request.args.get("location", "")
    category = request.args.get("category", "")

    conn = sqlite3.connect("database/internships.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM internships WHERE 1=1"
    params = []

    if search:
        query += """
        AND (
            title LIKE ?
            OR company LIKE ?
            OR location LIKE ?
            OR category LIKE ?
        )
        """
        params.extend([
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ])

    if location:
        query += " AND location = ?"
        params.append(location)

    if category:
        query += " AND category = ?"
        params.append(category)

    # Count total results
    count_query = query.replace("SELECT *", "SELECT COUNT(*)")

    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]

    total_pages = ceil(total / per_page)

    offset = (page - 1) * per_page

    query += " ORDER BY id DESC LIMIT ? OFFSET ?"

    params.extend([per_page, offset])

    cursor.execute(query, params)
    jobs = cursor.fetchall()

    cursor.execute("""
        SELECT DISTINCT location
        FROM internships
        ORDER BY location
    """)
    locations = cursor.fetchall()

    cursor.execute("""
        SELECT DISTINCT category
        FROM internships
        ORDER BY category
    """)
    categories = cursor.fetchall()

    conn.close()

    return render_template(
        "internships.html",
        jobs=jobs,
        search=search,
        location=location,
        category=category,
        locations=locations,
        categories=categories,
        page=page,
        total=total,
        total_pages=total_pages
    )


@app.route("/chat", methods=["POST"])
def chat():

    if "user_id" not in session:
        return jsonify({
            "reply": "Please login first."
        }), 401

    user_id = session["user_id"]
    message = request.json["message"]

    import os

    db_path = os.path.abspath("database/internships.db")
    print("Using database:", db_path)

    # Open database
    conn = sqlite3.connect(db_path, timeout=10)
    cursor = conn.cursor()

    # Save user's message
    cursor.execute("""
        INSERT INTO chat_history (user_id, sender, message)
        VALUES (?, ?, ?)
    """, (user_id, "user", message))

    conn.commit()
    conn.close()          # <-- IMPORTANT: Close before ask_ai()

    # Get AI response
    reply = ask_ai(message)

    # Open database again
    conn = sqlite3.connect(db_path, timeout=10)
    cursor = conn.cursor()

    # Save AI response
    cursor.execute("""
        INSERT INTO chat_history (user_id, sender, message)
        VALUES (?, ?, ?)
    """, (user_id, "bot", reply))

    conn.commit()
    conn.close()

    return jsonify({
        "reply": reply
    })

@app.route("/load_chat")
def load_chat():

    if "user_id" not in session:
        return jsonify([])

    user_id = session["user_id"]

    conn = sqlite3.connect("database/internships.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sender, message
        FROM chat_history
        WHERE user_id = ?
        ORDER BY chat_id ASC
    """, (user_id,))

    messages = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return jsonify(messages)

@app.route("/clear_chat", methods=["POST"])
def clear_chat():

    if "user_id" not in session:
        return jsonify({"success": False}), 401

    conn = sqlite3.connect("database/internships.db")
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM chat_history
        WHERE user_id=?
    """, (session["user_id"],))

    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route("/signup")
def signup():

    if "user_id" in session:
        return redirect("/dashboard")

    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup_post():

    full_name = request.form["full_name"]
    email = request.form["email"].strip().lower()
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if password != confirm_password:
        return "Passwords do not match."

    conn = sqlite3.connect("database/internships.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )

    if cursor.fetchone():
        conn.close()
        return "Email already exists."

    hashed_password = generate_password_hash(password)

    cursor.execute("""
        INSERT INTO users(full_name,email,password)
        VALUES(?,?,?)
    """, (
        full_name,
        email,
        hashed_password
    ))

    conn.commit()

    cursor.execute(
        "SELECT user_id, full_name FROM users WHERE email=?",
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    session["user_id"] = user[0]
    session["name"] = user[1]

    return redirect("/dashboard")

@app.route("/login")
def login():

    if "user_id" in session:
        return redirect("/dashboard")

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():

    email = request.form["email"].strip().lower()
    password = request.form["password"]

    conn = sqlite3.connect("database/internships.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id, full_name, password FROM users WHERE email=?",
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    if user is None:
        return render_template(
            "login.html",
            error="❌ Invalid email or password."
        )

    if not check_password_hash(user[2], password):
        return render_template(
            "login.html",
            error="❌ Invalid email or password."
        )

    session["user_id"] = user[0]
    session["name"] = user[1]

    return redirect("/dashboard")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

@app.route("/companies")
def companies():

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database/internships.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM companies
        ORDER BY company_name
    """)

    companies = cursor.fetchall()

    conn.close()

    return render_template(
        "companies.html",
        companies=companies
    )

if __name__ == "__main__":
    app.run(debug=True)
    