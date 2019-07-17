"""Test the login view using flask's test_client()."""


def test_200(client):
    """Check the login view should always return a 200."""
    assert "200" in client.get("/auth/login").status


def test_login_user(client, auth):
    """Check the login user route authenticates the user."""
    from flask_login import current_user

    with client:
        auth.register()
        assert not current_user.is_authenticated

        response = auth.login()
        assert current_user.is_authenticated
        assert "302" in response.status
        assert b"Invalid username or password." not in response.data


def test_login_authenticated_user(client, auth):
    """Check that login redirects when the user is already authenticated."""
    from flask import url_for
    with client:
        auth.register()
        auth.login()
        response = auth.login()
        assert "302" in response.status
        assert url_for('main.home', _external=True) == response.location
