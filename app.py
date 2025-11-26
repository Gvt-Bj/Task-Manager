from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# SQLite DB
conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    completed INTEGER DEFAULT 0
)
""")
conn.commit()

# Home page
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

# Add task (AJAX)
@app.post("/api/add")
def add_task(title: str = Form(...)):
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    conn.commit()
    task_id = cursor.lastrowid
    return JSONResponse({"id": task_id, "title": title, "completed": 0})

# Toggle completed (AJAX)
@app.post("/api/toggle/{task_id}")
def toggle_task(task_id: int):
    cursor.execute("UPDATE tasks SET completed = NOT completed WHERE id = ?", (task_id,))
    conn.commit()
    cursor.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,))
    status = cursor.fetchone()[0]
    return JSONResponse({"id": task_id, "completed": status})

# Delete task (AJAX)
@app.post("/api/delete/{task_id}")
def delete_task(task_id: int):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    return JSONResponse({"id": task_id})

# Edit task (AJAX)
@app.post("/api/edit/{task_id}")
def edit_task(task_id: int, title: str = Form(...)):
    cursor.execute("UPDATE tasks SET title = ? WHERE id = ?", (title, task_id))
    conn.commit()
    return JSONResponse({"id": task_id, "title": title})
