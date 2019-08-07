"""Route definitions for the poetry blueprint."""

from flask import render_template, redirect, url_for
from .. import poetry
from ...models import Meter, Poet, Poem


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
