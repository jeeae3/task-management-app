from flask import Flask, request, jsonify
import os
import sqlite3

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "database.py")

def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS board (
            board_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS category (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            board_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            position INTEGER NOT NULL,
            FOREIGN KEY (board_id) REFERENCES board(board_id) ON DELETE CASCADE
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            position INTEGER NOT NULL,
            comment TEXT,
            is_completed INTEGER DEFAULT 0,
            due_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES category(category_id) ON DELETE CASCADE
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_task (
            user_id INTEGER NOT NULL,
            task_id INTEGER NOT NULL,
            PRIMARY KEY (user_id, task_id),
            FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
            FOREIGN KEY (task_id) REFERENCES task(task_id) ON DELETE CASCADE
        );
    """)

    conn.commit()
    conn.close()


# ---------- CREATE ----------
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO "task" (category_id, title, position, comment, is_completed, due_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data.get('category_id'),
        data.get('title'),
        data.get('position'),
        data.get('comment'), 
        1 if data.get('is_completed') is True else 0,
        data.get('due_date'),
    ))
    conn.commit()
    
    new_task_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "task created"
        , "task_id": new_task_id
    }), 201


# ---------- READ ALL ----------
@app.route('/tasks', methods=['GET'])
def read_tasks():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM \"task\"")
    rows = cursor.fetchall()

    conn.close()

    tasks = [
        {
            "task_id": row[0],
            "title": row[1],
            "position": row[2],
            "comment": row[3],
            "is_completed": row[4],
            "due_date": row[5]
        }
        for row in rows
    ]

    return jsonify(tasks), 200


# ---------- READ ONE ----------
@app.route('/tasks/<int:id>', methods=['GET'])
def read_task(id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM \"task\" WHERE order_id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "task not found"}), 404

    task = {
        "task_id": row[0],
        "title": row[1],
        "position": row[2],
        "comment": row[3],
        "is_completed": row[4],
        "due_date": row[5]
    }

    return jsonify(task), 200


# ---------- UPDATE -------------

@app.route('/tasks/<int:>id/', methods=['PUT'])
def update_task(id):
    data = request.json

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE task
        SET category_id=?,
            title = ?, 
            position = ?, 
            comment = ?, 
            is_completed = ?, 
            due_date = ?
        WHERE task_id = ?
    """, (
        data.get('category_id'),
        data.get('title'),
        data.get('position'),
        data.get('comment'),
        1 if data.get('is_completed') is True else 0,
        data.get('due_date'),
        id
    ))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    conn.close()
    return jsonify({"message": "Task updated"}), 200


# ---------- DELETE ----------
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_order(id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM \"task\" WHERE task_id = ?", (id,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    conn.close()
    return jsonify({"message": "Task deleted"}), 200

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=4000)