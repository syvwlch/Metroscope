"""Test the site's database."""
import pytest
from flask import current_app
from run import create_app, db


@pytest.fixture
def app():
    """Set up and tear down the test app and db."""
    app = create_app('testing')

    app.config['TESTING'] = True

    app_context = app.app_context()
    app_context.push()
    db.create_all()

    yield app

    db.session.remove()
    db.drop_all()
    app_context.pop()


def test_app_exists(app):
    """Makes sure the test app exists."""
    assert current_app is not None


def test_app_is_testing(app):
    """Makes sure the test app is configured for testing."""
    assert current_app.config['TESTING']


def test_db_uses_SQLAlchemy(app):
    """Makes sure db is an SQLAlchemy object."""
    assert 'SQLAlchemy' in repr(db)


def test_db_track_mods_false(app):
    """Makes sure the db does not track modifications."""
    assert not current_app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
