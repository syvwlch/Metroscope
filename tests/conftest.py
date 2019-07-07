"""Configure shared resources for entire test suite."""

import pytest
from run.models import reset_db


@pytest.fixture
def app():
    """Set up and tear down the test app."""
    from run import create_app, db
    from flask_migrate import Migrate

    app = create_app('testing')
    Migrate(app, db)

    app.config['TESTING'] = True

    app_context = app.app_context()
    app_context.push()
    db.create_all()

    yield app

    db.session.remove()
    db.drop_all()
    app_context.pop()


@pytest.fixture
def client(app):
    """Set up and tear down a test client with some samples in the db."""
    reset_db()
    yield app.test_client()


@pytest.fixture
def client_empty_db(app):
    """Set up and tear down a test client with an empty db."""
    yield app.test_client()
