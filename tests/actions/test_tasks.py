# tests/actions/test_tasks.py
from app.models import User, Todo
from tests.helpers import register_and_login


def test_create_and_view_task(client, app):
    username = register_and_login(client, "alice")

    response = client.post(f"/new-task/{username}", data={"title": "Test Task"}, follow_redirects=True)
    assert b"Test Task" in response.data

    with app.app_context():
        user = User.query.filter_by(username=username).first()
        assert len(user.todos) == 1
        assert user.todos[0].title == "Test Task"


def test_create_task_empty_title(client, app):
    username = register_and_login(client, "bob")

    client.post(f"/new-task/{username}", data={"title": ""}, follow_redirects=True)

    with app.app_context():
        user = User.query.filter_by(username=username).first()
        assert len(user.todos) == 0


def test_view_tasks(client, app):
    username = register_and_login(client, "carol")

    client.post(f"/new-task/{username}", data={"title": "Task 1"}, follow_redirects=True)
    client.post(f"/new-task/{username}", data={"title": "Task 2"}, follow_redirects=True)

    response = client.get(f"/tasks/{username}")
    assert b"Task 1" in response.data
    assert b"Task 2" in response.data


def test_edit_task(client, app):
    username = register_and_login(client, "dave")

    client.post(f"/new-task/{username}", data={"title": "Old Task"}, follow_redirects=True)

    with app.app_context():
        task = Todo.query.filter_by(title="Old Task").first()
        assert task is not None

    response = client.post(
        f"/edit-task/{username}/{task.id}",
        data={"title": "Updated Task", "completed": False},
        follow_redirects=True,
    )
    assert b"Updated Task" in response.data


def test_delete_task(client, app):
    username = register_and_login(client, "eve")

    client.post(f"/new-task/{username}", data={"title": "Delete Me"}, follow_redirects=True)

    with app.app_context():
        task = Todo.query.filter_by(title="Delete Me").first()
        assert task is not None

    response = client.post(
        f"/delete-task/{username}/{task.id}",
        follow_redirects=True,
    )

    assert b"Delete Me" not in response.data

    with app.app_context():
        deleted = Todo.query.filter_by(title="Delete Me").first()
        assert deleted is None
