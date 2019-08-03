"""Test the login view using flask's test_client()."""

from flask import url_for, get_flashed_messages
from flask_login import current_user


def test_200(client):
    """Check the login view should always return a 200."""
    assert "200" in client.get("/auth/login").status


def test_login_user(client, auth):
    """Check the login user route authenticates the user."""
    with client:
        auth.register(follow_redirects=True)
        assert not current_user.is_authenticated

        response = auth.login()
        assert current_user.is_authenticated
        assert "302" in response.status
        assert url_for('main.home', _external=True) == response.location
        assert get_flashed_messages() == []


def test_login_authenticated_user(client, auth):
    """Check that login redirects when the user is already authenticated."""
    with client:
        auth.register()
        auth.login(follow_redirects=True)
        response = client.get('/auth/login')
        assert current_user.is_authenticated
        assert "302" in response.status
        assert url_for('main.home', _external=True) == response.location
        assert get_flashed_messages() == []


def test_login_bad_credentials(client, auth):
    """Check the login user route errors with bad credentials."""
    with client:
        response = auth.login()
        assert not current_user.is_authenticated
        assert "200" in response.status
        assert "Invalid username or password." in get_flashed_messages()[0]


def test_login_with_next(client, auth):
    """Check that login obeys the next parameter."""
    with client:
        auth.register(follow_redirects=True)
        response = auth.login(next="%2Fpoetry%2Fpoem")
        assert current_user.is_authenticated
        assert "302" in response.status
        assert url_for('poetry.poem_list', _external=True) == response.location
        assert get_flashed_messages() == []
