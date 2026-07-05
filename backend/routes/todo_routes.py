from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from backend import db
from backend.dao import todo_dao
from backend.utils.validator import validate_todo


todo_bp = Blueprint("todo", __name__, url_prefix="/api")


@todo_bp.get("/health")
def health_check():
    return jsonify({"status": "ok"})


@todo_bp.get("/todos")
@login_required
def list_todos():
    keyword = request.args.get("keyword", "").strip()
    status = normalize_status(request.args.get("status", "all"))
    sort = normalize_sort(request.args.get("sort", "newest"))
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 8, type=int)

    todos = todo_dao.get_todos(
        user_id=current_user.id,
        keyword=keyword,
        status=status,
        sort=sort,
        page=max(page, 1),
        per_page=min(max(per_page, 1), 50),
    )

    return jsonify(
        {
            "items": [todo_dao.todo_to_dict(todo) for todo in todos.items],
            "page": todos.page,
            "pages": todos.pages,
            "per_page": todos.per_page,
            "total": todos.total,
            "has_next": todos.has_next,
            "has_prev": todos.has_prev,
            "stats": get_stats(current_user.id),
        }
    )


@todo_bp.get("/todos/<int:todo_id>")
@login_required
def get_todo(todo_id):
    todo = todo_dao.get_by_id(todo_id, current_user.id)

    if todo is None:
        return jsonify({"error": "Todo not found"}), 404

    return jsonify(todo_dao.todo_to_dict(todo))


@todo_bp.post("/todos")
@login_required
def create_todo():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "")
    description = data.get("description", "")
    errors = validate_todo(title, description)

    if errors:
        return jsonify({"errors": errors}), 400

    todo = todo_dao.create_todo(current_user.id, title, description)
    return jsonify(todo_dao.todo_to_dict(todo)), 201


@todo_bp.put("/todos/<int:todo_id>")
@login_required
def update_todo(todo_id):
    todo = todo_dao.get_by_id(todo_id, current_user.id)

    if todo is None:
        return jsonify({"error": "Todo not found"}), 404

    data = request.get_json(silent=True) or {}
    title = data.get("title", "")
    description = data.get("description", "")
    errors = validate_todo(title, description)

    if errors:
        return jsonify({"errors": errors}), 400

    todo = todo_dao.update_todo(todo, title, description)
    return jsonify(todo_dao.todo_to_dict(todo))


@todo_bp.patch("/todos/<int:todo_id>/toggle")
@login_required
def toggle_todo(todo_id):
    todo = todo_dao.get_by_id(todo_id, current_user.id)

    if todo is None:
        return jsonify({"error": "Todo not found"}), 404

    todo = todo_dao.toggle_todo(todo)
    return jsonify(todo_dao.todo_to_dict(todo))


@todo_bp.delete("/todos/<int:todo_id>")
@login_required
def delete_todo(todo_id):
    todo = todo_dao.get_by_id(todo_id, current_user.id)

    if todo is None:
        return jsonify({"error": "Todo not found"}), 404

    todo_dao.delete_todo(todo)
    return jsonify({"message": "Todo deleted successfully"})


@todo_bp.errorhandler(SQLAlchemyError)
def handle_database_error(error):
    db.session.rollback()
    print(f"Database error: {error}")
    return jsonify({"error": "Database error"}), 500


def normalize_status(status):
    return status if status in ("all", "active", "completed") else "all"


def normalize_sort(sort):
    return sort if sort in ("newest", "oldest", "title", "status") else "newest"


def get_stats(user_id):
    return {
        "total": todo_dao.count_all(user_id),
        "completed": todo_dao.count_completed(user_id),
        "active": todo_dao.count_active(user_id),
    }