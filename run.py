"""Run script for the website."""

import os
from flask import Flask, render_template
import click
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from metroscope import scanned_poem
import markdown


basedir = os.path.abspath(os.path.dirname(__file__))

application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

bootstrap = Bootstrap(application)


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


@application.shell_context_processor
def make_shell_context():
    """Add a shell context processor."""
    return dict(db=db,
                Meter=Meter,
                Poet=Poet,
                Poem=Poem,
                reset_db=reset_db,
                )


@application.route("/")
def home():
    """Define the home route."""
    return render_template("home.html")


@application.route("/about")
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


@application.route("/poem/<keyword>")
def poem(keyword):
    """Define the poem route."""
    if "poems" not in db.engine.table_names():
        return render_template('404.html'), 404

    poem = Poem.query.filter_by(keyword=keyword).first_or_404()
    METER_PATTERN = []
    for beat in poem.meter.pattern:
        METER_PATTERN.append(beat == '1')

    return render_template("poem.html",
                           title=poem.title,
                           poet=poem.author.name,
                           meter=poem.meter.name,
                           poem=scanned_poem(poem.raw_text, METER_PATTERN),
                           )


@application.errorhandler(404)
def page_not_found(e):
    """Define the route for the 404 error page."""
    return render_template('404.html'), 404


@application.errorhandler(500)
def internal_server_error(e):
    """Define the route for the 500 error page."""
    return render_template('500.html'), 500


@application.cli.command('reset_db')
def reset_db():
    """Reset the database with the sample poems."""
    click.echo("Dropping all tables...")
    db.drop_all()
    click.echo("Creating all tables...")
    db.create_all()

    click.echo("Adding meters...")
    db.session.add(Meter(name='Iambic Pentameter',
                         pattern='0101010101'))
    db.session.add(Meter(name='Cataleptic Anapestic Trimeter',
                         pattern='01001001'))

    click.echo("Adding poets...")
    db.session.add(Poet(name='John Keats'))
    db.session.add(Poet(name='Edward Lear'))
    db.session.add(Poet(name='John Donne'))
    db.session.add(Poet(name='Wilfred Owen'))

    click.echo("Commiting to database...")
    db.session.commit()

    click.echo("Adding poems...")
    with open('Texts/FreeTexts/OdeOnIndolence.txt', "r") as poem:
        db.session.add(Poem(title='Ode on Indolence',
                            keyword='OdeOnIndolence',
                            raw_text=str(poem.read()),
                            poet_id=1,
                            meter_id=1))
    with open('Texts/FreeTexts/OldManWithBeard.txt', "r") as poem:
        db.session.add(Poem(title='There Was an Old Man with a Beard',
                            keyword='OldManWithBeard',
                            raw_text=str(poem.read()),
                            poet_id=2,
                            meter_id=2))
    with open('Texts/FreeTexts/Flea.txt', "r") as poem:
        db.session.add(Poem(title='The Flea',
                            keyword='Flea',
                            raw_text=str(poem.read()),
                            poet_id=3,
                            meter_id=1))
    with open('Texts/FreeTexts/AnthemForDoomedYouth.txt', "r") as poem:
        db.session.add(Poem(title='Anthem for Doomed Youth',
                            keyword='AnthemForDoomedYouth',
                            raw_text=str(poem.read()),
                            poet_id=4,
                            meter_id=1))

    click.echo("Commiting to database...")
    db.session.commit()

    click.echo("Database reset!")


if __name__ == "__main__":
    application.run()
