"""Test the major views using flask's test_client()."""
import pytest
from run import db


@pytest.mark.parametrize("route", [
    '/',
    '/about',
    ])
def test_200(client, route):
    """Check routes that should always return a 200."""
    assert "200" in client.get(route).status


@pytest.mark.parametrize("route", [
    '/foo',
    '/poem/bar',
    ])
def test_404(client, route):
    """Check routes that should always 404."""
    response = client.get(route)
    assert b'Page not found' in response.data
    assert "404" in response.status


@pytest.mark.xfail(strict=True)
def test_500(client):
    """Check the error handler for 500 errors."""
    # Find a way to force or mock a server error.
    response = client.get('/foo')
    assert b'Internal Server Error' in response.data
    assert "500" in response.status


def test_dropped_db(client):
    """Check behavior when the db has no tables."""
    db.drop_all()
    assert b'Sorry' in client.get('/').data
    assert "404" in client.get('/poem/Flea').status


def test_reset_route(client_empty_db):
    """Check the /reset route."""
    # The database has tables in it
    assert "poems" in db.engine.table_names()
    # The database has no poems in it
    assert b'Sorry' in client_empty_db.get('/').data
    assert "404" in client_empty_db.get('/poem/Flea').status

    # /reset route injects sample poems into database
    client_empty_db.get('/reset')
    assert b'Flea' in client_empty_db.get('/').data
    response = client_empty_db.get('/poem/Flea')
    assert b'Flea' in response.data
    assert "200" in response.status
    assert "404" in client_empty_db.get('/poem/foo').status

    # Makes sure doing it twice doesn't break anything.
    client_empty_db.get('/reset')
    assert b'Flea' in client_empty_db.get('/').data
    response = client_empty_db.get('/poem/Flea')
    assert b'Flea' in response.data
    assert "200" in response.status
    assert "404" in client_empty_db.get('/poem/foo').status


def test_about_default(client, monkeypatch):
    """Check that the about page is loading the default content."""
    monkeypatch.delenv("ABOUT_FILE", raising=False)
    assert b'What is Metroscope about?' in client.get('/about').data


def test_about_missing_file(client, monkeypatch):
    """Check that the about page fails to load content gracefully."""
    monkeypatch.setenv("ABOUT_FILE", 'NONEXISTENT.file')
    assert b'Failed to load' in client.get('/about').data
