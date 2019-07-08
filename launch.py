"""Create the flask app from the factory in the run package."""

import os
from run import create_app, db


app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    """Add a shell context processor."""
    from run.models import Meter, Poet, Poem, reset_db
    return dict(
                db=db,
                Meter=Meter,
                Poet=Poet,
                Poem=Poem,
                reset_db=reset_db,
                )


@app.cli.command('samples')
def samples_command():
    """Inject the samples idempotently."""
    from run.models import Meter, Poet, Poem
    # create or update the sample meters, poets, and poems
    Meter.insert_samples()
    Poet.insert_samples()
    Poem.insert_samples()
