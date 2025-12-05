# tests/helpers.py
from app.models import User, Todo

def register_and_login(client, username="alice", password="test123"):
    client.post("/register", data={
        "username": username,
        "password": password,
    }, follow_redirects=True)

    client.post("/login", data={
        "username": username,
        "password": password,
    }, follow_redirects=True)

    return username
