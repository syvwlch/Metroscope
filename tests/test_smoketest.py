"""Test the major pages using flask's test_client()."""
import pytest
from run import application


@pytest.fixture
def client():
    """Fixture to create the test client."""
    application.config['TESTING'] = True
    yield application.test_client()


@pytest.mark.parametrize("route", ['/', '/about'])
def test_200(client, route):
    """Make sure the page returns a 200."""
    # currently does not test the poem/foo route when poem foo exists
    # need to put that back in once there's a test database
    assert "200" in client.get(route).status


@pytest.mark.parametrize("route", ['/foo', '/poem/bar'])
def test_unknown_pages(client, route):
    """Make sure that pages that don't exist do 404."""
    assert "404" in client.get(route).status
