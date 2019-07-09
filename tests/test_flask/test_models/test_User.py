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
    assert "This role does not exist." in str(excinfo.value)


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
