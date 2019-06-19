"""Experiments with scanning meter."""

from pronouncing import stresses_for_word
from nltk import SyllableTokenizer

SSP = SyllableTokenizer()

CUSTOM_DICT = {
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


class WordBuilder(object):
    """
    Prepare a given word for analysis.

    Word is given as it is in the original, and the class provides a lowercase
    version ready for CMU lookup and syllable separation, as well as a list of
    syllable objects with various properties.
    """

    def __init__(self, word, custom_dict={}):
        """Initialize from original word."""
        self.word = word
        self.custom_dict = custom_dict

    def __str__(self):
        """Create the informal string representation of the class."""
        return self.word

    def __repr__(self):
        """Create the formal string representation of the class."""
        return "WordBuilder('" + self.word + "')"

    @property
    def syllables(self):
        """Return the syllables of the original word."""
        return SSP.tokenize(self.word)

    @property
    def stresses(self):
        """Return a list of the stresses for the given word."""
        cleaned_word = self.clean_word
        try:
            word_stresses = self.custom_dict[cleaned_word]
        except (KeyError, TypeError):
            try:
                word_stresses = stresses_for_word(str(cleaned_word))[0]
            except IndexError:
                word_stresses = ""
        if "è" in self.word:
            word_stresses += "1"
        return list(word_stresses)

    @property
    def stressed_syllables(self):
        """Combine the syllables and stresses of the original word."""
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

    @property
    def clean_word(self):
        """Prepare a word for CMU lookup."""
        clean = self.word
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

    def tag_string(self, snippet, tag, style=""):
        """Wrap a text snippet with an html tag."""
        if style == "":
            opening_tag = "<" + tag + ">"
        else:
            opening_tag = "<" + tag + " style='" + style + "'>"
        closing_tag = "</" + tag + ">"
        return opening_tag + snippet + closing_tag

    def stressed_HTML(self, pattern):
        """
        Mark up the original word based on the stress pattern provided.

        Return the word with the syllables wrapped with HTML tags based on
        their stress in the pattern, with a style attribute based on whether
        it aligns with the expected meter.
        Finally, wrap a <span> tag around the entire word.
        """
        MATCH = "color:black"
        NOT_MATCH = "color:red"
        STRESSED = "strong"
        UNSTRESSED = "span"
        UNKNOWN = "small"

        result = ""
        for syllable, pronunciation_stress in self.stressed_syllables:
            if pattern:
                if pattern.pop(0):
                    if pronunciation_stress == '0':
                        result += self.tag_string(syllable,
                                                  STRESSED,
                                                  NOT_MATCH)
                    else:
                        result += self.tag_string(syllable,
                                                  STRESSED,
                                                  MATCH)
                else:
                    if pronunciation_stress == '2':
                        result += self.tag_string(syllable,
                                                  UNSTRESSED,
                                                  NOT_MATCH)
                    else:
                        result += self.tag_string(syllable,
                                                  UNSTRESSED,
                                                  MATCH)
            else:
                result += self.tag_string(syllable,
                                          UNKNOWN,
                                          NOT_MATCH)
        return self.tag_string(result, "span")


class LineBuilder(object):
    """
    Prepare a given line of verse for analysis.

    Line is stored as a list of instances of the WordBuilder class.
    Various representations as strings are provided, including the HTML used
    on the website.
    """

    def __init__(self, line):
        """Initialize from original line."""
        self.line = line

    def __str__(self):
        """Create the informal string representation of the class."""
        return self.line

    def __repr__(self):
        """Create the formal string representation of the class."""
        return "LineBuilder('" + self.line + "')"

    def clean_line(self):
        """Prepare a line for splitting on spaces."""
        clean = self.line
        for sep in "—-":
            clean = clean.replace(sep, " ")
        return clean

    def word_list(self):
        """Create the list of WordBuilder instances."""
        word_list = []
        for word in self.clean_line().split():
            word_list.append(WordBuilder(word, custom_dict=CUSTOM_DICT))
        return word_list

    def stressed_HTML(self, stress_pattern):
        """Mark up the line based on the stress pattern provided."""
        MISSING = "<b style='color:red'> _ </b>"

        stressed_line = ""
        for word in self.word_list():
            number_stresses = len(word.stresses)
            word_meter = stress_pattern[0:number_stresses]
            stress_pattern = stress_pattern[number_stresses:]
            # use the stress pattern directly for the word stresses
            stressed_line += word.stressed_HTML(word_meter) + " "
        for stress in stress_pattern:
            stressed_line += MISSING
        return stressed_line


"""
Everything below this point is pre-refactoring code.

The site runs on the code below right now, while unit tests
run on the code above.
"""


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
                # result += stress_line(line, meter)
                result += LineBuilder(line).stressed_HTML(meter)
                result += "<br>\n"
    result += "</p>\n</div>"
    return result


if __name__ == "__main__":
    print("This is a module, import it into a script to use.")
