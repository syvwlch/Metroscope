"""Route definitions for the main blueprint."""

import os
from flask import render_template
from . import main
import markdown


@main.route("/")
def home():
    """Define the home route."""
    return render_template("main/home.html")


@main.route("/about")
def about():
    """Define the about route."""
    ABOUT_FILE = os.environ.get('ABOUT_FILE') or 'README.md'
    try:
        with open(ABOUT_FILE, "r") as readme:
            ABOUT_CONTENTS = markdown.markdown(readme.read())
    except IOError:
        ABOUT_CONTENTS = "Failed to load the contents of the about page."
    return render_template("main/about.html",
                           contents=ABOUT_CONTENTS,
                           )
