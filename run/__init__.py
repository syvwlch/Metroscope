"""Set up the application factory for the site."""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from config import config

db = SQLAlchemy()
bootstrap = Bootstrap()


def create_app(config_name):
    """Create the app instance."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    """Add a shell context processor."""
    from run.models import Meter, Poet, Poem, reset_db
    return dict(db=db,
                Meter=Meter,
                Poet=Poet,
                Poem=Poem,
                reset_db=reset_db,
                )
