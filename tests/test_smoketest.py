"""Test the major pages using flask's test_client()."""
import os
import pytest
from run import create_app, db
from run.models import Poem


@pytest.fixture
def client():
    """Set up and tear down the test app and client."""
    app = create_app('testing')
    app.config['TESTING'] = True

    app_context = app.app_context()
    app_context.push()
    db.create_all()

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
    """Check behavior when there is no db."""
    try:
        os.remove('data-test.sqlite')
    except OSError:
        pass

    # There is no database
    assert b'Sorry' in client.get('/').data
    assert "404" in client.get('/poem/Flea').status

    # Create database and inject sample poems
    client.get('/reset')

    assert b'Flea' in client.get('/').data
    response = client.get('/poem/Flea')
    assert b'Flea' in response.data
    assert "200" in response.status
    assert "404" in client.get('/poem/foo').status


def test_empty_db(client):
    """Check behavior when the db is empty."""
    for poem in Poem.query.all():
        db.session.delete(poem.id)
    db.session.commit()

    # The database has no poems in it
    assert b'Sorry' in client.get('/').data
    assert "404" in client.get('/poem/Flea').status

    # Inject sample poems into existing database
    client.get('/reset')

    assert b'Flea' in client.get('/').data
    response = client.get('/poem/Flea')
    assert b'Flea' in response.data
    assert "200" in response.status
    assert "404" in client.get('/poem/foo').status


def test_double_reset(client):
    """Check that the /reset route is idempotent."""
    # Hitting the /reset route more than once should not break the db
    client.get('/reset')
    client.get('/reset')

    assert b'Flea' in client.get('/').data

    response = client.get('/poem/Flea')
    assert b'Flea' in response.data
    assert "200" in response.status

    assert "404" in client.get('/poem/foo').status
