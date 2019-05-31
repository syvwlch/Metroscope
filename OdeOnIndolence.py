"""Analysis of Keat's Ode on Indolence."""

from flask import Flask, render_template
from Metroscope import scanned_poem

app = Flask(__name__)


@app.route("/")
def home():
    """Define the home route."""
    return render_template("poem.html",
                           title=POEM_TITLE,
                           poet=POET_NAME,
                           meter=METER_NAME,
                           poem=scanned_poem(POEM_PATH, METER_PATTERN),
                           )


if __name__ == "__main__":
    app.run()
