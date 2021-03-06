"""Test the logout view using flask's test_client()."""


from flask import url_for, get_flashed_messages


def test_302(client):
    """Check the logout view should always return a 302."""
    assert "302" in client.get("/auth/logout").status


def test_logout_user(client, auth):
    """Check the logout user route de-authenticates the user."""
    from flask_login import current_user

    with client:
        auth.register()
        assert not current_user.is_authenticated

        auth.login(follow_redirects=True)
        assert current_user.is_authenticated

        response = auth.logout()
        assert not current_user.is_authenticated
        assert "302" in response.status
        assert url_for('main.home', _external=True) == response.location
        assert get_flashed_messages() == ['You have been logged out.']


def test_logout_unauthenticated_user(client, auth):
    """Check the logout user route is safe for unauthenticated user."""
    from flask_login import current_user

    with client:
        auth.register(follow_redirects=True)
        assert not current_user.is_authenticated

        response = auth.logout()
        assert not current_user.is_authenticated
        assert "302" in response.status
        redirect = url_for('auth.login', _external=True)
        redirect += '?next=%2Fauth%2Flogout'
        assert redirect == response.location
        assert get_flashed_messages() == ['Please log in to access this page.']
