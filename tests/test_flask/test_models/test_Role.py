"""Test the Role model."""

from run.models import Role


def test_Role_repr():
    """Test the __repr__ method."""
    assert repr(
        Role(name='name')) == "<Role 'name'>"
