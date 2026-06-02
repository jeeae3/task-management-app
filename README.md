# TaskBoard — Project & Task Management App

A full-stack Kanban-style task management application built with Flask, React, and SQLite.

## Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Backend     | Python 3 + Flask                  |
| Database    | SQLite                            |
| Frontend    | React 18 + Vite + React Router    |
| Monitoring  | Prometheus + Grafana (via Docker) |

---

## Project Structure

```
task-management-app/
├── taskboard/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── main.py           # Flask app entry point
│   │   │   ├── database.py       # DB setup and default data
│   │   │   ├── models/           # Data models
│   │   │   ├── schemas/          # Repository classes (CRUD logic)
│   │   │   └── routes/
│   │   │       ├── projects.py   # Project CRUD endpoints
│   │   │       └── tasks.py      # Task CRUD endpoints
│   │   ├── tests/                # Unit tests
│   │   └── requirements.txt      # Python dependencies
│   └── frontend/
│       ├── src/
│       │   ├── api/              # API client (fetch calls)
│       │   ├── components/       # Reusable UI components
│       │   ├── pages/            # ProjectsPage, BoardPage
│       │   ├── App.jsx           # Root component + routing
│       │   └── App.css           # Global styles
│       └── package.json          # Node dependencies
└── README.md
```

---

## Prerequisites

Make sure you have the following installed:

- Python 3.8+
- Node.js 18+
- npm 9+
- pip

---

## Setup & Running Locally

You need to run the **backend** and **frontend** in two separate terminal windows.

### Terminal 1 — Backend (Flask)

```bash
# 1. Navigate to backend folder
cd taskboard/backend

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Navigate to app folder
cd app

# 4. Run the Flask server
python main.py
```

Backend will be running at: **http://localhost:4000**

> The database is created and populated with sample data automatically on first run.
> If the database is empty, run this once:
> ```bash
> python3 -c "import database; db = database.Database(); db.populate_db_default()"
> ```

---

### Terminal 2 — Frontend (React)

```bash
# 1. Navigate to frontend folder
cd taskboard/frontend

# 2. Install Node dependencies
npm install

# 3. Start the dev server
npm run dev
```

Frontend will be running at: **http://localhost:5173**

---

## API Endpoints

### Projects
| Method | Endpoint            | Description         |
|--------|---------------------|---------------------|
| GET    | /projects           | Get all projects    |
| POST   | /projects           | Create a project    |
| GET    | /projects/\<id\>    | Get single project  |
| PUT    | /projects/\<id\>    | Update project      |
| DELETE | /projects/\<id\>    | Delete project      |

### Tasks
| Method | Endpoint         | Description      |
|--------|------------------|------------------|
| GET    | /tasks           | Get all tasks    |
| POST   | /tasks           | Create a task    |
| GET    | /tasks/\<id\>    | Get single task  |
| PUT    | /tasks/\<id\>    | Update task      |
| DELETE | /tasks/\<id\>    | Delete task      |

---

## Database Schema

```
project
├── project_id    INTEGER PRIMARY KEY
├── board_id      INTEGER
├── name          TEXT
└── position      INTEGER

task
├── task_id       INTEGER PRIMARY KEY
├── project_id    INTEGER FK → project
├── title         TEXT
├── position      INTEGER
├── comment       TEXT
├── status        TEXT (todo | in_progress | done)
├── priority      TEXT (low | medium | high)
├── due_date      TEXT
└── created_at    TEXT
```

---

## Features

- View all projects on a dashboard
- Click into any project to see its Kanban board
- Create, edit, and delete projects
- Create, edit, and delete tasks
- Move tasks between columns (To Do → In Progress → Done)
- Set task priority (Low / Medium / High)

---

## Running Tests

```bash
cd taskboard/backend
pytest tests/
```
