"""Experiments with scanning meter."""

from pronouncing import stresses_for_word
from nltk import SyllableTokenizer

SSP = SyllableTokenizer()

CUSTOM_DICT = {
                "phidian": {"syllables": ["phi", "dian"],
                            "stresses": "20"},
                "indolence": {"syllable": ["in", "do", "lence"],
                              "stresses": "200"},
                "benumbed": {"syllable": ["be", "numbed"],
                             "stresses": "02"},
                "unhaunted": {"syllable": ["un", "haun", "ted"],
                              "stresses": "020"},
                "nothingness": {"syllable": ["no", "thing", "ness"],
                                "stresses": "202"},
                "embroidered": {"syllable": ["em", "broi", "dered"],
                                "stresses": "020"},
                "besprinkled": {"syllable": ["be", "sprin", "kled"],
                                "stresses": "020"},
                "o’er": {"syllable": ["o’er"],
                         "stresses": "0"},
                "unmeek": {"syllable": ["un", "meek"],
                           "stresses": "01"},
                "poesy": {"syllable": ["po", "e", "sy"],
                          "stresses": "202"},
                "forsooth": {"syllable": ["for", "sooth"],
                             "stresses": "02"},
                "honeyed": {"syllable": ["ho", "neyed"],
                            "stresses": "20"},
                "casement": {"syllable": ["case", "ment"],
                             "stresses": "20"},
                "leaved": {"syllable": ["leaved"],
                           "stresses": "2"},
                "throstle": {"syllable": ["thro", "stle"],
                             "stresses": "20"},
                "’twas": {"syllable": ["’twas"],
                          "stresses": "2"},
                "dieted": {"syllable": ["di", "e", "ted"],
                           "stresses": "202"},
                "masque": {"syllable": ["masque"],
                           "stresses": "2"},
                "spright": {"syllable": ["spright"],
                            "stresses": "2"},
                "flow’rs": {"syllable": ["flow’rs"],
                            "stresses": "2"},
                "deniest": {"syllable": ["de", "niest"],
                            "stresses": "20"},
                "know’st": {"syllable": ["know’st"],
                            "stresses": "2"},
                "triumph’st": {"syllable": ["tri", "umph’st"],
                               "stresses": "20"},
                "say’st": {"syllable": ["say’st"],
                           "stresses": "2"},
                "find’st": {"syllable": ["find’st"],
                            "stresses": "2"},
                "yield’st": {"syllable": ["yield’st"],
                             "stresses": "2"},
                "’tis": {"syllable": ["’tis"],
                         "stresses": "2"},
                "purpled": {"syllable": ["pur", "pled"],
                            "stresses": "20"},
                "maidenhead": {"syllable": ["mai", "den", "head"],
                               "stresses": "202"},
                "orisons": {"syllable": ["o", "ri", "son"],
                            "stresses": "200"},
                "mockeries": {"syllable": ["mo", "ke", "ries"],
                              "stresses": "200"},
                "pallor": {"syllable": ["pa", "llor"],
                           "stresses": "20"},
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
        self._is_in_custom_dict = self.clean_word in self.custom_dict

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
        if self._is_in_custom_dict:
            word_stresses = self.custom_dict[cleaned_word]["stresses"]
        else:
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

    def _matched_syllables(self, pattern):
        """
        Match the pronounced stresses against the given pattern.

        Private method in service of stressed_HTML().
        Returns a list of lists:
            - syllable string,
            - Boolean for pattern stress,
            - Boolean for match between pattern & pronunciation
        """
        result = []
        for syllable, pronunciation_stress in self.stressed_syllables:
            if pattern:
                if pattern.pop(0):
                    result.append([syllable,
                                   True,
                                   pronunciation_stress != '0'])
                else:
                    result.append([syllable,
                                   False,
                                   pronunciation_stress != '2'])
            else:
                result.append([syllable,
                               None,
                               False])
        return result

    def stressed_HTML(self, pattern):
        """
        Mark up the original word based on the stress pattern provided.

        Return the word with the syllables wrapped with HTML tags and style
        attributes based on stress, provided meter, and whether they match.
        Finally, wrap a <span> tag around the entire word.
        """
        STYLES = {True: "color:black",
                  False: "color:red"}
        TAGS = {True: "strong",
                False: "span",
                None: "small"}

        result = ""
        for syllable, stress, match in self._matched_syllables(pattern):
            result += self.tag_string(syllable,
                                      TAGS[stress],
                                      STYLES[match])
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
