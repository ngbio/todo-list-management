import pytest

from backend.dao.users import add_user, auth_user, get_current_user, validate_email, validate_password
from backend.models import User
from backend.utils import hash_password


def test_add_user_success(test_session):
    add_user(
        name="Nguyen Van A",
        email="nva@example.com",
        username="nguyenvana",
        password="secret123",
        confirm="secret123",
    )

    user = User.query.filter(User.username == "nguyenvana").first()

    assert user is not None
    assert user.name == "Nguyen Van A"
    assert user.email == "nva@example.com"
    assert user.password == hash_password("secret123")
    assert user.active is True


def test_add_user_rejects_existing_username(test_session, sample_user):
    with pytest.raises(ValueError):
        add_user(
            name="Another Demo",
            email="another@example.com",
            username=sample_user.username,
            password="secret123",
            confirm="secret123",
        )


@pytest.mark.parametrize(
    "email, expected",
    [
        ("valid@example.com", True),
        ("", True),
        (None, True),
        ("invalid-email", False),
    ],
)
def test_validate_email(email, expected):
    valid, message = validate_email(email)

    assert valid is expected
    assert message


@pytest.mark.parametrize("password", ["", "12345"])
def test_validate_password_rejects_short_password(password):
    valid, message = validate_password(password, password)

    assert valid is False
    assert message


def test_validate_password_rejects_confirm_mismatch():
    valid, message = validate_password("secret123", "different")

    assert valid is False
    assert message


def test_auth_user_success(sample_user):
    result = auth_user("demo", "demo123")

    assert result is not None
    assert result.username == sample_user.username


def test_auth_user_wrong_password(sample_user):
    result = auth_user("demo", "wrong123")

    assert result is None


def test_get_current_user(sample_user):
    result = get_current_user(sample_user.id)

    assert result.username == sample_user.username
