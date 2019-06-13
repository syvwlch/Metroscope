"""Run script for the website."""

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from Metroscope import scanned_poem

application = Flask(__name__)
bootstrap = Bootstrap(application)


@application.route("/")
def home():
    """Define the home route."""
    return render_template("home.html")


@application.route("/about")
def about():
    """Define the about route."""
    return render_template("about.html")


@application.route("/poem/<filename>")
def poem(filename):
    """Define the poem route."""
    if filename == "OdeOnIndolence":
        POEM_TITLE = "Ode on Indolence"
        POET_NAME = "John Keats"
        POEM_PATH = "Texts/FreeTexts/OdeOnIndolence.txt"
        METER_NAME = "strict iambic pentameter"
        METER_PATTERN = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, ]
    else:
        return render_template('404.html'), 404
    return render_template("poem.html",
                           title=POEM_TITLE,
                           poet=POET_NAME,
                           meter=METER_NAME,
                           poem=scanned_poem(POEM_PATH, METER_PATTERN),
                           )


@application.errorhandler(404)
def page_not_found(e):
    """Define the route for the 404 error page."""
    return render_template('404.html'), 404


@application.errorhandler(500)
def internal_server_error(e):
    """Define the route for the 500 error page."""
    return render_template('500.html'), 500


if __name__ == "__main__":
    application.run()
