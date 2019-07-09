"""Test the User model."""

import pytest
from run.models import User, Role


def test_User_repr():
    """Test the __repr__ method."""
    assert repr(
        User(display_name='display_name')) == "<User 'display_name'>"


def test_User_ValueError(app):
    """Check that insert_samples() raises ValueError if role absent."""
    with pytest.raises(ValueError) as excinfo:
        User.insert_samples()
    assert "This role does not exist." in str(excinfo.value)
    Role.insert_samples()
