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


class Poet(db.Model):
    """Define the Poets table."""

    __tablename__ = 'poets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    poems = db.relationship('Poem', backref='author', lazy='dynamic')

    def __repr__(self):
        """Represent the class."""
        return f"<Poet '{self.name}'>"


class Poem(db.Model):
    """Define the Poems table."""

    __tablename__ = 'poems'
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(64), unique=True, nullable=False)
    title = db.Column(db.String(64), nullable=False)
    raw_text = db.Column(db.Text, nullable=False)
    poet_id = db.Column(db.Integer, db.ForeignKey('poets.id'))
    meter_id = db.Column(db.Integer, db.ForeignKey('meters.id'))

    def __repr__(self):
        """Represent the class."""
        return f"<Poem '{self.title}'>"


def reset_db():
    """Reset the database with the sample poems."""
    METERS = [
        {'name': 'Iambic Pentameter', 'pattern': '0101010101'},
        {'name': 'Cataleptic Anapestic Trimeter', 'pattern': '01001001'}
    ]
    POETS = [
        'John Keats',
        'Edward Lear',
        'John Donne',
        'Wilfred Owen'
    ]
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

    db.drop_all()
    db.create_all()

    for meter in METERS:
        if Meter.query.filter_by(pattern=meter['pattern']).first() is None:
            db.session.add(
                Meter(name=meter['name'], pattern=meter['pattern'])
            )

    for poet in POETS:
        if Poet.query.filter_by(name=poet).first() is None:
            db.session.add(Poet(name=poet))

    # commit so loading poets can use poets and meters tables
    db.session.commit()

    for poem in POEMS:
        if Poem.query.filter_by(keyword=poem['keyword']).first() is None:
            path = 'samples/free/' + poem['keyword'] + '.txt'
            with open(path, "r") as text_file:
                title = poem['title']
                keyword = poem['keyword']
                poet_id = Poet.query.filter_by(name=poem['poet']).first().id
                meter_id = Meter.query.filter_by(
                    pattern=poem['pattern']).first().id
                db.session.add(
                    Poem(
                        title=title,
                        keyword=keyword,
                        raw_text=str(text_file.read()),
                        poet_id=poet_id,
                        meter_id=meter_id,
                    )
                )

    db.session.commit()
