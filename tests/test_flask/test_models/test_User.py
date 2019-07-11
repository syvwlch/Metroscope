"""Test the User model."""

import pytest
from run.models import User


def test_User_repr(app):
    """Test the __repr__ method."""
    assert repr(
        User(display_name='display_name')) == "<User 'display_name'>"


def test_password_setter(app):
    """Check setting the password stores a hash."""
    u = User(password='cat')
    assert u.password_hash is not None


def test_no_password_getter(app):
    """Check password can't be read."""
    u = User(password='cat')
    with pytest.raises(AttributeError) as excinfo:
        u.password
    assert "Password is not a readable attribute." in str(excinfo.value)


def test_password_verification(app):
    """Check password verification works."""
    u = User(password='cat')
    assert u.verify_password('cat')
    assert not u.verify_password('dog')


def test_password_salts_are_random(app):
    """Check different users with same password have different hashes."""
    u = User(password='cat')
    u2 = User(password='cat')
    assert u.password_hash != u2.password_hash
