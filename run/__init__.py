"""Run script for the website."""

import os
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from metroscope import scanned_poem
import markdown


app = Flask(__name__)

basedir = app.instance_path
try:
    os.makedirs(basedir)
except OSError:
    pass

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

bootstrap = Bootstrap(app)


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
    db.drop_all()
    db.create_all()

    METERS = [
        {'name': 'Iambic Pentameter', 'pattern': '0101010101'},
        {'name': 'Cataleptic Anapestic Trimeter', 'pattern': '01001001'}
    ]
    for meter in METERS:
        db.session.add(
            Meter(name=meter['name'], pattern=meter['pattern'])
        )

    POETS = [
        'John Keats',
        'Edward Lear',
        'John Donne',
        'Wilfred Owen'
    ]
    for poet in POETS:
        db.session.add(Poet(name=poet))

    # commit so loading poets can use poets and meters tables
    db.session.commit()

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
    for sample in POEMS:
        path = 'samples/free/' + sample['keyword'] + '.txt'
        with open(path, "r") as poem:
            title = sample['title']
            keyword = sample['keyword']
            poet_id = Poet.query.filter_by(name=sample['poet']).first().id
            meter_id = Meter.query.filter_by(
                pattern=sample['pattern']).first().id
            db.session.add(
                Poem(
                    title=title,
                    keyword=keyword,
                    raw_text=str(poem.read()),
                    poet_id=poet_id,
                    meter_id=meter_id,
                )
            )

    db.session.commit()


@app.shell_context_processor
def make_shell_context():
    """Add a shell context processor."""
    return dict(db=db,
                Meter=Meter,
                Poet=Poet,
                Poem=Poem,
                reset_db=reset_db,
                )


@app.route("/")
def home():
    """Define the home route."""
    if "poems" not in db.engine.table_names():
        poems = []
    else:
        poems = Poem.query.all()
    return render_template("home.html", poems=poems)


@app.route("/about")
def about():
    """Define the about route."""
    try:
        with open("README.md", "r") as readme:
            ABOUT_CONTENTS = markdown.markdown(readme.read())
    except IOError:
        ABOUT_CONTENTS = "Failed to load the contents of the about page."
    return render_template("about.html",
                           contents=ABOUT_CONTENTS,
                           )


@app.route("/poem/<keyword>")
def poem(keyword):
    """Define the poem route."""
    # if the poems table does not exist, 404 the route
    if "poems" not in db.engine.table_names():
        return render_template('404.html'), 404

    # retrieve the requested poem if it exists
    poem = Poem.query.filter_by(keyword=keyword).first_or_404()

    return render_template("poem.html",
                           title=poem.title,
                           poet=poem.author.name,
                           meter=poem.meter.name,
                           poem=scanned_poem(poem.raw_text,
                                             poem.meter.pattern))


@app.errorhandler(404)
def page_not_found(e):
    """Define the route for the 404 error page."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Define the route for the 500 error page."""
    return render_template('500.html'), 500


@app.route("/reset")
def reset():
    """
    Define the reset route.

    For safety, only works if the poems table does not already exist.
    """
    if "poems" not in db.engine.table_names():
        reset_db()
    return redirect(url_for('home'))
