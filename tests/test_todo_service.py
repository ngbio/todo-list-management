from backend.dao import todo_dao
from backend.models import Todo


def test_create_todo_trims_title_and_description(test_session, sample_user):
    todo = todo_dao.create_todo(sample_user.id, "  Write tests  ", "  Cover services  ")

    assert todo.id is not None
    assert todo.user_id == sample_user.id
    assert todo.title == "Write tests"
    assert todo.description == "Cover services"
    assert todo.is_completed is False


def test_get_todos_returns_only_owner_tasks(sample_todos, sample_user):
    pagination = todo_dao.get_todos(user_id=sample_user.id)

    assert pagination.total == 2
    assert all(todo.user_id == sample_user.id for todo in pagination.items)


def test_get_todos_filters_keyword_status_and_sort(sample_todos, sample_user):
    pagination = todo_dao.get_todos(
        user_id=sample_user.id,
        keyword="review",
        status="completed",
        sort="title",
    )

    assert pagination.total == 1
    assert pagination.items[0].title == "Review code"
    assert pagination.items[0].is_completed is True


def test_get_by_id_rejects_other_user_todo(sample_todos, sample_user, another_user):
    other_todo = Todo.query.filter(Todo.user_id == another_user.id).first()

    result = todo_dao.get_by_id(other_todo.id, sample_user.id)

    assert result is None


def test_update_toggle_and_delete_todo(test_session, sample_user):
    todo = todo_dao.create_todo(sample_user.id, "Old title", "Old desc")

    updated = todo_dao.update_todo(todo, "New title", "")
    assert updated.title == "New title"
    assert updated.description is None

    toggled = todo_dao.toggle_todo(updated)
    assert toggled.is_completed is True

    todo_dao.delete_todo(toggled)
    assert todo_dao.get_by_id(toggled.id, sample_user.id) is None


def test_count_helpers(sample_todos, sample_user):
    assert todo_dao.count_all(sample_user.id) == 2
    assert todo_dao.count_completed(sample_user.id) == 1
    assert todo_dao.count_active(sample_user.id) == 1
