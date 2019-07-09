"""Database models for the users of the site."""

from run import db


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
    def insert_samples():
        """
        Insert some sample roles into the database.

        Idempotent.
        """
        ROLES = [
            {'name': 'Contributor'},
            {'name': 'Editor'}
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


class User(db.Model):
    """Define the users table."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    display_name = db.Column(db.String(64), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        """Represent the class."""
        return f"<User '{self.display_name}'>"

    @staticmethod
    def insert_samples():
        """
        Insert some sample users into the database.

        Idempotent.
        """
        USERS = [
            {
                'email': 'john.doe@test.org',
                'display_name': 'John Doe',
                'role': 'Contributor',
            },
            {
                'email': 'admin@metro.scope',
                'display_name': 'Ye Olde Admin',
                'role': 'Editor',
            },
        ]
        needs_commit = False
        for user in USERS:
            if Role.query.filter_by(name=user['role']).first() is None:
                raise ValueError('This role does not exist.')
            email = user['email']
            display_name = user['display_name']
            if User.query.filter_by(email=email).first() is None:
                role = Role.query.filter_by(name=user['role']).first()
                db.session.add(
                    User(
                        email=email,
                        display_name=display_name,
                        role_id=role.id,
                    )
                )
                print(f"Adding user '{display_name}' to database.")
                needs_commit = True
        if needs_commit:
            db.session.commit()
            print("Changes committed.")
