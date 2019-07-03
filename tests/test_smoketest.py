"""Test the major pages using flask's test_client()."""
import pytest
from flask import current_app
from run import create_app, db


@pytest.fixture
def test_app():
    """Set up and tear down the test database."""
    app = create_app('testing')
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    yield app
    db.session.remove()
    db.drop_all()
    app_context.pop()


@pytest.fixture
def client(test_app):
    """Fixture to create the test client."""
    current_app.config['TESTING'] = True
    # Need to hit the /reset route to load sample poems into db
    current_app.test_client().get('/reset')
    yield current_app.test_client()


@pytest.mark.parametrize("route", [
    '/',
    '/about',
    # '/poem/Flea',
    ])
def test_200(client, route):
    """Make sure the page returns a 200."""
    assert "200" in client.get(route).status


@pytest.mark.parametrize("route", [
    '/foo',
    '/poem/bar',
    ])
def test_unknown_pages(client, route):
    """Make sure that pages that don't exist do 404."""
    assert "404" in client.get(route).status
