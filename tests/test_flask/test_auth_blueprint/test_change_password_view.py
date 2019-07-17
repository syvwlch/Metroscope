"""Test the change password view using flask's test_client()."""


from flask import url_for, get_flashed_messages
from flask_login import current_user


def test_requires_login(client, auth):
    """Check the change password view requires login."""
    with client:
        response = client.get("/auth/change-password")
        assert not current_user.is_authenticated
        assert "302" in response.status
        redirect = url_for('auth.login', _external=True)
        redirect += "?next=%2Fauth%2Fchange-password"
        assert redirect == response.location


def test_change_password(client, auth):
    """Check the change password route works."""
    with client:
        auth.register()
        auth.login(follow_redirects=True)

        response = client.post(
            '/auth/change-password',
            data={
                'old_password': 'cat',
                'email': 'john@metro.scope',
                'password': 'dog',
                'password2': 'dog',
            },
        )
        assert current_user.is_authenticated
        assert "302" in response.status
        assert url_for('main.home', _external=True) == response.location
        assert get_flashed_messages() == ['Your password has been updated.']
