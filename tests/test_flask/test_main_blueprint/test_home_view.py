"""Test the home view using flask's test_client()."""


def test_200(client):
    """Check the home should always return a 200."""
    assert "200" in client.get("/").status
