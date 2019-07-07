"""Create the flask app from the factory in the run package."""

import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from flask_bootstrap import Bootstrap
from run import create_app

db = SQLAlchemy()
bootstrap = Bootstrap()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


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


@app.cli.command('deploy')
def deploy_command():
    """Run the (idempotent) deployment tasks."""
    from run.models import Meter, Poet, Poem

    # Migrate the database to the latest revision
    upgrade()

    # create or update the sample meters, poets, and poems
    Meter.insert_samples()
    Poet.insert_samples()
    Poem.insert_samples()
