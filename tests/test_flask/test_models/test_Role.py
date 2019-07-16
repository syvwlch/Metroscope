"""Test the Role model."""

from run.models import Role, Permission


def test_Role_repr():
    """Test the __repr__ method."""
    assert repr(
        Role(name='name')) == "<Role 'name'>"


def test_Role_insert_roles(app):
    """Test the insert_samples static method of Role."""
    assert Role.query.first() is None

    Role.insert_roles()
    assert Role.query.first() is not None

    roles = Role.query.all()
    for role in roles:
        assert isinstance(role.name, str)
        assert isinstance(role.default, bool)
        assert isinstance(role.permissions, int)

    Role.insert_roles()
    # Check the operation is idempotent
    assert roles == Role.query.all()


def test_Role_Contributor_is_default(app):
    """Test that Contributor is the only default role."""
    Role.insert_roles()
    contributor_role = Role.query.filter_by(name='Contributor').first()
    assert contributor_role.default
    roles = Role.query.all()
    number_of_default_roles = 0
    for role in roles:
        if role.default:
            number_of_default_roles += 1
    assert number_of_default_roles == 1


def test_Role_relationship_User(app):
    """Test the relationship between Role and User."""
    from run import db
    from run.models import User

    Role.insert_roles()
    roles = Role.query.all()

    for role in roles:
        u = User(
            display_name=f'{role.name} user',
            email=f'{role.name}@test.com',
            role=role,
        )
        db.session.add(u)
    db.session.commit()

    for role in roles:
        for user in role.users:
            assert isinstance(user, User)
            assert role == user.role


def test_role_permissions():
    """Check permissions methods."""
    role = Role(name='new role')
    assert not role.has_permission(Permission.ADMIN)
    assert not role.has_permission(Permission.ADD_POEM)
    role.add_permission(Permission.ADMIN)
    assert role.has_permission(Permission.ADMIN)
    assert not role.has_permission(Permission.ADD_POEM)
    role.add_permission(Permission.ADD_POEM)
    assert role.has_permission(Permission.ADMIN)
    assert role.has_permission(Permission.ADD_POEM)
    role.remove_permission(Permission.ADMIN)
    assert not role.has_permission(Permission.ADMIN)
    assert role.has_permission(Permission.ADD_POEM)
    role.reset_permissions()
    assert not role.has_permission(Permission.ADMIN)
    assert not role.has_permission(Permission.ADD_POEM)
