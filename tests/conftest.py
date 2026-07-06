from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend import app, db
import backend.app  # noqa: F401 - register blueprints and Flask-Login user loader
from backend.models import Todo, User, UserRole
from backend.utils import hash_password


@pytest.fixture
def test_app():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {}
    app.secret_key = "test-secret-key"

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
        db.engine.dispose()


@pytest.fixture
def test_client(test_app):
    return test_app.test_client()


@pytest.fixture
def test_session(test_app):
    yield db.session
    db.session.rollback()
    db.session.remove()


@pytest.fixture
def sample_user(test_session):
    user = User(
        name="Demo User",
        email="demo@example.com",
        username="demo",
        password=hash_password("demo123"),
        user_role=UserRole.USER,
    )
    test_session.add(user)
    test_session.commit()
    return user


@pytest.fixture
def another_user(test_session):
    user = User(
        name="Other User",
        email="other@example.com",
        username="other",
        password=hash_password("other123"),
        user_role=UserRole.USER,
    )
    test_session.add(user)
    test_session.commit()
    return user


@pytest.fixture
def sample_todos(test_session, sample_user, another_user):
    todos = [
        Todo(user_id=sample_user.id, title="Write README", description="Document setup", is_completed=False),
        Todo(user_id=sample_user.id, title="Review code", description="Check API", is_completed=True),
        Todo(user_id=another_user.id, title="Private task", description="Other user todo", is_completed=False),
    ]
    test_session.add_all(todos)
    test_session.commit()
    return todos


@pytest.fixture
def login_user():
    def _login_user(client, user):
        with client.session_transaction() as session:
            session["_user_id"] = str(user.id)
            session["_fresh"] = True

    return _login_user
