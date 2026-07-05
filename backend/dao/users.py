import re

from backend import db
from backend.models import User, UserRole
from backend.utils import hash_password


def validate_password(password, confirm_password=None):
    if not password or len(password) < 6:
        return False, "Mat khau phai co it nhat 6 ky tu!"

    if confirm_password and password != confirm_password:
        return False, "Mat khau xac nhan khong khop!"

    return True, "OK"


def validate_name(name):
    if not name or not name.strip():
        return False, "Ho ten khong duoc de trong!"

    return True, "OK"


def validate_username(username):
    if not username or not username.strip():
        return False, "Ten dang nhap khong duoc de trong!"

    return True, "OK"


def validate_email(email):
    if not email:
        return True, "OK"

    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if not re.match(pattern, email.strip()):
        return False, "Email khong hop le!"

    return True, "OK"


def get_current_user(user_id):
    return db.session.get(User, int(user_id))


def auth_user(username, password):
    password = hash_password(password)
    return User.query.filter(User.username == username, User.password == password).first()


def add_user(name, email, username, password, confirm):
    valid, msg = validate_name(name)
    if not valid:
        raise ValueError(msg)

    valid, msg = validate_username(username)
    if not valid:
        raise ValueError(msg)

    valid, msg = validate_email(email)
    if not valid:
        raise ValueError(msg)

    valid, msg = validate_password(password, confirm)
    if not valid:
        raise ValueError(msg)

    if User.query.filter(User.username == username.strip()).first():
        raise ValueError("Username da ton tai!")

    password = hash_password(password)

    user = User(
        name=name.strip(),
        email=email.strip() if email else None,
        username=username.strip(),
        password=password,
        user_role=UserRole.USER,
    )

    db.session.add(user)
    db.session.commit()

    return user


def user_to_dict(user):
    return user.to_dict()