from app.models import User, Todo

def test_login_creates_user(client, app):
    response = client.post("/login", data={"nm": "alice"}, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        user = User.query.filter_by(username="alice").first()
        assert user is not None

def test_create_and_view_task(client, app):
    # Create a user
    client.post("/login", data={"nm": "alice"}, follow_redirects=True)

    # Create a new task
    response = client.post("/new-task/alice", data={"title": "Test Task"}, follow_redirects=True)

    # check that the task appears in the HTML
    assert b"Test Task" in response.data

    # Check in the DB as well
    with app.app_context():
        user = User.query.filter_by(username="alice").first()
        assert len(user.todos) == 1
        assert user.todos[0].title == "Test Task"

def test_create_task_empty_title(client, app):
    client.post("/login", data={"nm": "bob"}, follow_redirects=True)
    client.post("/new-task/bob", data={"title": ""}, follow_redirects=True)
    
    with app.app_context():
        user = User.query.filter_by(username="bob").first()
        assert len(user.todos) == 0

def test_view_tasks(client, app):
    client.post("/login", data={"nm": "carol"}, follow_redirects=True)
    client.post("/new-task/carol", data={"title": "Task 1"}, follow_redirects=True)
    client.post("/new-task/carol", data={"title": "Task 2"}, follow_redirects=True)
    response = client.get("/tasks/carol")
    assert b"Task 1" in response.data
    assert b"Task 2" in response.data

def test_edit_task(client, app):
    client.post("/login", data={"nm": "dave"}, follow_redirects=True)
    client.post("/new-task/dave", data={"title": "Old Task"}, follow_redirects=True)
    
    with app.app_context():
        task = Todo.query.filter_by(title="Old Task").first()
    
    response = client.post(f"/edit-task/dave/{task.id}", data={"title": "Updated Task"}, follow_redirects=True)
    assert b"Updated Task" in response.data

def test_delete_task(client, app):
    client.post("/login", data={"nm": "eve"}, follow_redirects=True)
    client.post("/new-task/eve", data={"title": "Delete Me"}, follow_redirects=True)
    
    with app.app_context():
        task = Todo.query.filter_by(title="Delete Me").first()
    
    response = client.post(f"/delete-task/eve/{task.id}", follow_redirects=True)

    # Ensure the deleted task no longer appears in the page
    assert b"Delete Me" not in response.data
    with app.app_context():
        deleted = Todo.query.filter_by(title="Delete Me").first()
        assert deleted is None
