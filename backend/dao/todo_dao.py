from sqlalchemy import case, or_

from backend import db
from backend.models import Todo


def get_todos(user_id, keyword=None, status="all", sort="newest", page=1, per_page=8):
    query = Todo.query.filter(Todo.user_id == user_id)

    if keyword:
        search_value = f"%{keyword.strip()}%"
        query = query.filter(
            or_(
                Todo.title.ilike(search_value),
                Todo.description.ilike(search_value),
            )
        )

    if status == "completed":
        query = query.filter(Todo.is_completed.is_(True))
    elif status == "active":
        query = query.filter(Todo.is_completed.is_(False))

    if sort == "oldest":
        query = query.order_by(Todo.created_at.asc())
    elif sort == "title":
        query = query.order_by(Todo.title.asc())
    elif sort == "status":
        query = query.order_by(
            case((Todo.is_completed.is_(False), 0), else_=1),
            Todo.created_at.desc(),
        )
    else:
        query = query.order_by(Todo.created_at.desc())

    return query.paginate(page=page, per_page=per_page, error_out=False)


def get_by_id(todo_id, user_id=None):
    todo = db.session.get(Todo, todo_id)

    if todo is None:
        return None

    if user_id is not None and todo.user_id != user_id:
        return None

    return todo


def create_todo(user_id, title, description=None):
    todo = Todo(
        user_id=user_id,
        title=title.strip(),
        description=clean_description(description),
    )
    db.session.add(todo)
    db.session.commit()
    return todo


def update_todo(todo, title, description=None):
    todo.title = title.strip()
    todo.description = clean_description(description)
    db.session.commit()
    return todo


def toggle_todo(todo):
    todo.is_completed = not todo.is_completed
    db.session.commit()
    return todo


def delete_todo(todo):
    db.session.delete(todo)
    db.session.commit()


def count_all(user_id):
    return Todo.query.filter(Todo.user_id == user_id).count()


def count_completed(user_id):
    return Todo.query.filter(
        Todo.user_id == user_id,
        Todo.is_completed.is_(True),
    ).count()


def count_active(user_id):
    return Todo.query.filter(
        Todo.user_id == user_id,
        Todo.is_completed.is_(False),
    ).count()


def todo_to_dict(todo):
    return todo.to_dict()


def clean_description(description):
    if description is None:
        return None

    description = description.strip()
    return description or None