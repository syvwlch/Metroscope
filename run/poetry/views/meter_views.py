"""Route definitions for the poetry blueprint."""

from flask import render_template, redirect, url_for
from flask_login import current_user
from run import db
from .. import poetry
from ...models import Meter, Poem, Permission
from ..forms import (
    MeterUpdateForm,
    MeterAddForm,
    MeterDeleteForm,
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
        delete_form = None

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
            form.id.data = keyword
            if form.validate_on_submit():
                meter.name = form.name.data
                meter.pattern = form.pattern.data
                db.session.commit()
                return redirect(url_for('poetry.meter', keyword=keyword))
            form.name.data = meter.name
            form.pattern.data = meter.pattern
        else:
            form = None

        if current_user.can(Permission.ADD_METER) and poems == []:
            delete_form = MeterDeleteForm()
            delete_form.id.data = keyword
            if delete_form.validate_on_submit():
                db.session.delete(meter)
                db.session.commit()
                return redirect(url_for('poetry.meter_list'))
            form.name.data = meter.name
        else:
            delete_form = None

    return render_template(
        "poetry/meter.html",
        form=form,
        delete_form=delete_form,
        meter=meter,
        poems=poems,
    )
