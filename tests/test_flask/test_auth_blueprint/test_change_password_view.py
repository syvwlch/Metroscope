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
        assert current_user.is_authenticated
        assert current_user.verify_password('cat')

        response = client.post(
            '/auth/change-password',
            data={
                'old_password': 'cat',
                'password': 'dog',
                'password2': 'dog',
            },
        )
        assert current_user.is_authenticated
        assert "302" in response.status
        assert url_for('main.home', _external=True) == response.location
        assert get_flashed_messages() == ['Your password has been updated.']
        assert current_user.verify_password('dog')


def test_change_password_no_old_password(client, auth):
    """Check the change password route fails without old password."""
    with client:
        auth.register()
        auth.login(follow_redirects=True)

        response = client.post(
            '/auth/change-password',
            data={
                'password': 'dog',
                'password2': 'dog',
            },
        )
        assert current_user.is_authenticated
        assert "200" in response.status
        assert get_flashed_messages() == []
        assert b"This field is required." in response.data
        assert current_user.verify_password('cat')


def test_change_password_wrong_old_password(client, auth):
    """Check the change password route fails with wrong old password."""
    with client:
        auth.register()
        auth.login(follow_redirects=True)

        response = client.post(
            '/auth/change-password',
            data={
                'old_password': 'rabbit',
                'password': 'dog',
                'password2': 'dog',
            },
        )
        assert current_user.is_authenticated
        assert "200" in response.status
        assert get_flashed_messages() == ['Invalid password.']
        assert current_user.verify_password('cat')
