"""Test the 404 error handler using flask's test_client()."""
import pytest


@pytest.mark.parametrize("route", [
    '/foo',
    '/poem/bar',
    ])
def test_404(client, route):
    """Check routes that should always 404."""
    response = client.get(route)
    assert b'Page not found' in response.data
    assert "404" in response.status
