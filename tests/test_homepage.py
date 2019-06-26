"""Test the homepage using flask's test_client()."""
from run import application


def test_not_404():
    """Make sure the homepage doesn't 404."""
    client = application.test_client()
    response = client.get('/')
    assert "404" not in response.status


def test_not_500():
    """Make sure the homepage doesn't 500."""
    client = application.test_client()
    response = client.get('/')
    assert "500" not in response.status
