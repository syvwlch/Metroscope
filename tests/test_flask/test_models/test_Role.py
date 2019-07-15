"""Test the Role model."""

from run.models import Role


def test_Role_repr():
    """Test the __repr__ method."""
    assert repr(
        Role(name='name')) == "<Role 'name'>"


def test_insert_roles_idempotent(app):
    """Check insert_roles is idempotent."""
    Role.insert_roles()
    roles = Role.query.all()
    Role.insert_roles()
    assert roles == Role.query.all()
