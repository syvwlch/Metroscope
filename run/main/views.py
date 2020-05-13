"""Route definitions for the main blueprint."""

import os
from flask import render_template
from . import main
import markdown


@main.route("/")
def home():
    """Define the home route."""
    ABOUT_FILE = os.environ.get('ABOUT_FILE') or 'README.md'
    try:
        with open(ABOUT_FILE, "r") as readme:
            ABOUT_CONTENTS = markdown.markdown(readme.read())
    except IOError:
        ABOUT_CONTENTS = "Failed to load the contents of the about page."
    return render_template("main/home.html",
                           contents=ABOUT_CONTENTS,
                           )

@main.route("/lessons_learned")
def lessons_learned():
    """Define the lessons_learned route."""
    LESSONS_FILE = 'LESSONS_LEARNED.md'
    try:
        with open(LESSONS_FILE, "r") as lessons:
            LESSONS_CONTENTS = markdown.markdown(lessons.read())
    except IOError:
        LESSONS_CONTENTS = "Failed to load the contents of the lessons learned page."
    return render_template("main/home.html",
                           contents=LESSONS_CONTENTS,
                           )
