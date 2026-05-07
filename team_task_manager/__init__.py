from flask import Flask, g, render_template, session

from config import Config

from .extensions import db
from .models import TaskStatus, User
from .routes.api import api_bp
from .routes.auth import auth_bp
from .routes.main import main_bp
from .routes.projects import project_bp
from .routes.tasks import task_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(api_bp)

    @app.before_request
    def load_current_user():
        g.current_user = None
        user_id = session.get("user_id")

        if user_id:
            g.current_user = db.session.get(User, user_id)

        if user_id and g.current_user is None:
            session.clear()

    @app.context_processor
    def inject_template_data():
        return {
            "current_user": g.get("current_user"),
            "task_statuses": [status.value for status in TaskStatus],
        }

    @app.errorhandler(403)
    def forbidden(_error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(_error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(_error):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    with app.app_context():
        db.create_all()

    return app
