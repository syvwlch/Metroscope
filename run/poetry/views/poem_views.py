"""Route definitions for the poetry blueprint."""

from flask import render_template, redirect, url_for
from flask_login import current_user
from run import db
from .. import poetry
from ...models import Meter, Poem, Permission
from ..helpers import stanzas
from ..forms import (
    PoemChangeMeterForm,
    PoemSetDefaultMeterForm,
)


@poetry.route("/poem")
def poem_list():
    if "poems" not in db.engine.table_names():
        poems = []
    else:
        poems = Poem.query.order_by('title').all()
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
        form = PoemSetDefaultMeterForm()
    else:
        form = PoemChangeMeterForm()

    meters = Meter.query.order_by('name').all()
    # move the poem's default meter to the top of the drop-down
    meters.insert(0, meters.pop(meters.index(poem.meter)))
    form.pattern.choices = [(m.pattern, m.name) for m in meters]
    default_pattern, default_name = form.pattern.choices[0]
    form.pattern.choices[0] = (default_pattern, default_name + ' (default)')

    if form.validate_on_submit():
        meter = Meter.query.filter_by(pattern=form.pattern.data).first()
        if (current_user.can(Permission.CHANGE_METER)
                and form.set_as_default.data is True):
            poem.meter = meter
            db.session.commit()
            form.set_as_default.data = False
            return redirect(url_for('poetry.poem', keyword=keyword))
    else:
        meter = poem.meter

    return render_template(
        "poetry/poem.html",
        form=form,
        title=poem.title,
        poet=poem.author,
        meter=meter,
        stanzas=stanzas(poem.raw_text, meter.pattern),
    )
