"""Test the site's database configuration."""
from flask import current_app
from run import db


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
