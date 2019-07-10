"""Database models for the users of the site."""

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from run import db, login_manager


class Role(db.Model):
    """Define the roles table."""

    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        """Represent the class."""
        return f"<Role '{self.name}'>"

    @staticmethod
    def insert_roles():
        """
        Insert roles into the database.

        Idempotent.
        """
        ROLES = [
            {'name': 'Contributor'},
            {'name': 'Editor'},
            {'name': 'Admin'},
        ]
        needs_commit = False
        for role in ROLES:
            if Role.query.filter_by(name=role['name']).first() is None:
                db.session.add(
                    Role(name=role['name'])
                )
                print(f"Adding role '{role['name']}' to database.")
                needs_commit = True
        if needs_commit:
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

    def __repr__(self):
        """Represent the class."""
        return f"<User '{self.display_name}'>"

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

    @staticmethod
    def insert_admin():
        """
        Insert the admin user into the database.

        Idempotent.
        """
        from flask import current_app

        needs_commit = False
        email = current_app.config['ADMIN_EMAIL']
        display_name = 'Admin'
        role_name = 'Admin'
        password = current_app.config['ADMIN_PASSWORD']

        role = Role.query.filter_by(name=role_name).first()
        if role is None:
            raise ValueError(f'The {role_name} role does not exist.')
        if User.query.filter_by(role_id=role.id).first() is None:
            admin = User(
                    email=email,
                    display_name=display_name,
                    role_id=role.id,
                )
            admin.password = password
            db.session.add(admin)
            print(f"Adding user {email} with the {role} role.")
            needs_commit = True
        else:
            print(f'A user with the {role} role already exists.')
        if needs_commit:
            db.session.commit()
            print("Changes committed.")
        # else:
        #     print('No changes committed.')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
