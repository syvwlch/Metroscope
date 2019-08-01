"""Route definitions for the poetry blueprint."""

from flask import render_template, redirect, url_for
from flask_login import current_user
from run import db
from . import poetry
from ..models import Meter, Poet, Poem, Permission
from .helpers import stanzas
from .forms import (
    PoemChangeMeterForm,
    PoemSetDefaultMeterForm,
    MeterUpdateForm,
    MeterAddForm,
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
        poet=poem.author.name,
        meter=meter,
        stanzas=stanzas(poem.raw_text, meter.pattern),
    )


@poetry.route("/meter")
def meter_list():
    if "meters" not in db.engine.table_names():
        meters = []
    else:
        meters = Meter.query.order_by('name').all()
    return render_template("poetry/meter_list.html", meters=meters)


@poetry.route("/meter/<keyword>", methods=['GET', 'POST'])
def meter(keyword):
    """Define the meter route."""
    # if the meters table does not exist, 404 the route
    if "meters" not in db.engine.table_names():
        return render_template('main/404.html'), 404

    if keyword == 'new':
        meter = None
        poems = []
        form = MeterAddForm()

        if form.validate_on_submit():
            if current_user.can(Permission.ADD_METER):
                meter = Meter(
                    name=form.name.data,
                    pattern=form.pattern.data,
                )
                db.session.add(meter)
                db.session.commit()
                keyword = Meter.query.filter_by(
                    pattern=form.pattern.data
                ).first().id
                return redirect(url_for('poetry.meter', keyword=keyword))
    else:
        # retrieve the requested meter if it exists
        meter = Meter.query.get_or_404(keyword)

        # retrieve the poems which use this meter, if any
        poems = Poem.query.filter_by(meter=meter).all()
        if poems is None:
            poems = []

        if current_user.can(Permission.ADD_METER):
            form = MeterUpdateForm()
            form.id.data = str(meter.id)
            if form.validate_on_submit():
                meter.name = form.name.data
                meter.pattern = form.pattern.data
                db.session.commit()
            else:
                form.name.data = meter.name
                form.pattern.data = meter.pattern
        else:
            form = None

    return render_template(
        "poetry/meter.html",
        form=form,
        meter=meter,
        poems=poems,
    )
