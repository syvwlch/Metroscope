"""Route definitions for the poetry blueprint."""

from flask import render_template, redirect, url_for
from flask_login import current_user
from run import db
from . import poetry
from ..models import Meter, Poet, Poem, Permission
from .helpers import stanzas
from .forms import ChangeMeterForm


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

    if current_user.can(Permission.CHANGE_METER):
        form = ChangeMeterForm()
        meters = Meter.query.order_by('name').all()
        # move the poem's default meter to the top of the drop-down
        meters.insert(0, meters.pop(meters.index(poem.meter)))
        form.pattern.choices = [(m.pattern, m.name) for m in meters]

        if form.validate_on_submit():
            pattern = form.pattern.data
            meter = Meter.query.filter_by(pattern=pattern).first().name
        else:
            pattern = poem.meter.pattern
            meter = poem.meter.name
    else:
        form = None
        meter = poem.meter.name
        pattern = poem.meter.pattern

    return render_template(
        "poetry/poem.html",
        form=form,
        title=poem.title,
        poet=poem.author.name,
        meter=meter,
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
