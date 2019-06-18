"""Run script for the website."""

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from Metroscope import scanned_poem
import markdown

application = Flask(__name__)
bootstrap = Bootstrap(application)


@application.route("/")
def home():
    """Define the home route."""
    return render_template("home.html")


@application.route("/about")
def about():
    """Define the about route."""
    try:
        with open("README.md", "r") as readme:
            ABOUT_CONTENTS = markdown.markdown(readme.read())
    except IOError:
        ABOUT_CONTENTS = "Failed to load the contents of the about page."
    return render_template("about.html",
                           contents=ABOUT_CONTENTS,
                           )


@application.route("/poem/<filename>")
def poem(filename):
    """Define the poem route."""
    if filename == "OdeOnIndolence":
        POEM_TITLE = "Ode on Indolence"
        POET_NAME = "John Keats"
        POEM_PATH = "Texts/FreeTexts/OdeOnIndolence.txt"
        METER_NAME = "strict iambic pentameter"
        METER_PATTERN = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, ]
    elif filename == "OldManWithBeard":
        POEM_TITLE = "There Was an Old Man with a Beard"
        POET_NAME = "Edward Lear"
        POEM_PATH = "Texts/FreeTexts/OldManWithBeard.txt"
        METER_NAME = "anapestic trimeter"
        METER_PATTERN = [0, 1, 0, 0, 1, 0, 0, 1, ]
    elif filename == "Flea":
        POEM_TITLE = "The Flea"
        POET_NAME = "John Donne"
        POEM_PATH = "Texts/FreeTexts/Flea.txt"
        METER_NAME = "strict iambic pentameter"
        METER_PATTERN = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, ]
    elif filename == "AnthemForDoomedYouth":
        POEM_TITLE = "Anthem for Doomed Youth"
        POET_NAME = "Wilfred Owen"
        POEM_PATH = "Texts/FreeTexts/AnthemForDoomedYouth.txt"
        METER_NAME = "strict iambic pentameter"
        METER_PATTERN = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, ]
    elif filename == "NearingForty":
        POEM_TITLE = "Nearing Forty"
        POET_NAME = "Derek Walcott"
        POEM_PATH = "Texts/FreeTexts/NearingForty.txt"
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
