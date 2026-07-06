def test_health_check(test_client):
    response = test_client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_profile_requires_login(test_client):
    response = test_client.get("/api/profile")

    assert response.status_code == 401
    assert response.get_json()["ok"] is False


def test_register_success_creates_user(test_client):
    response = test_client.post(
        "/api/register",
        json={
            "name": "New User",
            "email": "new@example.com",
            "username": "newuser",
            "password": "secret123",
            "confirm": "secret123",
        },
    )

    data = response.get_json()

    assert response.status_code == 201
    assert data["ok"] is True
    assert data["user"]["username"] == "newuser"


def test_register_invalid_payload_returns_error(test_client):
    response = test_client.post(
        "/api/register",
        json={
            "name": "",
            "email": "bad-email",
            "username": "",
            "password": "123",
            "confirm": "456",
        },
    )

    data = response.get_json()

    assert response.status_code == 400
    assert data["ok"] is False
    assert "error" in data


def test_login_success_sets_session_and_profile_returns_user(test_client, sample_user):
    login_response = test_client.post(
        "/api/login",
        json={"username": sample_user.username, "password": "demo123"},
    )

    assert login_response.status_code == 200
    assert login_response.get_json()["user"]["username"] == sample_user.username

    profile_response = test_client.get("/api/profile")

    assert profile_response.status_code == 200
    assert profile_response.get_json()["user"]["username"] == sample_user.username


def test_login_failure_returns_unauthorized(test_client, sample_user):
    response = test_client.post(
        "/api/login",
        json={"username": sample_user.username, "password": "wrong123"},
    )

    data = response.get_json()

    assert response.status_code == 401
    assert data["ok"] is False
    assert "error" in data


def test_logout_clears_profile_session(test_client, sample_user):
    test_client.post("/api/login", json={"username": sample_user.username, "password": "demo123"})

    logout_response = test_client.post("/api/logout")
    profile_response = test_client.get("/api/profile")

    assert logout_response.status_code == 200
    assert logout_response.get_json()["ok"] is True
    assert profile_response.status_code == 401


def test_list_todos_requires_login(test_client):
    response = test_client.get("/api/todos")

    assert response.status_code == 401
    assert response.get_json()["ok"] is False


def test_list_todos_returns_current_user_items(test_client, login_user, sample_user, sample_todos):
    login_user(test_client, sample_user)

    response = test_client.get("/api/todos")
    data = response.get_json()

    assert response.status_code == 200
    assert data["total"] == 2
    assert data["stats"] == {"total": 2, "completed": 1, "active": 1}
    assert all(item["user_id"] == sample_user.id for item in data["items"])


def test_create_todo_validation_error(test_client, login_user, sample_user):
    login_user(test_client, sample_user)

    response = test_client.post("/api/todos", json={"title": ""})

    assert response.status_code == 400
    assert "errors" in response.get_json()


def test_create_update_toggle_and_delete_todo(test_client, login_user, sample_user):
    login_user(test_client, sample_user)

    create_response = test_client.post(
        "/api/todos",
        json={"title": "Write API tests", "description": "Use Flask client"},
    )
    created = create_response.get_json()

    assert create_response.status_code == 201
    assert created["title"] == "Write API tests"
    assert created["user_id"] == sample_user.id

    update_response = test_client.put(
        f"/api/todos/{created['id']}",
        json={"title": "Update API tests", "description": ""},
    )
    updated = update_response.get_json()

    assert update_response.status_code == 200
    assert updated["title"] == "Update API tests"
    assert updated["description"] is None

    toggle_response = test_client.patch(f"/api/todos/{created['id']}/toggle")
    toggled = toggle_response.get_json()

    assert toggle_response.status_code == 200
    assert toggled["is_completed"] is True

    delete_response = test_client.delete(f"/api/todos/{created['id']}")

    assert delete_response.status_code == 200
    assert delete_response.get_json()["message"] == "Todo deleted successfully"


def test_user_cannot_access_other_user_todo(test_client, login_user, sample_user, another_user, sample_todos):
    login_user(test_client, sample_user)
    other_todo = next(todo for todo in sample_todos if todo.user_id == another_user.id)

    response = test_client.get(f"/api/todos/{other_todo.id}")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Todo not found"
