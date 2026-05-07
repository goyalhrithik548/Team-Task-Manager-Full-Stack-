from datetime import datetime

from flask import Blueprint, flash, g, jsonify, redirect, request, url_for

from ..decorators import admin_required, login_required
from ..extensions import db
from ..models import Project, Task, TaskStatus, User


task_bp = Blueprint("tasks", __name__)


def _parse_due_date(value):
    if not value:
        return None

    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def _assignee_for_project(project, assignee_id):
    try:
        assignee_id = int(assignee_id)
    except (TypeError, ValueError):
        return None

    assignee = db.session.get(User, assignee_id)

    if not assignee or assignee not in project.members:
        return None

    return assignee


@task_bp.route("/projects/<int:project_id>/tasks", methods=["POST"])
@admin_required
def create_task(project_id):
    project = db.get_or_404(Project, project_id)

    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    due_date = _parse_due_date(request.form.get("due_date"))
    status = request.form.get("status", TaskStatus.TODO.value)
    assignee = _assignee_for_project(project, request.form.get("assigned_to"))

    errors = []
    if not title:
        errors.append("Task title is required.")
    if not description:
        errors.append("Task description is required.")
    if not due_date:
        errors.append("Please provide a valid due date.")
    if status not in [task_status.value for task_status in TaskStatus]:
        errors.append("Please choose a valid task status.")
    if not assignee:
        errors.append("Please assign the task to a project team member.")

    if errors:
        for error in errors:
            flash(error, "danger")
        return redirect(url_for("projects.project_detail", project_id=project.id))

    task = Task(
        title=title,
        description=description,
        due_date=due_date,
        status=status,
        assignee=assignee,
        project=project,
    )

    try:
        db.session.add(task)
        db.session.commit()
        flash("Task created successfully.", "success")
    except Exception:
        db.session.rollback()
        flash("Unable to create the task.", "danger")

    return redirect(url_for("projects.project_detail", project_id=project.id))


@task_bp.route("/tasks/<int:task_id>/status", methods=["POST"])
@login_required
def update_status(task_id):
    task = db.get_or_404(Task, task_id)
    next_status = request.form.get("status", "").strip()

    if next_status not in [status.value for status in TaskStatus]:
        flash("Please choose a valid task status.", "danger")
        return redirect(url_for("projects.project_detail", project_id=task.project_id))

    can_update = g.current_user.is_admin() or task.assigned_to == g.current_user.id
    if not can_update:
        flash("You can only update your own assigned tasks.", "danger")
        return redirect(url_for("projects.project_detail", project_id=task.project_id))

    task.status = next_status

    try:
        db.session.commit()
        flash("Task status updated.", "success")
    except Exception:
        db.session.rollback()
        flash("Unable to update the task status.", "danger")

    return redirect(url_for("projects.project_detail", project_id=task.project_id))


@task_bp.route("/tasks/<int:task_id>/delete", methods=["POST"])
@admin_required
def delete_task(task_id):
    task = db.get_or_404(Task, task_id)
    project_id = task.project_id

    try:
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted successfully.", "success")
    except Exception:
        db.session.rollback()
        flash("Unable to delete the task.", "danger")

    return redirect(url_for("projects.project_detail", project_id=project_id))


@task_bp.route("/api/tasks/<int:task_id>")
@login_required
def task_api_detail(task_id):
    task = db.get_or_404(Task, task_id)
    return jsonify(task.to_dict())
