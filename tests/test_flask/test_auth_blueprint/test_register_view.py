"""Test the register view using flask's test_client()."""

from flask import url_for, get_flashed_messages
from flask_login import current_user


def test_200(client):
    """Check the register view should always return a 200."""
    assert "200" in client.get("/auth/register").status


def test_register_user(client, auth):
    """Check the register user route adds a user to the db."""
    from run.models import User
    assert User.query.first() is None
    with client:
        response = auth.register()
        assert "302" in response.status
        assert url_for('auth.login', _external=True) == response.location
        assert "You can now login." in get_flashed_messages()[0]
    assert User.query.first() is not None


def test_register_authenticated_user(client, auth):
    """Check that register redirects when the user is already authenticated."""
    with client:
        auth.register()
        auth.login(follow_redirects=True)
        response = client.get('/auth/register')
        assert current_user.is_authenticated
        assert "302" in response.status
        assert url_for('main.home', _external=True) == response.location
        assert get_flashed_messages() == []


def test_register_display_name_already_exists(client, auth):
    """Check that register errors when display name already in use."""
    with client:
        auth.register(follow_redirects=True)
        response = auth.register(email='john2@metro.scope')
        assert "200" in response.status
        assert b'Display name already in use.' in response.data
        assert get_flashed_messages() == []


def test_register_email_already_exists(client, auth):
    """Check that register errors when email already in use."""
    with client:
        auth.register(follow_redirects=True)
        response = auth.register(display_name='john2')
        assert "200" in response.status
        assert b'Email already registered.' in response.data
        assert get_flashed_messages() == []
