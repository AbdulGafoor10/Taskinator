import sqlite3
from datetime import date
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB = "tasks.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            title    TEXT    NOT NULL,
            done     INTEGER NOT NULL DEFAULT 0,
            priority TEXT    NOT NULL DEFAULT 'medium',
            due_date TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = get_db()

    status_filter = request.args.get("filter", "all")
    search_query  = request.args.get("q", "").strip()

    sql    = "SELECT * FROM tasks WHERE 1=1"
    params = []

    if status_filter == "active":
        sql += " AND done = 0"
    elif status_filter == "done":
        sql += " AND done = 1"

    if search_query:
        sql += " AND title LIKE ?"
        params.append(f"%{search_query}%")

    sql += " ORDER BY done ASC, due_date ASC NULLS LAST, id DESC"

    tasks      = conn.execute(sql, params).fetchall()
    total      = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    done_count = conn.execute("SELECT COUNT(*) FROM tasks WHERE done = 1").fetchone()[0]
    conn.close()

    today = date.today().isoformat()

    return render_template(
        "index.html",
        tasks=tasks,
        total=total,
        done_count=done_count,
        today=today,
        filter=status_filter,
        q=search_query,
    )


@app.route("/add", methods=["POST"])
def add():
    title    = request.form.get("title", "").strip()
    priority = request.form.get("priority", "medium")
    due_date = request.form.get("due_date", "").strip() or None

    if title:
        conn = get_db()
        conn.execute(
            "INSERT INTO tasks (title, priority, due_date) VALUES (?, ?, ?)",
            (title, priority, due_date),
        )
        conn.commit()
        conn.close()

    return redirect(url_for("index",
        filter=request.args.get("filter", "all"),
        q=request.args.get("q", "")
    ))

@app.route("/complete/<int:task_id>")
def complete(task_id):
    conn = get_db()
    conn.execute("UPDATE tasks SET done = 1 - done WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index",
        filter=request.args.get("filter", "all"),
        q=request.args.get("q", "")
    ))

@app.route("/delete/<int:task_id>")
def delete(task_id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index",
        filter=request.args.get("filter", "all"),
        q=request.args.get("q", "")
    ))


@app.route("/edit/<int:task_id>", methods=["POST"])
def edit(task_id):
    new_title = request.form.get("title", "").strip()
    new_due   = request.form.get("due_date", "").strip() or None
    new_prio  = request.form.get("priority", "medium")

    if new_title:
        conn = get_db()
        conn.execute(
            "UPDATE tasks SET title = ?, due_date = ?, priority = ? WHERE id = ?",
            (new_title, new_due, new_prio, task_id),
        )
        conn.commit()
        conn.close()

    return redirect(url_for("index",
        filter=request.args.get("filter", "all"),
        q=request.args.get("q", "")
    ))

@app.route("/clear")
def clear_done():
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE done = 1")
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
