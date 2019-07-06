"""Test the major pages using flask's test_client()."""
import os
import pytest
from run import create_app, db
from flask_migrate import Migrate


@pytest.fixture
def app():
    """Set up and tear down the test app."""
    app = create_app('testing')
    Migrate(app, db)

    app.config['TESTING'] = True

    app_context = app.app_context()
    app_context.push()

    yield app

    app_context.pop()


@pytest.fixture
def client(app):
    """Set up and tear down the test client."""
    yield app.test_client()


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


@pytest.mark.xfail
def test_500(client):
    """Check the error handler for 500 errors."""
    response = client.put('/foo')
    assert b'Page not found' in response.data
    assert "500" in response.status


def test_no_db(client):
    """Check behavior when there is no db."""
    try:
        os.remove('data-test.sqlite')
    except OSError:
        pass

    # There is no database
    assert b'Sorry' in client.get('/').data
    assert "404" in client.get('/poem/Flea').status


def test_reset_route(client):
    """Check the /reset route."""
    # The database has no poems in it when first initialized
    assert b'Sorry' in client.get('/').data
    assert "404" in client.get('/poem/Flea').status

    # Inject sample poems into existing database
    client.get('/reset')
    assert b'Flea' in client.get('/').data

    # Makes sure doing it twice doesn't break anything.
    client.get('/reset')
    assert b'Flea' in client.get('/').data
    response = client.get('/poem/Flea')
    assert b'Flea' in response.data
    assert "200" in response.status
    assert "404" in client.get('/poem/foo').status
