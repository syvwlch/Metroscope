"""Test the major views using flask's test_client()."""
import pytest


@pytest.mark.xfail(strict=True)
def test_500(client):
    """Check the error handler for 500 errors."""
    # Find a way to force or mock a server error.
    response = client.get('/foo')
    assert b'Internal Server Error' in response.data
    assert "500" in response.status
