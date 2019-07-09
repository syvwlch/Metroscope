"""Test the login view using flask's test_client()."""


def test_200(client):
    """Check the login view should always return a 200."""
    assert "200" in client.get("/auth/login").status
