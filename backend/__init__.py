import os
from pathlib import Path
from urllib.parse import quote_plus

from flask import Flask, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


def load_env():
    env_paths = [
        Path(__file__).resolve().parent.parent / ".env",
        Path(__file__).resolve().parent / ".env",
    ]

    for env_path in env_paths:
        if not env_path.exists():
            continue

        with open(env_path, encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#") or "=" not in line:
                    continue

                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "http://localhost:3000")
FRONTEND_ORIGINS = [
    origin.strip()
    for origin in FRONTEND_ORIGIN.split(",")
    if origin.strip()
]

CORS(app, supports_credentials=True, origins=FRONTEND_ORIGINS)

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = os.environ.get(
    "SESSION_COOKIE_SAMESITE", "None"
)
app.config["SESSION_COOKIE_SECURE"] = (
    os.environ.get("SESSION_COOKIE_SECURE", "true").lower() == "true"
)

AIVEN_DB_HOST = os.environ.get("AIVEN_DB_HOST", "localhost")
AIVEN_DB_PORT = os.environ.get("AIVEN_DB_PORT", "3306")
AIVEN_DB_USER = os.environ.get("AIVEN_DB_USER", "root")
AIVEN_DB_PASSWORD = os.environ.get("AIVEN_DB_PASSWORD", "")
AIVEN_DB_NAME = os.environ.get("AIVEN_DB_NAME", "todo_list_management")
AIVEN_DB_SSL_CA = os.environ.get("AIVEN_DB_SSL_CA")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{quote_plus(AIVEN_DB_USER)}:{quote_plus(AIVEN_DB_PASSWORD)}"
    f"@{AIVEN_DB_HOST}:{AIVEN_DB_PORT}/{AIVEN_DB_NAME}?charset=utf8mb4"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

if AIVEN_DB_SSL_CA:
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {"ssl": {"ca": AIVEN_DB_SSL_CA}}
    }
else:
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"connect_args": {"ssl": {}}}

db = SQLAlchemy(app=app)
login = LoginManager(app=app)


@login.unauthorized_handler
def unauthorized():
    return jsonify({"ok": False, "error": "Vui lòng đăng nhập"}), 401
