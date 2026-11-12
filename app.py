
import os
from urllib.parse import urlparse, unquote

import pg8000
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

frontend_url = os.getenv(
    "FRONTEND_ORIGIN",
    "https://sanjanasraj.github.io"
)

CORS(app, origins=[frontend_url])

DATABASE_URL = os.getenv("DATABASE_URL")


def get_db_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured.")

    parsed = urlparse(DATABASE_URL)

    return pg8000.connect(
        host=parsed.hostname,
        port=parsed.port or 5432,
        database=parsed.path.lstrip("/"),
        user=unquote(parsed.username),
        password=unquote(parsed.password),
        ssl_context=True
    )


def create_table():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                title VARCHAR(150) NOT NULL,
                description TEXT NOT NULL,
                technologies TEXT NOT NULL,
                project_url TEXT
            )
        """)
        conn.commit()
        cursor.close()
    finally:
        conn.close()


@app.route("/")
def home():
    return jsonify({
        "message": "Sanjana's Portfolio API is running!"
    })


@app.route("/api/health")
def health():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()

        return jsonify({
            "status": "healthy",
            "database": "connected"
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500

    finally:
        if conn:
            conn.close()


@app.route("/api/projects")
def get_projects():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects ORDER BY id")

        columns = [column[0] for column in cursor.description]
        projects = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        cursor.close()
        return jsonify(projects)

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500

    finally:
        if conn:
            conn.close()


create_table()

if __name__ == "__main__":
    app.run(debug=True)
