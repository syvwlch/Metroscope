"""Database models for the site."""

from run import db


class Meter(db.Model):
    """Define the meters table."""

    __tablename__ = 'meters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    pattern = db.Column(db.String(64), unique=True, nullable=False)
    poems = db.relationship('Poem', backref='meter', lazy='dynamic')

    def __repr__(self):
        """Represent the class."""
        return f"<Meter '{self.name}'>"

    @staticmethod
    def insert_samples():
        """
        Insert some sample meters into the database.

        Idempotent.
        """
        METERS = [
            {'name': 'Iambic Pentameter', 'pattern': '0101010101'},
            {'name': 'Cataleptic Anapestic Trimeter', 'pattern': '01001001'}
        ]
        needs_commit = False
        for meter in METERS:
            if Meter.query.filter_by(pattern=meter['pattern']).first() is None:
                db.session.add(
                    Meter(name=meter['name'], pattern=meter['pattern'])
                )
                print(f"Adding meter '{meter['name']}' to database.")
                needs_commit = True
        if needs_commit:
            db.session.commit()
            print("Changes committed.")


class Poet(db.Model):
    """Define the poets table."""

    __tablename__ = 'poets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    poems = db.relationship('Poem', backref='author', lazy='dynamic')

    def __repr__(self):
        """Represent the class."""
        return f"<Poet '{self.name}'>"

    @staticmethod
    def insert_samples():
        """
        Insert some sample poets into the database.

        Idempotent.
        """
        POETS = [
            'John Keats',
            'Edward Lear',
            'John Donne',
            'Wilfred Owen'
        ]
        needs_commit = False
        for poet in POETS:
            if Poet.query.filter_by(name=poet).first() is None:
                db.session.add(Poet(name=poet))
                print(f"Adding poet '{poet}' to database.")
                needs_commit = True
        if needs_commit:
            db.session.commit()
            print("Changes committed.")


class Poem(db.Model):
    """Define the poems table."""

    __tablename__ = 'poems'
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(64), unique=True, nullable=False)
    title = db.Column(db.String(64), nullable=False)
    raw_text = db.Column(db.Text, nullable=False)
    HTML = db.Column(db.Text)
    poet_id = db.Column(db.Integer, db.ForeignKey('poets.id'))
    meter_id = db.Column(db.Integer, db.ForeignKey('meters.id'))

    def __repr__(self):
        """Represent the class."""
        return f"<Poem '{self.title}'>"

    @staticmethod
    def insert_samples():
        """
        Insert some sample poems into the database.

        Idempotent.
        """
        from metroscope import scanned_poem
        POEMS = [
            {
                'title': 'Ode on Indolence',
                'keyword': 'OdeOnIndolence',
                'poet': 'John Keats',
                'pattern': '0101010101',
            },
            {
                'title': 'There Was an Old Man with a Beard',
                'keyword': 'OldManWithBeard',
                'poet': 'Edward Lear',
                'pattern': '01001001',
            },
            {
                'title': 'The Flea',
                'keyword': 'Flea',
                'poet': 'John Donne',
                'pattern': '0101010101',
            },
            {
                'title': 'Anthem for Doomed Youth',
                'keyword': 'AnthemForDoomedYouth',
                'poet': 'Wilfred Owen',
                'pattern': '0101010101',
            },
        ]
        needs_commit = False
        for poem in POEMS:
            if Poet.query.filter_by(name=poem['poet']).first() is None:
                raise ValueError('This poet does not exist.')
            if Meter.query.filter_by(pattern=poem['pattern']).first() is None:
                raise ValueError('This meter pattern does not exist.')
            if Poem.query.filter_by(keyword=poem['keyword']).first() is None:
                path = 'samples/free/' + poem['keyword'] + '.txt'
                title = poem['title']
                keyword = poem['keyword']
                poet = Poet.query.filter_by(name=poem['poet']).first()
                meter = Meter.query.filter_by(pattern=poem['pattern']).first()
                with open(path, "r") as text_file:
                    raw_text = str(text_file.read())
                    db.session.add(
                        Poem(
                            title=title,
                            keyword=keyword,
                            raw_text=raw_text,
                            HTML=scanned_poem(raw_text, meter.pattern),
                            poet_id=poet.id,
                            meter_id=meter.id,
                        )
                    )
                    print(f"Adding poem '{poem['title']}' to database.")
                needs_commit = True
        if needs_commit:
            db.session.commit()
            print("Changes committed.")


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


def reset_db():
    """Insert samples into the database."""
    Meter.insert_samples()
    Poet.insert_samples()
    Poem.insert_samples()

    Role.insert_samples()
    User.insert_samples()
