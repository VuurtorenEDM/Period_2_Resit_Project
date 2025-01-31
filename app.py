from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
import sqlite3
import os
import plotly.express as px
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    # Connect to SQLite and fetch data
    conn = sqlite3.connect("LM35.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM temperature_data ORDER BY timestamp DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    # Convert to DataFrame
    df = pd.DataFrame(rows, columns=["id", "temperature", "timestamp"])  # Adjust column names as needed

    # Create the graph
    fig = px.line(df, x="timestamp", y="temperature", title="LM35 Data")

    # Customize layout
    fig.update_layout(
        xaxis_title="Timestamp",
        yaxis_title="Temperature (°C)",
        xaxis=dict(tickangle=-45)  # Rotate labels for readability
    )

    # Convert to HTML
    graph_html = fig.to_html(full_html=False)

    return render_template('index.html', graph_html=graph_html)

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__name__":
    app.run(debug=True)

# Initialize database
def init_db():
    conn = sqlite3.connect("LM35.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS temperature_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        temperature REAL NOT NULL,
                        timestamp DATETIME NOT NULL)''')
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
    cursor.execute("INSERT INTO temperature_data (temperature, timestamp) VALUES (?, ?)", (temperature, datetime.now(pytz.timezone('Europe/Amsterdam')).strftime('%Y-%m-%d %H:%M:%S')))
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
    return render_template("data.html", data = data)

# if __name__ == '__main__':
#     init_db()
#     app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 443)), debug=True)

