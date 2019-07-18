"""Test the admin view using flask's test_client()."""

from flask import url_for
from flask_login import current_user


def test_requires_login(client, auth):
    """Check the admin view requires login."""
    with client:
        response = client.get("/auth/admin")
        assert not current_user.is_authenticated
        assert "302" in response.status
        redirect = url_for('auth.login', _external=True)
        redirect += "?next=%2Fauth%2Fadmin"
        assert redirect == response.location


def test_requires_admin_permission(client, auth):
    """Check the admin view requires admin permission."""
    with client:
        auth.register()
        auth.login(follow_redirects=True)
        response = client.get("/auth/admin")
        assert current_user.is_authenticated
        assert "403" in response.status
        assert b"Access Forbidden" in response.data


def test_admin(client, auth):
    """Check the admin view shows the user and role."""
    from flask import current_app
    from run.models import Role
    with client:
        Role.insert_roles()
        auth.register(email=current_app.config['ADMIN_EMAIL'])
        auth.login(email=current_app.config['ADMIN_EMAIL'])
        assert current_user.is_authenticated
        assert current_user.is_admin()
        response = client.get("/auth/admin")
        assert "200" in response.status
        assert b"Registered Users" in response.data
        assert b"John" in response.data
        assert b"Roles" in response.data
        assert b"Admin" in response.data
