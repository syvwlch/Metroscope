"""Route definitions for the poetry blueprint."""

from flask import render_template, redirect, url_for
from flask_login import current_user
from run import db
from .. import poetry
from ...models import Poet, Poem, Permission
from ..forms import (
    PoetUpdateForm,
    PoetAddForm,
    PoetDeleteForm,
)


@poetry.route("/poet")
def poet_list():
    if "poets" not in db.engine.table_names():
        poets = []
    else:
        poets = Poet.query.order_by('name').all()
    return render_template("poetry/poet_list.html", poets=poets)


@poetry.route("/poet/<keyword>", methods=['GET', 'POST'])
def poet(keyword):
    """Define the poet route."""
    # if the poet table does not exist, 404 the route
    if "poets" not in db.engine.table_names():
        return render_template('main/404.html'), 404

    if keyword == 'new':
        poet = None
        poems = []
        form = PoetAddForm()
        delete_form = None

        if form.validate_on_submit():
            if current_user.can(Permission.ADD_POEM):
                poet = Poet(
                    name=form.name.data,
                )
                db.session.add(poet)
                db.session.commit()
                keyword = poet.query.filter_by(
                    name=form.name.data
                ).first().id
                return redirect(url_for('poetry.poet', keyword=keyword))
    else:
        # retrieve the requested poet if they exist
        poet = Poet.query.get_or_404(keyword)

        # retrieve the poems written by this poet, if any
        poems = Poem.query.filter_by(author=poet).all()
        if poems is None:
            poems = []

        if current_user.can(Permission.ADD_POEM):
            form = PoetUpdateForm()
            form.id.data = keyword
            if form.validate_on_submit():
                poet.name = form.name.data
                db.session.commit()
                return redirect(url_for('poetry.poet', keyword=keyword))
            form.name.data = poet.name
        else:
            form = None

        if current_user.can(Permission.ADD_POEM) and poems == []:
            delete_form = PoetDeleteForm()
            delete_form.id.data = keyword
            if delete_form.validate_on_submit():
                db.session.delete(poet)
                db.session.commit()
                return redirect(url_for('poetry.poet_list'))
            form.name.data = poet.name
        else:
            delete_form = None

    return render_template(
        "poetry/poet.html",
        form=form,
        delete_form=delete_form,
        poet=poet,
        poems=poems,
    )
