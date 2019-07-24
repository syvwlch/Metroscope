"""Route definitions for the poetry blueprint."""

from flask import render_template, redirect, url_for
from run import db
from . import poetry
from ..models import Meter, Poet, Poem
from metroscope import LineBuilder, CUSTOM_DICT


def rhyme_designator(index):
    """
    Returns a string with an uppercase letter and a modifier.

    The modifier indicates how many times around the alphabet the index has
    gone, e.g. for index = 27, the string is A'.
    """
    from string import ascii_uppercase
    num = len(ascii_uppercase)
    letter = ascii_uppercase[index % num]
    modifier = index // num
    if modifier == 0:
        modifier = ""
    else:
        modifier = str(modifier)
    return letter + modifier


def scanned_poem(poem, pattern):
    """
    Create a list of stanzas from the poem.

    Each stanza will be a list of LineBuilder instances.
    """
    stanzas = []
    for stanza in poem.split("\n\n"):
        rhymes = {"None": "_"}
        lines = []
        for line in stanza.split("\n"):
            if line != "":
                lb = LineBuilder(
                    line=line,
                    pattern=pattern,
                    custom_dict=CUSTOM_DICT,
                )
                rp = str(lb._rhyming_part)
                try:
                    rd = rhymes[rp]
                except KeyError:
                    rhymes.update({rp: rhyme_designator(len(rhymes)-1)})
                    rd = rhymes[rp]
                lb.rhyme_designator = rd
                lines.append(lb)
        stanzas.append(lines)
    return stanzas


@poetry.route("/poem")
def poem_list():
    if "poems" not in db.engine.table_names():
        poems = []
    else:
        poems = Poem.query.all()
    return render_template("poetry/poem_list.html", poems=poems)


@poetry.route("/poem/<keyword>")
def poem(keyword):
    """Define the poem route."""
    # if the poems table does not exist, 404 the route
    if "poems" not in db.engine.table_names():
        return render_template('main/404.html'), 404

    # retrieve the requested poem if it exists
    poem = Poem.query.filter_by(keyword=keyword).first_or_404()

    return render_template(
        "poetry/poem.html",
        title=poem.title,
        poet=poem.author.name,
        meter=poem.meter.name,
        stanzas=scanned_poem(poem.raw_text, poem.meter.pattern),
    )


@poetry.route("/add_samples")
def add_samples():
    """Define the add_samples route."""
    try:
        Meter.insert_samples()
        Poet.insert_samples()
        Poem.insert_samples()
    except Exception:
        return render_template('main/404.html'), 404
    return redirect(url_for('main.home'))
