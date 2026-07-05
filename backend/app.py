from backend import app, login
from backend.dao.users import get_current_user
from backend.routes.login_logout import login_logout_bp
from backend.routes.register import register_bp
from backend.routes.todo_routes import todo_bp


@login.user_loader
def load_user(user_id):
    return get_current_user(user_id)


def register_api():
    app.register_blueprint(login_logout_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(todo_bp)


register_api()


if __name__ == "__main__":
    app.run(debug=True)