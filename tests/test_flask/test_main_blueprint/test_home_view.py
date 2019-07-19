"""Test the home view using flask's test_client()."""

from flask import url_for


def test_200(client):
    """Check the home should always return a 200."""
    with client:
        response = client.get("/")
        assert "200" in response.status
        assert url_for('poetry.poem_list') in str(response.data)
