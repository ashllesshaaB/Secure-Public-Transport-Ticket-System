from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import hashlib
import qrcode
import os
from cryptography.fernet import Fernet

app = Flask(__name__)

# -----------------------------
# Encryption Setup
# -----------------------------
key = Fernet.generate_key()
cipher = Fernet(key)

# -----------------------------
# Database Setup
# -----------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            destination TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# -----------------------------
# Home
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -----------------------------
# Register
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, hashed_password))
        conn.commit()
        conn.close()

        return "User Registered Securely!"

    return render_template("register.html")

# -----------------------------
# Login
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?",
                  (username, hashed_password))
        user = c.fetchone()
        conn.close()

        if user:
            return redirect(url_for("dashboard"))
        else:
            return "Invalid Credentials"

    return render_template("login.html")

# -----------------------------
# Dashboard
# -----------------------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# -----------------------------
# Book Ticket (Encrypted + Fraud Detection)
# -----------------------------
@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "POST":
        source = request.form["source"]
        destination = request.form["destination"]

        # Fraud Detection Rule
        if source.lower() == destination.lower():
            return "Fraud Detected: Source and Destination cannot be same!"

        encrypted_source = cipher.encrypt(source.encode())
        encrypted_destination = cipher.encrypt(destination.encode())

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO tickets (source, destination) VALUES (?, ?)",
                  (encrypted_source, encrypted_destination))
        ticket_id = c.lastrowid
        conn.commit()
        conn.close()

        if not os.path.exists("static"):
            os.makedirs("static")

        qr_data = f"TicketID:{ticket_id}"
        img = qrcode.make(qr_data)
        img.save(f"static/ticket_{ticket_id}.png")

        return f"""
        <h3>Encrypted Ticket Booked Successfully!</h3>
        <img src="/static/ticket_{ticket_id}.png" width="300">
        <br><br>
        <a href="/dashboard">Back to Dashboard</a>
        """

    return render_template("book.html")

# -----------------------------
# View Tickets
# -----------------------------
@app.route("/tickets")
def tickets():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tickets")
    data = c.fetchall()
    conn.close()

    result = "<h2>All Tickets</h2><br>"

    for row in data:
        ticket_id = row[0]
        source = cipher.decrypt(row[1]).decode()
        destination = cipher.decrypt(row[2]).decode()

        result += f"""
        Ticket ID: {ticket_id} <br>
        From: {source} <br>
        To: {destination} <br><br>
        """

    result += '<a href="/dashboard">Back</a>'
    return result

# -----------------------------
# Validate Ticket
# -----------------------------
@app.route("/validate", methods=["GET", "POST"])
def validate():
    if request.method == "POST":
        ticket_id = request.form["ticket_id"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,))
        ticket = c.fetchone()
        conn.close()

        if ticket:
            return "Valid Ticket ✅"
        else:
            return "Invalid Ticket ❌"

    return render_template("validate.html")

# -----------------------------
# Run with HTTPS Simulation
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')
