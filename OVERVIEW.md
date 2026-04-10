# Flask — Package/Library Overview

---

## 1. Which package/library did I select?

**Flask** — a web framework for Python.

- 📦 Install: `pip install flask`
- 📖 Docs: https://flask.palletsprojects.com/
- 🐍 Language: Python

---

## 2. What is Flask?

### What purpose does it serve?

Flask lets you build web applications in Python. It connects URLs to Python functions, renders HTML pages, reads form input, and sends responses back to the browser — with very little boilerplate. It is called a "micro-framework" because it provides only what is needed without forcing a specific structure [1].

### How do you use it?

A minimal Flask app looks like this:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

if __name__ == "__main__":
    app.run()
```

You define **routes** using `@app.route(...)`, write a Python function for each one, and Flask handles the rest. Running the file starts a local development server at `http://127.0.0.1:5000`.

### Core concepts in detail

**Routing with methods** — restricting a route to GET or POST:

```python
@app.route("/add", methods=["POST"])
def add():
    ...
```

**Reading form input** — from a submitted HTML form:

```python
from flask import request

title    = request.form.get("title", "").strip()
priority = request.form.get("priority", "medium")
due_date = request.form.get("due_date") or None
```

**Reading URL query parameters** — for search and filter:

```python
search = request.args.get("q", "")
status = request.args.get("filter", "all")
```

**Rendering HTML templates with Jinja2** — passing Python data into HTML:

```python
from flask import render_template

return render_template("index.html", tasks=tasks, today=today)
```

Inside the template, Jinja2 lets you use conditionals and loops:

```html
{% for task in tasks %}
    <li class="{% if task['done'] %}done{% endif %}">
        {{ task["title"] }}
    </li>
{% endfor %}
```

**Redirecting after form submission** — to avoid duplicate submissions on refresh:

```python
from flask import redirect, url_for

return redirect(url_for("index", filter="all"))
```

**Connecting to SQLite** — Flask works seamlessly with Python's built-in sqlite3:

```python
import sqlite3

def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row  # lets you access columns by name
    return conn
```

---

## 3. Functionalities of Flask used in this project

| Flask Feature | How it is used |
|---|---|
| `@app.route()` | Defines 6 routes: `/`, `/add`, `/complete`, `/delete`, `/edit`, `/clear` |
| `methods=["POST"]` | Restricts `/add` and `/edit` to POST requests only |
| `request.form` | Reads task title, priority, and due date from HTML forms |
| `request.args` | Reads `?filter=` and `?q=` from the URL for filtering and search |
| `render_template()` | Renders `index.html` with task data, today's date, filter state |
| `redirect()` + `url_for()` | Redirects back to `/` after every action, preserving filter/search state |
| Jinja2 conditionals | Shows "overdue" warning, toggles Done/Undo button, dims completed tasks |
| Jinja2 filters | `| capitalize`, `| int`, `| selectattr` used in the template |
| `sqlite3` (via Python) | Stores and retrieves tasks with INSERT, SELECT, UPDATE, DELETE |

**Example — dynamic SQL with search and filter:**

```python
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

tasks = conn.execute(sql, params).fetchall()
```

This builds a query conditionally depending on what the user searched and filtered — a more realistic pattern than a single fixed query.

---

## 4. When was Flask created?

Flask was first released in **2010** by Armin Ronacher, originally as an April Fool's joke that became a legitimate project [2]. It is now maintained by the Pallets Projects team and is consistently ranked among the most popular Python web frameworks worldwide.

---

## 5. Why did I select Flask?

I was only used to coding python in a very simple way which only includes functions and getting the results in the terminal, so i wanted to program something with python that looked visually appealing and interactive in a web browser.
Most of the Lab activities in our class only dealt with functions and scripts. Flask library felt beginer friendly to take a step ahead into web application. Its also easier to follow compared to bigger frameworks like Django.

---

## 6. How did learning Flask influence my learning of Python?

Working with Flask reinforced and extended several Python concepts:

**request.form vs request.args**: I mixed these up early on and kept getting empty values back. Fixing that made me understand how GET and POST actually work differently.
**.get()** on form data: I already knew **dictionary .get()** from previous CS courses, so seeing **request.form.get("key", default)** work the same way made it less intimidating.
**Jinja2** templates: At first it felt weird writing **{% if %}** and **{% for %}** inside an HTML file. But once I saw how Flask passes data from Python into the template, it made sense. It's basically the same logic just in a different place.

Flask made Python feel more useful than just running scripts in a terminal.

---

## 7. Overall experience with Flask

### When would I recommend Flask?

Flask is a good fit for:

- Someone who knows Python basics and wants to build something like web based application
- Small tools, personal projects, or prototypes where setup time matters
- Learning how web apps work at a fundamental level before moving to larger frameworks like Django [3]

It is probably not the right choice for large production applications that need a lot of built-in structure out of the box.

One thing that was confusing at first: understanding the difference between **request.form (POST data)** and **request.args (URL parameters)**, took a bit of trial and error

### Would I continue using Flask?

Yes. Getting a working, styled, database-backed web app running in under 150 lines of Python code is a strong sign of how accessible Flask is. I could see using it in future co-op/Internship or personal projects to wrap a Python script in a simple UI.

---

## References

[1] Flask Documentation — "What does 'micro' mean?": https://flask.palletsprojects.com/en/stable/foreword/#what-does-micro-mean

[2] Flask — Wikipedia: https://en.wikipedia.org/wiki/Flask_(web_framework)

[3] Pallets Projects — Flask: https://palletsprojects.com/projects/flask/
