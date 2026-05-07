from flask import Blueprint, flash, g, jsonify, redirect, render_template, request, url_for

from ..decorators import admin_required, login_required
from ..extensions import db
from ..models import Project, User


project_bp = Blueprint("projects", __name__, url_prefix="/projects")


def _selected_members(member_ids):
    if not member_ids:
        return []

    clean_ids = []
    for member_id in member_ids:
        try:
            clean_ids.append(int(member_id))
        except (TypeError, ValueError):
            return None

    unique_ids = list(dict.fromkeys(clean_ids))
    members = User.query.filter(User.id.in_(unique_ids)).all()

    if len(members) != len(unique_ids):
        return None

    return members


def _validate_project_input(title, description, member_ids, creator):
    errors = []

    if not title:
        errors.append("Project title is required.")
    if not description:
        errors.append("Project description is required.")

    members = _selected_members(member_ids)
    if members is None:
        errors.append("Please choose valid team members.")
        members = []

    if creator not in members:
        members.append(creator)

    return errors, members


@project_bp.route("", methods=["GET", "POST"])
@login_required
def project_list():
    if request.method == "POST":
        if not g.current_user.is_admin():
            flash("Only admins can create projects.", "danger")
            return redirect(url_for("projects.project_list"))

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        member_ids = request.form.getlist("member_ids")

        errors, members = _validate_project_input(
            title, description, member_ids, g.current_user
        )

        if errors:
            for error in errors:
                flash(error, "danger")
            return redirect(url_for("projects.project_list"))

        project = Project(
            title=title,
            description=description,
            creator=g.current_user,
        )
        project.members = members

        try:
            db.session.add(project)
            db.session.commit()
            flash("Project created successfully.", "success")
        except Exception:
            db.session.rollback()
            flash("Could not create the project. Please try again.", "danger")

        return redirect(url_for("projects.project_list"))

    projects = Project.query.order_by(Project.created_at.desc()).all()
    users = User.query.order_by(User.full_name.asc()).all()
    return render_template(
        "projects/index.html",
        active_page="projects",
        projects=projects,
        users=users,
    )


@project_bp.route("/<int:project_id>")
@login_required
def project_detail(project_id):
    project = db.get_or_404(Project, project_id)

    return render_template(
        "projects/detail.html",
        active_page="projects",
        project=project,
        users=User.query.order_by(User.full_name.asc()).all(),
    )


@project_bp.route("/<int:project_id>/members", methods=["POST"])
@admin_required
def update_members(project_id):
    project = db.get_or_404(Project, project_id)
    member_ids = request.form.getlist("member_ids")
    errors, members = _validate_project_input(
        project.title,
        project.description,
        member_ids,
        project.creator,
    )

    if errors:
        for error in errors:
            flash(error, "danger")
        return redirect(url_for("projects.project_detail", project_id=project.id))

    if not members:
        members = [project.creator]

    project.members = members

    try:
        db.session.commit()
        flash("Project team updated.", "success")
    except Exception:
        db.session.rollback()
        flash("Unable to update the project team.", "danger")

    return redirect(url_for("projects.project_detail", project_id=project.id))


@project_bp.route("/<int:project_id>/delete", methods=["POST"])
@admin_required
def delete_project(project_id):
    project = db.get_or_404(Project, project_id)

    try:
        db.session.delete(project)
        db.session.commit()
        flash("Project deleted successfully.", "success")
    except Exception:
        db.session.rollback()
        flash("Unable to delete the project.", "danger")

    return redirect(url_for("projects.project_list"))


@project_bp.route("/api/list")
@login_required
def project_api_list():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return jsonify([project.to_dict() for project in projects])
