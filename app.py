from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

# ✅ Railway MySQL Connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT", 3306))
    )

# ✅ Home Page
@app.route("/")
def home():
    return render_template("index.html")

# ✅ Contact Form → Save to DB
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)",
        (name, email, message)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/")

# ✅ Create Table Automatically
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            message TEXT
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

# ✅ Run App
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)