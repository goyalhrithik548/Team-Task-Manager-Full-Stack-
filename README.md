# Team Task Manager

A beginner-friendly full-stack task management app built with Flask, SQLAlchemy, PostgreSQL, Bootstrap 5, and vanilla JavaScript.

**LIVE_URL** - https://team-task-manager-full-stack-production-12c4.up.railway.app/

## Features

- Signup, login, and logout using Flask session authentication
- Role-based access control with `ADMIN` and `MEMBER`
- Project creation, team member assignment, and deletion
- Task creation, assignment, status updates, and deletion
- Dashboard cards for total, completed, pending, and overdue tasks
- Bootstrap UI with responsive layouts, cards, tables, and modals
- REST-style JSON endpoints under `/api`

## Tech Stack

- Backend: Python, Flask, Flask-SQLAlchemy
- Database: PostgreSQL
- Frontend: HTML, CSS, Bootstrap 5, Vanilla JavaScript
- Authentication: Flask session-based auth

## Folder Structure

```text
.
|-- app.py
|-- config.py
|-- seed.py
|-- requirements.txt
|-- .env.example
|-- team_task_manager
|   |-- __init__.py
|   |-- decorators.py
|   |-- extensions.py
|   |-- models.py
|   |-- routes
|   |   |-- __init__.py
|   |   |-- api.py
|   |   |-- auth.py
|   |   |-- main.py
|   |   |-- projects.py
|   |   `-- tasks.py
|   |-- static
|   |   |-- css
|   |   |   `-- style.css
|   |   `-- js
|   |       `-- app.js
|   `-- templates
|       |-- auth
|       |   |-- login.html
|       |   `-- signup.html
|       |-- errors
|       |   |-- 403.html
|       |   |-- 404.html
|       |   `-- 500.html
|       |-- partials
|       |   `-- flash_messages.html
|       |-- projects
|       |   |-- detail.html
|       |   `-- index.html
|       |-- base.html
|       `-- dashboard.html
`-- README.md
```

## Database Setup

Make sure PostgreSQL is installed and running.

### 1. Create the database

```sql
CREATE DATABASE team_task_manager;
```

If you are using the `psql` shell:

```bash
psql -U postgres
CREATE DATABASE team_task_manager;
\q
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and update the values if needed:

```env
SECRET_KEY=super-secret-key
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/team_task_manager
```

## Local Run Instructions

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate it

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Seed the database

```bash
python seed.py
```

### 5. Run the app

```bash
python app.py
```

Open the browser and visit:

```text
http://127.0.0.1:5000
```

## Demo Accounts

After running `python seed.py`, you can log in with:

- Admin: `admin@example.com` / `admin123`
- Member: `aisha@example.com` / `member123`
- Member: `rahul@example.com` / `member123`

## Role Rules

- `ADMIN` can create and delete projects
- `ADMIN` can create, assign, update, and delete tasks
- `MEMBER` can only update the status of tasks assigned to them

## Main Routes

### HTML Routes

- `GET /signup`
- `GET /login`
- `POST /logout`
- `GET /dashboard`
- `GET /projects`
- `POST /projects`
- `GET /projects/<project_id>`
- `POST /projects/<project_id>/members`
- `POST /projects/<project_id>/delete`
- `POST /projects/<project_id>/tasks`
- `POST /tasks/<task_id>/status`
- `POST /tasks/<task_id>/delete`

### JSON Routes

- `GET /api/dashboard/stats`
- `GET /api/projects`
- `GET /api/projects/<project_id>/tasks`
- `GET /api/tasks/<task_id>`

## Validation and Relationships

- Email must be valid and unique
- Password must be at least 6 characters
- Project title and description are required
- Task title, description, due date, assignee, and status are validated
- A task can only be assigned to a user who belongs to that project
- Relationships:
  - One user can create many projects
  - One project can have many tasks
  - One user can be assigned many tasks
  - Users and projects have a many-to-many relationship for team membership

## Deployment

The application can be deployed on Railway with:
- PostgreSQL database service
- Environment variables
- Flask production server

Environment variables required:
- SECRET_KEY
- DATABASE_URL

## Notes

- The app uses `db.create_all()` to keep setup simple for beginners.
- For a production app, Flask-Migrate and CSRF protection would be good next improvements.
