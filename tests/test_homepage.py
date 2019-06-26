"""Test the homepage using flask's test_client()."""
import pytest
from run import application


@pytest.fixture
def client():
    """Fixture to create the test client."""
    application.config['TESTING'] = True
    yield application.test_client()


def test_not_404(client):
    """Make sure the homepage doesn't 404."""
    assert "404" not in client.get('/').status


def test_not_500(client):
    """Make sure the homepage doesn't 500."""
    assert "500" not in client.get('/').status
