"""Experiments with scanning meter."""

from pronouncing import stresses_for_word
from syllabipy.sonoripy import SonoriPy


class WordBuilder(object):
    """
    Prepare a given word for analysis.

    Word is given as it is in the original, and the class provides a lowercase
    version ready for CMU lookup and syllable separation, as well as a list of
    syllable objects with various properties.
    """

    def __init__(self, word):
        """Initialize from original word."""
        self.word = word
        self.syllables = SonoriPy(word.lower())
        self.stresses = get_stress_word(word)

    def __str__(self):
        """Create the informal string representation of the class."""
        return self.word

    def __repr__(self):
        """Create the formal string representation of the class."""
        return "WordBuilder('" + self.word + "')"

    @property
    def stressed_syllables(self):
        """Return a read-only list of the original word's syllables."""
        word = self.word
        syllables = self.syllables
        stresses = self.stresses
        result = []
        for syllable in syllables:
            if len(stresses) > 1:
                result.append([word[0:len(syllable)], stresses.pop(0)])
                word = word[len(syllable):]
            elif len(stresses) == 1:
                result.append([word, stresses.pop(0)])
            else:
                pass
        return result


def clean_word(word):
    """Prepare a word for CMU lookup."""
    clean = word
    # First, force lowercase and strip punctuation
    clean = clean.lower()
    for punct in ".,;:!?—'\"":
        clean = clean.replace(punct, "")
    # Many poets mark added stress on a silent e with an è
    clean = clean.replace("è", "e")
    # Many poets mark elided vowels with a ’ at the end of a wor
    if clean[-2:] == "’s":
        clean = clean.replace("’s", "")
    clean = clean.replace("’d", "ed")
    return clean


def get_stress_word(word):
    """Return a list of the stresses for the given word."""
    custom_dict = {
                    "phidian": "20",
                    "indolence": "200",
                    "benumbed": "02",
                    "unhaunted": "020",
                    "nothingness": "202",
                    "embroidered": "020",
                    "besprinkled": "020",
                    "o’er": "0",
                    "unmeek": "02",
                    "poesy": "202",
                    "forsooth": "02",
                    "honeyed": "20",
                    "casement": "20",
                    "leaved": "2",
                    "throstle": "20",
                    "’twas": "2",
                    "dieted": "202",
                    "masque": "2",
                    "spright": "2",
                    "flow’rs": "2",
                    "deniest": "20",
                    "know’st": "2",
                    "triumph’st": "20",
                    "say’st": "2",
                    "find’st": "2",
                    "yield’st": "2",
                    "’tis": "2",
                    "purpled": "20",
                    "maidenhead": "202",
                    "orisons": "200",
                    "mockeries": "200",
                    "pallor": "20",
                  }
    cleaned_word = clean_word(word)
    try:
        word_stresses = custom_dict[cleaned_word]
    except KeyError:
        try:
            word_stresses = stresses_for_word(cleaned_word)[0]
        except IndexError:
            word_stresses = ""
    if "è" in word:
        word_stresses += "1"
    return list(word_stresses)


def get_syllables_word(word):
    """
    Retrieve the syllables for a given word.

    Returns a list of [syllable text, syllable stress].
    """
    syllables = SonoriPy(word.lower())
    stresses = get_stress_word(word)
    result = []
    for syllable in syllables:
        if len(stresses) > 1:
            result.append([word[0:len(syllable)], stresses.pop(0)])
            word = word[len(syllable):]
        elif len(stresses) == 1:
            result.append([word, stresses.pop(0)])
        else:
            pass
    return result


def clean_line(line):
    """Prepare a line of text for show_stress_line."""
    clean = line
    for sep in "—-":
        clean = clean.replace(sep, " ")
    return clean


def tag_string(snippet, tag, style=""):
    """Wrap a text snippet with an html tag."""
    opening_tag = "<" + tag + " style='" + style + "'>"
    closing_tag = "</" + tag + ">"
    return opening_tag + snippet + closing_tag


def stress_word(word, stresses):
    """
    Mark up a word based on the stress pattern provided.

    Return the word with the stresses syllables wrapped with a <strong> tag,
    and a <span> tag around the entire word.
    Adds a style attribute based on whether the syllable's normal stress
    aligns with the expected meter.
    """
    MATCH = "color:black"
    NOT_MATCH = "color:red"
    syllables = get_syllables_word(word)
    result = ""
    for syllable, pronunciation_stress in syllables:
        if stresses:
            if stresses.pop(0):
                if pronunciation_stress == '0':
                    result += tag_string(syllable, "strong", NOT_MATCH)
                else:
                    result += tag_string(syllable, "strong", MATCH)
            else:
                if pronunciation_stress == '2':
                    result += tag_string(syllable, "span", NOT_MATCH)
                else:
                    result += tag_string(syllable, "span", MATCH)
        else:
            result += tag_string(syllable, "small", NOT_MATCH)
    return tag_string(result, "span")


def stress_line(line, stress_pattern):
    """Mark up a line of verse based on the stress pattern provided."""
    stressed_line = ""
    line = clean_line(line)
    for word in line.split():
        word_stresses = get_stress_word(word)
        number_stresses = len(word_stresses)
        word_meter = stress_pattern[0:number_stresses]
        stress_pattern = stress_pattern[number_stresses:]
        # use the stress pattern directly for the word stresses
        word_stresses = word_meter
        # -----------------------------------------------------
        stressed_line += stress_word(word, word_stresses) + " "
    for stress in stress_pattern:
        stressed_line += "<b style='color:red'> _ </b>"
    return stressed_line


def scanned_poem(path, meter):
    """
    Create HTML with the scanned poem.

    Wrap the poem in a <div> tag, each stanza in a <p> tag,
    and end each line with a <br> tag.
    """
    result = "<div>\n<p>\n"
    with open(path, "r") as poem:
        for line in poem:
            if line == "\n":
                result += "</p>\n<p>"
            else:
                result += stress_line(line, meter)
                result += "<br>\n"
    result += "</p>\n</div>"
    return result


if __name__ == "__main__":
    print("This is a module, import it into a script to use.")
