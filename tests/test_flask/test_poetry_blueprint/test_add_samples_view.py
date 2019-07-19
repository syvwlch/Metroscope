"""Test the add_samples view using flask's test_client()."""
from run import db


def test_dropped_db(client):
    """Check behavior when the db has no tables."""
    db.drop_all()
    assert b'Sorry' in client.get('/poetry/poem').data
    assert "404" in client.get('/poetry/poem/Flea').status
    # /add_samples route should not cause server error when db has no tables
    assert "404" in client.get('/poetry/add_samples').status


def test_add_samples_route(client):
    """Check the /add_samples route."""
    # The database has tables in it
    assert "poems" in db.engine.table_names()
    # The database has no poems in it
    assert b'Sorry' in client.get('/poetry/poem').data
    assert "404" in client.get('/poetry/poem/Flea').status

    # /add_samples route injects sample poems into database
    client.get('/poetry/add_samples')
    assert b'Flea' in client.get('/poetry/poem').data
    response = client.get('/poetry/poem/Flea')
    assert b'Flea' in response.data
    assert "200" in response.status
    assert "404" in client.get('/poetry/poem/foo').status

    # Makes sure doing it twice doesn't break anything.
    client.get('/poetry/add_samples')
    assert b'Flea' in client.get('/poetry/poem').data
    response = client.get('/poetry/poem/Flea')
    assert b'Flea' in response.data
    assert "200" in response.status
    assert "404" in client.get('/poetry/poem/foo').status
