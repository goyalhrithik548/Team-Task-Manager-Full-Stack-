from datetime import date, timedelta

from team_task_manager import create_app
from team_task_manager.extensions import db
from team_task_manager.models import Project, Task, TaskStatus, User, UserRole


app = create_app()


def create_user(full_name, email, password, role):
    user = User.query.filter_by(email=email).first()
    if user:
        return user

    user = User(full_name=full_name, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.flush()
    return user


with app.app_context():
    db.create_all()

    admin = create_user(
        "Admin User",
        "admin@example.com",
        "admin123",
        UserRole.ADMIN.value,
    )
    member_one = create_user(
        "Aisha Khan",
        "aisha@example.com",
        "member123",
        UserRole.MEMBER.value,
    )
    member_two = create_user(
        "Rahul Verma",
        "rahul@example.com",
        "member123",
        UserRole.MEMBER.value,
    )

    if Project.query.count() == 0:
        website_project = Project(
            title="Website Redesign",
            description="Refresh the landing page and improve task visibility for the team.",
            creator=admin,
        )
        website_project.members = [admin, member_one, member_two]

        api_project = Project(
            title="Client API Integration",
            description="Connect external APIs and track delivery milestones in one place.",
            creator=admin,
        )
        api_project.members = [admin, member_one]

        db.session.add_all([website_project, api_project])
        db.session.flush()

        db.session.add_all(
            [
                Task(
                    title="Create wireframes",
                    description="Draft homepage and dashboard wireframes.",
                    status=TaskStatus.IN_PROGRESS.value,
                    due_date=date.today() + timedelta(days=2),
                    assignee=member_one,
                    project=website_project,
                ),
                Task(
                    title="Review old content",
                    description="List outdated sections that must be removed.",
                    status=TaskStatus.TODO.value,
                    due_date=date.today() - timedelta(days=1),
                    assignee=member_two,
                    project=website_project,
                ),
                Task(
                    title="Set up API keys",
                    description="Prepare credentials and environment values for the integration.",
                    status=TaskStatus.DONE.value,
                    due_date=date.today() - timedelta(days=3),
                    assignee=member_one,
                    project=api_project,
                ),
            ]
        )

    db.session.commit()

    print("Seed data created successfully.")
    print("Admin login: admin@example.com / admin123")
    print("Member login: aisha@example.com / member123")
    print("Member login: rahul@example.com / member123")
