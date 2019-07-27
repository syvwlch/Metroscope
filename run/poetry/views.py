"""Route definitions for the poetry blueprint."""

from flask import render_template, redirect, url_for
from run import db
from . import poetry
from ..models import Meter, Poet, Poem
from .helpers import stanzas
from .forms import PoemForm


@poetry.route("/poem")
def poem_list():
    if "poems" not in db.engine.table_names():
        poems = []
    else:
        poems = Poem.query.all()
    return render_template("poetry/poem_list.html", poems=poems)


@poetry.route("/poem/<keyword>", methods=['GET', 'POST'])
def poem(keyword):
    """Define the poem route."""
    # if the poems table does not exist, 404 the route
    if "poems" not in db.engine.table_names():
        return render_template('main/404.html'), 404

    # retrieve the requested poem if it exists
    poem = Poem.query.filter_by(keyword=keyword).first_or_404()

    form = PoemForm()
    meters = Meter.query.order_by('name').all()
    # move the poem's default meter to the top of the drop-down
    meters.insert(0, meters.pop(meters.index(poem.meter)))
    form.pattern.choices = [(m.pattern, m.name) for m in meters]

    if form.validate_on_submit():
        pattern = form.pattern.data
    else:
        pattern = poem.meter.pattern

    return render_template(
        "poetry/poem.html",
        form=form,
        title=poem.title,
        poet=poem.author.name,
        meter=poem.meter.name,
        stanzas=stanzas(poem.raw_text, pattern),
    )


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
