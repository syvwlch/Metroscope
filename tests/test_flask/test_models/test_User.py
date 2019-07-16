"""Test the User model."""

import pytest
from run.models import User, AnonymousUser, Permission


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


def test_password_reset_token(app):
    """Check that password reset tokens can be verified."""
    from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
    u = User(password='cat')
    token = u.generate_reset_token()
    s = Serializer(app.config['SECRET_KEY'])
    assert s.loads(token.encode('utf-8')).get('reset') == u.id


def test_password_reset(app):
    """Check that the password_reset static method works."""
    from run import db
    u = User(
        email='john@example.com',
        display_name='John',
        password='cat',
    )
    db.session.add(u)
    db.session.commit()
    token = 'fake_token'
    assert not User.reset_password(token, 'dog')
    assert u.verify_password('cat')
    token = u.generate_reset_token()
    assert User.reset_password(token, 'dog')
    assert u.verify_password('dog')


def test_default_user_permissions(app):
    from run.models import Role
    Role.insert_roles()
    u = User(
        email='john@example.com',
        display_name='John',
        password='cat',
    )
    assert u.role.default
    assert not u.can(Permission.ADMIN)
    assert not u.can(Permission.ADD_POEM)
    assert not u.can(Permission.ADD_METER)
    assert u.can(Permission.CHANGE_METER)


def test_anonymous_user_permissions(app):
    u = AnonymousUser()
    assert not u.can(Permission.ADMIN)
    assert not u.can(Permission.ADD_POEM)
    assert not u.can(Permission.ADD_METER)
    assert not u.can(Permission.CHANGE_METER)


def test_admin_user_permissions(app):
    from run.models import Role
    Role.insert_roles()
    ADMIN_EMAIL = app.config['ADMIN_EMAIL']
    u = User(
        email=ADMIN_EMAIL,
        display_name='John',
        password='cat',
    )

    assert u.role.name == 'Admin'

    assert u.can(Permission.ADMIN)
    assert u.can(Permission.ADD_POEM)
    assert u.can(Permission.ADD_METER)
    assert u.can(Permission.CHANGE_METER)

    assert u.is_admin()
