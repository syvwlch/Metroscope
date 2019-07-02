"""Test the major pages using flask's test_client()."""
import pytest
from run import app


@pytest.fixture
def client():
    """Fixture to create the test client."""
    app.config['TESTING'] = True
    # Need to hit the /reset route to load sample poems into db
    app.test_client().get('/reset')
    yield app.test_client()


@pytest.mark.parametrize("route", ['/', '/about', '/poem/Flea'])
def test_200(client, route):
    """Make sure the page returns a 200."""
    assert "200" in client.get(route).status


@pytest.mark.parametrize("route", ['/foo', '/poem/bar'])
def test_unknown_pages(client, route):
    """Make sure that pages that don't exist do 404."""
    assert "404" in client.get(route).status
