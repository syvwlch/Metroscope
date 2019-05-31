"""Analysis of Keat's Ode on Indolence."""

from flask import Flask, render_template
from Metroscope import stress_line

app = Flask(__name__)
POEM_TITLE = "Ode on Indolence"
POET_NAME = "John Keats"
POEM_PATH = "Texts/FreeTexts/OdeOnIndolence.txt"
METER_NAME = "strict iambic pentameter"
METER_PATTERN = "x/x/x/x/x/"


@app.route("/")
def home():
    """Define the home route."""
    return render_template("poem.html",
                           title=POEM_TITLE,
                           poet=POET_NAME,
                           meter=METER_NAME,
                           poem=scanned_poem(POEM_PATH, METER_PATTERN),
                           )


def scanned_poem(path, meter):
    """Create a multiline string with the scanned poem."""
    result = ""
    with open(path, "r") as poem:
        for line in poem:
            aligned_stresses, stressed_line = stress_line(line, meter)
            # result += aligned_stresses
            # result += "<br>\n"
            result += stressed_line
            result += "<br>\n"
    return result


if __name__ == "__main__":
    app.run()
