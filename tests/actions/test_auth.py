# tests/actions/test_auth.py
from app.models import User
from tests.helpers import register_and_login


def test_login_creates_user(client, app):
    username = "alice"

    client.post("/register", data={"username": username, "password": "test123"}, follow_redirects=True)
    response = client.post("/login", data={"username": username, "password": "test123"}, follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        user = User.query.filter_by(username=username).first()
        assert user is not None


def test_logout_clears_session_and_blocks_home(client, app):
    register_and_login(client, "logoutUser")

    # logout
    client.get("/logout", follow_redirects=True)

    # home should redirect to login
    response = client.get("/home", follow_redirects=True)
    assert b"Please log in first." in response.data
    assert b"Login" in response.data
def test_logout_clears_session(client, app):
    register_and_login(client, "logoutUser")

    # Log out
    response = client.get("/logout", follow_redirects=True)

    # Should be redirected to login page
    assert b"Login" in response.data

    # Now try to access home page
    home_response = client.get("/home", follow_redirects=True)

    # Should be redirected BACK to login because session is gone
    assert b"Please log in first." in home_response.data
    assert b"Login" in home_response.data


def test_cannot_access_home_after_logout(client, app):
    register_and_login(client, "u1")

    # logout
    client.get("/logout", follow_redirects=True)

    # Try accessing /home
    response = client.get("/home", follow_redirects=True)

    assert b"Please log in first." in response.data
    assert b"Login" in response.data


def test_cannot_access_tasks_after_logout(client, app):
    username = register_and_login(client, "u2")

    # logout
    client.get("/logout", follow_redirects=True)

    response = client.get(f"/tasks/{username}", follow_redirects=True)

    assert b"Please log in first." in response.data
    assert b"Login" in response.data


def test_cannot_access_create_task_after_logout(client, app):
    username = register_and_login(client, "u3")

    # logout
    client.get("/logout", follow_redirects=True)

    response = client.get(f"/new-task/{username}", follow_redirects=True)

    assert b"Please log in first." in response.data
    assert b"Login" in response.data


def test_cannot_access_edit_task_after_logout(client, app):
    username = register_and_login(client, "u4")

    # Log out
    client.get("/logout", follow_redirects=True)

    # Try to access the edit page with any task_id (1 is fine)
    response = client.get(
        f"/edit-task/{username}/1",
        follow_redirects=True,
    )

    # Because of @login_required, we should be redirected to login
    assert b"Please log in first." in response.data
    assert b"Login" in response.data