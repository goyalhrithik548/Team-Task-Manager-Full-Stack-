from flask import Blueprint, g, redirect, render_template, url_for
from sqlalchemy import func

from ..decorators import login_required
from ..models import Project, Task, TaskStatus


main_bp = Blueprint("main", __name__)


def _task_scope_for_user(user):
    query = Task.query
    if user.is_admin():
        return query
    return query.filter_by(assigned_to=user.id)


@main_bp.route("/")
def index():
    if g.get("current_user"):
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    user = g.current_user
    task_query = _task_scope_for_user(user)

    total_tasks = task_query.count()
    completed_tasks = task_query.filter_by(status=TaskStatus.DONE.value).count()
    pending_tasks = task_query.filter(Task.status != TaskStatus.DONE.value).count()
    overdue_tasks = task_query.filter(
        Task.due_date < func.current_date(),
        Task.status != TaskStatus.DONE.value,
    ).count()

    recent_tasks = (
        task_query.order_by(Task.due_date.asc(), Task.created_at.desc()).limit(8).all()
    )
    overdue_task_list = (
        task_query.filter(
            Task.due_date < func.current_date(),
            Task.status != TaskStatus.DONE.value,
        )
        .order_by(Task.due_date.asc())
        .limit(6)
        .all()
    )
    recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        active_page="dashboard",
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        overdue_tasks=overdue_tasks,
        recent_tasks=recent_tasks,
        overdue_task_list=overdue_task_list,
        recent_projects=recent_projects,
    )
