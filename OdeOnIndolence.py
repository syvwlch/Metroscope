"""Analysis of Keat's Ode on Indolence."""

from flask import Flask
from Metroscope import stress_line

app = Flask(__name__)
POEM_PATH = "Texts/FreeTexts/OdeOnIndolence.txt"
POEM_METER = "x/x/x/x/x/"


@app.route("/")
def home():
    """Define the home route."""
    return scanned_poem(POEM_PATH, POEM_METER)


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
            # print(line, end="")
    return result


if __name__ == "__main__":
    app.run()
