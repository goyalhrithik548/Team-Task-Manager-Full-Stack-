from flask import Blueprint, g, jsonify
from sqlalchemy import func

from ..decorators import login_required
from ..models import Project, Task, TaskStatus


api_bp = Blueprint("api", __name__, url_prefix="/api")


def _task_scope():
    if g.current_user.is_admin():
        return Task.query
    return Task.query.filter_by(assigned_to=g.current_user.id)


@api_bp.route("/dashboard/stats")
@login_required
def dashboard_stats():
    task_query = _task_scope()

    data = {
        "total_tasks": task_query.count(),
        "completed_tasks": task_query.filter_by(status=TaskStatus.DONE.value).count(),
        "pending_tasks": task_query.filter(Task.status != TaskStatus.DONE.value).count(),
        "overdue_tasks": task_query.filter(
            Task.due_date < func.current_date(),
            Task.status != TaskStatus.DONE.value,
        ).count(),
    }
    return jsonify(data)


@api_bp.route("/projects")
@login_required
def api_projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return jsonify([project.to_dict() for project in projects])


@api_bp.route("/projects/<int:project_id>/tasks")
@login_required
def api_project_tasks(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify([task.to_dict() for task in project.tasks])
