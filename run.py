"""Analysis of Keat's Ode on Indolence."""

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from Metroscope import scanned_poem

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route("/")
def home():
    """Define the home route."""
    return render_template("home.html")


@app.route("/poem")
def poem():
    """Define the poem route."""
    POEM_TITLE = "Ode on Indolence"
    POET_NAME = "John Keats"
    POEM_PATH = "Texts/FreeTexts/OdeOnIndolence.txt"
    METER_NAME = "strict iambic pentameter"
    METER_PATTERN = "x/x/x/x/x/"
    return render_template("poem.html",
                           title=POEM_TITLE,
                           poet=POET_NAME,
                           meter=METER_NAME,
                           poem=scanned_poem(POEM_PATH, METER_PATTERN),
                           )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run()
