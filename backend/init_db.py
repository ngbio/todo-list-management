try:
    from sqlalchemy import inspect, text

    from backend import AIVEN_DB_HOST, AIVEN_DB_NAME, app, db
    from backend.dao.users import add_user
    from backend.models import Todo, User
except ModuleNotFoundError:
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from sqlalchemy import inspect, text

    from backend import AIVEN_DB_HOST, AIVEN_DB_NAME, app, db
    from backend.dao.users import add_user
    from backend.models import Todo, User


DEMO_USER = {
    "name": "Demo User",
    "email": "demo@example.com",
    "username": "demo",
    "password": "123456",
}


def ensure_todo_columns():
    inspector = inspect(db.engine)

    if not inspector.has_table("todo"):
        return

    columns = [column["name"] for column in inspector.get_columns("todo")]

    if "active" not in columns:
        db.session.execute(text("ALTER TABLE todo ADD COLUMN active BOOL DEFAULT true"))

    if "user_id" not in columns:
        db.session.execute(text("DELETE FROM todo"))
        db.session.execute(text("ALTER TABLE todo ADD COLUMN user_id INT NOT NULL"))
        db.session.execute(text("CREATE INDEX idx_todo_user_id ON todo (user_id)"))

    db.session.commit()


def create_sample_user():
    user = User.query.filter(User.username == DEMO_USER["username"]).first()

    if user:
        return user

    return add_user(
        name=DEMO_USER["name"],
        email=DEMO_USER["email"],
        username=DEMO_USER["username"],
        password=DEMO_USER["password"],
        confirm=DEMO_USER["password"],
    )


def create_sample_data(user):
    if Todo.query.filter(Todo.user_id == user.id).first():
        return

    todos = [
        Todo(
            user_id=user.id,
            title="Phân tích yêu cầu Todo List",
            description="Liệt kê chức năng CRUD, tìm kiếm, lọc trạng thái và validate.",
            is_completed=True,
        ),
        Todo(
            user_id=user.id,
            title="Thiết kế giao diện ReactJS",
            description="Xây dựng layout responsive bằng CSS custom, form thêm/sửa và danh sách công việc.",
        ),
        Todo(
            user_id=user.id,
            title="Viết README hướng dẫn chạy",
            description="Hướng dẫn cài đặt, cấu hình Aiven MySQL, khởi tạo database và chạy ứng dụng local.",
        ),
    ]

    db.session.add_all(todos)


def init_db():
    with app.app_context():
        print(f"Using database: {AIVEN_DB_NAME} on {AIVEN_DB_HOST}")
        db.create_all()
        ensure_todo_columns()
        user = create_sample_user()
        create_sample_data(user)
        db.session.commit()
        print(f"Users: {User.query.count()}")
        print(f"Todos: {Todo.query.count()}")


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")