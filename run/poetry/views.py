"""Route definitions for the analyze blueprint."""

from flask import render_template, redirect, url_for
from run import db
from . import poetry
from ..models import Meter, Poet, Poem


@poetry.route("/poem/<keyword>")
def poem(keyword):
    """Define the poem route."""
    # if the poems table does not exist, 404 the route
    if "poems" not in db.engine.table_names():
        return render_template('main/404.html'), 404

    # retrieve the requested poem if it exists
    poem = Poem.query.filter_by(keyword=keyword).first_or_404()

    return render_template("poetry/poem.html",
                           title=poem.title,
                           poet=poem.author.name,
                           meter=poem.meter.name,
                           poem=poem.HTML)


@poetry.route("/add_samples")
def add_samples():
    """Define the add_samples route."""
    try:
        Meter.insert_samples()
        Poet.insert_samples()
        Poem.insert_samples()
    except Exception:
        return render_template('main/404.html'), 404
    return redirect(url_for('main.home'))
