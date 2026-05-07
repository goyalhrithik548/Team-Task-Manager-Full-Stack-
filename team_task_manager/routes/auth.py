import re

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from ..decorators import login_required
from ..extensions import db
from ..models import User, UserRole


auth_bp = Blueprint("auth", __name__)

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if session.get("user_id"):
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        errors = []

        if not full_name:
            errors.append("Full name is required.")
        if not email or not EMAIL_PATTERN.match(email):
            errors.append("Please enter a valid email address.")
        if len(password) < 6:
            errors.append("Password must be at least 6 characters long.")
        if password != confirm_password:
            errors.append("Passwords do not match.")
        if User.query.filter_by(email=email).first():
            errors.append("An account with that email already exists.")

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template("auth/signup.html")

        user = User(full_name=full_name, email=email, role=UserRole.MEMBER.value)
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash("Something went wrong while creating your account.", "danger")
            return render_template("auth/signup.html")

        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password.", "danger")
            return render_template("auth/login.html")

        session.clear()
        session["user_id"] = user.id
        session.permanent = True

        flash(f"Welcome back, {user.full_name}.", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("auth/login.html")


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
