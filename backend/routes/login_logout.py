from flask import Blueprint, jsonify, request
from flask_login import current_user, login_user, logout_user

from backend.dao.users import auth_user, user_to_dict


login_logout_bp = Blueprint("login_logout", __name__, url_prefix="/api")


@login_logout_bp.route("/login", methods=["POST"])
def login_process():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")
    user = auth_user(username, password)

    if user:
        login_user(user)
        return jsonify({"ok": True, "user": user_to_dict(user)})

    return jsonify({"ok": False, "error": "Tên đăng nhập hoặc mật khẩu không chính xác!"}), 401


@login_logout_bp.route("/logout", methods=["POST"])
def logout_process():
    logout_user()
    return jsonify({"ok": True, "message": "Đăng xuất thành công"})


@login_logout_bp.route("/profile")
def profile_view():
    if not current_user.is_authenticated:
        return jsonify({"ok": False, "user": None}), 401

    return jsonify({"ok": True, "user": user_to_dict(current_user)})