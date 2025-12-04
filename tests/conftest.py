import sys
import os
import pytest
from dotenv import load_dotenv

# Add project root to sys.path so "app" can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load environment variables (optional)
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env.testing"))
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # In-memory DB
        "SECRET_KEY": "test-secret-key"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
