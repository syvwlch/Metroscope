"""Helper functions for poetry views.py"""

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


def rhymes(lines):
    """Create a dict with the rhymes in the lines."""
    rhymes = {"None": "_"}
    for line in lines:
        rhymes.setdefault(
            str(line.rhyming_part),
            rhyme_designator(len(rhymes)-1),
        )
    return rhymes


def lines(stanza, pattern):
    """Create a list of LineBuilder instances from a stanza."""
    lines = []
    for line in stanza.split("\n"):
        if line != "":
            lb = LineBuilder(
                line=line,
                pattern=pattern,
                custom_dict=CUSTOM_DICT,
            )
            lines.append(lb)
    return lines


def stanzas(poem, pattern):
    """
    Create a list of stanzas from the poem.

    Each stanza will include:
        - a list of LineBuilder instances, and
        - a dictionary of the rhymes.
    """
    stanzas = []
    for stanza in poem.split("\n\n"):
        verses = lines(stanza, pattern)
        stanzas.append([verses, rhymes(verses)])
    return stanzas
