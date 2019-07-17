"""Test the logout view using flask's test_client()."""


def test_302(client):
    """Check the logout view should always return a 302."""
    assert "302" in client.get("/auth/logout").status


def test_logout_user(client, auth):
    """Check the logout user route de-authenticates the user."""
    from flask_login import current_user

    with client:
        auth.register()
        assert not current_user.is_authenticated

        auth.login()
        assert current_user.is_authenticated

        response = auth.logout(follow_redirects=True)
        assert not current_user.is_authenticated
        assert "200" in response.status
        assert b"You have been logged out." in response.data
