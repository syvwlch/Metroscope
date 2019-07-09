"""Test the add_samples view using flask's test_client()."""
from run import db


def test_dropped_db(client):
    """Check behavior when the db has no tables."""
    db.drop_all()
    assert b'Sorry' in client.get('/').data
    assert "404" in client.get('/poem/Flea').status
    # /reset route causes server error when db has no tables


def test_add_samples_route(client_empty_db):
    """Check the /add_samples route."""
    # The database has tables in it
    assert "poems" in db.engine.table_names()
    # The database has no poems in it
    assert b'Sorry' in client_empty_db.get('/').data
    assert "404" in client_empty_db.get('/poem/Flea').status

    # /add_samples route injects sample poems into database
    client_empty_db.get('/add_samples')
    assert b'Flea' in client_empty_db.get('/').data
    response = client_empty_db.get('/poem/Flea')
    assert b'Flea' in response.data
    assert "200" in response.status
    assert "404" in client_empty_db.get('/poem/foo').status

    # Makes sure doing it twice doesn't break anything.
    client_empty_db.get('/add_samples')
    assert b'Flea' in client_empty_db.get('/').data
    response = client_empty_db.get('/poem/Flea')
    assert b'Flea' in response.data
    assert "200" in response.status
    assert "404" in client_empty_db.get('/poem/foo').status
