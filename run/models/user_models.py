"""Database models for the users of the site."""

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from run import db, login_manager


class Permission:
    ADMIN = 1
    ADD_POEM = 2
    ADD_METER = 4
    CHANGE_METER = 8


class Role(db.Model):
    """Define the roles table."""

    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    default = db.Column(db.Boolean, default='False', index=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    permissions = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        """Represent the class."""
        return f"<Role '{self.name}'>"

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        """
        Insert roles into the database.

        Idempotent.
        """
        ROLES = {
            'Contributor': [
                Permission.CHANGE_METER
            ],
            'Editor': [
                Permission.CHANGE_METER,
                Permission.ADD_METER,
                Permission.ADD_POEM,
            ],
            'Admin': [
                Permission.CHANGE_METER,
                Permission.ADD_METER,
                Permission.ADD_POEM,
                Permission.ADMIN,
            ],
        }
        default_role = 'Contributor'
        for r in ROLES:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
                print(f"Creating role '{r}'.")
            role.reset_permissions()
            for perm in ROLES[r]:
                role.add_permission(perm)
            print(f"Resetting permissions for role '{r}'.")
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()
        print("Changes committed.")


class User(UserMixin, db.Model):
    """Define the users table."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    display_name = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(name='Admin').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        """Represent the class."""
        return f"<User '{self.display_name}'>"

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_admin(self):
        return self.can(Permission.ADMIN)

    @property
    def password(self):
        """Block attempts to read password."""
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """Generate the hash of the password."""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Compare the password against the stored hash."""
        return check_password_hash(self.password_hash, password)


class AnonymousUser(AnonymousUserMixin):
    def can(self, perm):
        return False

    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
