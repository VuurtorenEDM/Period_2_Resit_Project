##take data in from lm35 sensor
##push to db
##comm data out
##redirect pages (can use homepage as reference)

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)

@app.get("/")
def index():
    return "hello, World"

# Initialize database
def init_db():
    conn = sqlite3.connect("temperature.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS temperature_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        temperature REAL NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# Route to receive temperature data
@app.route('/add', methods=['POST'])
def add_temperature():
    data = request.json
    temperature = data.get("temperature")

    if temperature is None:
        return jsonify({"error": "No temperature provided"}), 400

    conn = sqlite3.connect("LM35.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO temperature_data (temperature) VALUES (?)", (temperature,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Temperature added successfully!"})

# Route to fetch temperature data
@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect("LM35.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM temperature_data ORDER BY timestamp DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    data = [{"id": row[0], "temperature": row[1], "timestamp": row[2]} for row in rows]
    return render_template("data.html", data = [{"temperature":"18", "timestamp": "25/01/30"}])

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)), debug=True)