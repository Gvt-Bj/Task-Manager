task-manager/
├─ app.py                # FastAPI backend
├─ templates/
│   └─ index.html        # HTML template
├─ static/
│   ├─ style.css         # CSS for styling
│   └─ script.js         # JS for dynamic behavior
├─ tasks.db              # SQLite database (auto-created)
└─ README.md

git clone https://github.com/yourusername/desk-tasks.git
cd desk-tasks

pip install fastapi uvicorn jinja2

uvicorn app:app --reload

http://127.0.0.1:8000
Tasks are stored in tasks.db automatically.

Add, edit, delete, and complete tasks directly in the browser.

Usage

Add a Task: Enter a task title in the input box and click Add.

Mark Complete/Incomplete: Click the ✔ button next to the task.

Delete a Task: Click the 🗑 button.

Edit Task Title: Click on the task title, edit, and press Enter or click outside to save.

Tech Stack

Backend: FastAPI

Database: SQLite

Frontend: HTML, CSS, JavaScript (Vanilla JS)

Templating: Jinja2

Future Enhancements

Drag-and-drop task reordering

Task deadlines and priorities

Categories or tags for tasks

Dark mode toggle

User authentication for multiple users
