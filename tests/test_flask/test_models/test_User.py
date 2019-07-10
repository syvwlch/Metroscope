"""Test the User model."""

import pytest
from run.models import User


def test_User_repr():
    """Test the __repr__ method."""
    assert repr(
        User(display_name='display_name')) == "<User 'display_name'>"


def test_User_ValueError(app):
    """Check that insert_admin() raises ValueError if role absent."""
    with pytest.raises(ValueError) as excinfo:
        User.insert_admin()
    assert "The Admin role does not exist." in str(excinfo.value)


def test_insert_admin_safe(app):
    """Check insert_admin does nothing if an admin user already exists."""
    from run import db
    from run.models import Role
    Role.insert_roles()
    admin_role = Role.query.filter_by(name="Admin").first()
    db.session.add(User(
        email="a@b.c",
        display_name="first_admin",
        role_id=admin_role.id,
        )
    )
    db.session.commit()
    # check the baseline before running insert_admin
    admins = User.query.filter_by(role_id=admin_role.id)
    assert admins.count() == 1
    assert admins.first().email == "a@b.c"
    # insert_admin will now attempt to insert the admin user from env vars
    # which has a different email address
    User.insert_admin()
    admins = User.query.filter_by(role_id=admin_role.id)
    assert admins.count() == 1
    assert admins.first().email == "a@b.c"


def test_password_setter():
    """Check setting the password stores a hash."""
    u = User(password='cat')
    assert u.password_hash is not None


def test_no_password_getter():
    """Check password can't be read."""
    u = User(password='cat')
    with pytest.raises(AttributeError) as excinfo:
        u.password
    assert "Password is not a readable attribute." in str(excinfo.value)


def test_password_verification():
    """Check password verification works."""
    u = User(password='cat')
    assert u.verify_password('cat')
    assert not u.verify_password('dog')


def test_password_salts_are_random():
    """Check different users with same password have different hashes."""
    u = User(password='cat')
    u2 = User(password='cat')
    assert u.password_hash != u2.password_hash
