"""Test the site's database."""
# import pytest
from run import application, db


def test_db_uses_SQLAlchemy():
    """Makes sure db is an SQLAlchemy object."""
    assert('SQLAlchemy' in repr(db))


def test_db_URI_set():
    """Makes sure the db's URI was set."""
    uri = application.config['SQLALCHEMY_DATABASE_URI']
    assert(uri != 'sqlite:///:memory:')


def test_db_track_mods_false():
    """Makes sure the db does not track modifications."""
    assert(not application.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
