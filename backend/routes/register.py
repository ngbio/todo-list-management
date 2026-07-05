from flask import Blueprint, jsonify, request

import backend.dao.users as users_dao


register_bp = Blueprint("register", __name__, url_prefix="/api")


@register_bp.route("/register", methods=["POST"])
def register_process():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")
    confirm = data.get("confirm")
    name = data.get("name")
    email = data.get("email")

    try:
        user = users_dao.add_user(
            name=name,
            email=email,
            username=username,
            password=password,
            confirm=confirm,
        )

        return jsonify({
            "ok": True,
            "message": "Đăng ký thành công! Vui lòng đăng nhập.",
            "user": users_dao.user_to_dict(user),
        }), 201
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    except Exception as ex:
        print(ex)
        return jsonify({"ok": False, "error": " lỗi hệ thống, vui lòng thử lại sau!"}), 500