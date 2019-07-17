"""Test the login view using flask's test_client()."""


def test_200(client):
    """Check the register view should always return a 200."""
    assert "200" in client.get("/auth/register").status


def test_register_user(client, auth):
    """Check the register user route adds a user to the db."""

    response = auth.register(follow_redirects=True)
    assert "200" in response.status
    assert b"You can now login." in response.data
