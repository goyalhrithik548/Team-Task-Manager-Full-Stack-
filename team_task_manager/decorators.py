from functools import wraps

from flask import flash, g, redirect, session, url_for


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))

        return view_func(*args, **kwargs)

    return wrapped_view


def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapped_view(*args, **kwargs):
        if not g.current_user or not g.current_user.is_admin():
            flash("Only admins can perform that action.", "danger")
            return redirect(url_for("main.dashboard"))

        return view_func(*args, **kwargs)

    return wrapped_view
