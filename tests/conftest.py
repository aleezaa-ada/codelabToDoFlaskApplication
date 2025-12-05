import pytest
from dotenv import load_dotenv
from app import create_app, db

load_dotenv()

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # In-memory DB
        "SECRET_KEY": "test-secret-key",
        "WTF_CSRF_ENABLED": False, 

    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
