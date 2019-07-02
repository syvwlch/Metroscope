"""Route definitions for the site."""

from flask import render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from metroscope import scanned_poem
import markdown
from run import app
from run.models import db, Poem, reset_db

bootstrap = Bootstrap(app)


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
