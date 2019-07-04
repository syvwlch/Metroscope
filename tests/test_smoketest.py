"""Test the major pages using flask's test_client()."""
import pytest
from run import create_app, db


@pytest.fixture
def client():
    """Set up and tear down the test app and client."""
    app = create_app('testing')
    app.config['TESTING'] = True

    app_context = app.app_context()
    app_context.push()

    yield app.test_client()

    db.session.remove()
    db.drop_all()
    app_context.pop()


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
    """Check behavior when the db is empty."""
    db.drop_all()

    assert b'Sorry' in client.get('/').data

    assert "404" in client.get('/poem/Flea').status


def test_reset(client):
    """Check the /reset route adds sample poems."""
    db.drop_all()
    client.get('/reset')

    assert b'Flea' in client.get('/').data

    response = client.get('/poem/Flea')
    assert b'Flea' in response.data
    assert "200" in response.status

    assert "404" in client.get('/poem/foo').status


def test_double_reset(client):
    """Check that the /reset route is idempotent."""
    db.drop_all()
    client.get('/reset')
    client.get('/reset')

    assert b'Flea' in client.get('/').data

    response = client.get('/poem/Flea')
    assert b'Flea' in response.data
    assert "200" in response.status

    assert "404" in client.get('/poem/foo').status
