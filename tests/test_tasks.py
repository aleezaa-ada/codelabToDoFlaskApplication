from app.models import User, Todo


def register_and_login(client, username="alice", password="test123"):
    """Helper to register + log in a user."""
    client.post("/register", data={
        "username": username,
        "password": password
    }, follow_redirects=True)

    client.post("/login", data={
        "username": username,
        "password": password
    }, follow_redirects=True)

    return username


def test_login_creates_user(client, app):
    username = "alice"

    # Register user first
    client.post("/register", data={"username": username, "password": "test123"}, follow_redirects=True)

    # Then login
    response = client.post("/login", data={"username": username, "password": "test123"}, follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        user = User.query.filter_by(username=username).first()
        assert user is not None


def test_create_and_view_task(client, app):
    username = register_and_login(client, "alice")

    # Create a new task
    response = client.post(f"/new-task/{username}", data={"title": "Test Task"}, follow_redirects=True)
    assert b"Test Task" in response.data

    # Check DB
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        assert len(user.todos) == 1
        assert user.todos[0].title == "Test Task"


def test_create_task_empty_title(client, app):
    username = register_and_login(client, "bob")

    # Submit empty title
    client.post(f"/new-task/{username}", data={"title": ""}, follow_redirects=True)

    with app.app_context():
        user = User.query.filter_by(username=username).first()
        # Validation should prevent task creation
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

    # Create task
    client.post(f"/new-task/{username}", data={"title": "Old Task"}, follow_redirects=True)

    with app.app_context():
        task = Todo.query.filter_by(title="Old Task").first()
        assert task is not None

    # Update it
    response = client.post(
        f"/edit-task/{username}/{task.id}",
        data={"title": "Updated Task", "completed": False},
        follow_redirects=True
    )

    assert b"Updated Task" in response.data


def test_delete_task(client, app):
    username = register_and_login(client, "eve")

    # Create task
    client.post(f"/new-task/{username}", data={"title": "Delete Me"}, follow_redirects=True)

    with app.app_context():
        task = Todo.query.filter_by(title="Delete Me").first()
        assert task is not None

    # Delete task
    response = client.post(
        f"/delete-task/{username}/{task.id}",
        follow_redirects=True
    )

    assert b"Delete Me" not in response.data

    with app.app_context():
        deleted = Todo.query.filter_by(title="Delete Me").first()
        assert deleted is None
