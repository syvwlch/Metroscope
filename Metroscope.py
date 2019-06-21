"""Experiments with scanning meter."""

from pronouncing import stresses_for_word, phones_for_word, rhyming_part
from nltk import SyllableTokenizer

SSP = SyllableTokenizer()

CUSTOM_DICT = {
                "phidian": {"syllables": ["phi", "dian"],
                            "stresses": "20"},
                "indolence": {"syllables": ["in", "do", "lence"],
                              "stresses": "201"},
                "benumbed": {"syllables": ["be", "numbed"],
                             "stresses": "02"},
                "unhaunted": {"syllables": ["un", "haun", "ted"],
                              "stresses": "020"},
                "nothingness": {"syllables": ["no", "thing", "ness"],
                                "stresses": "202"},
                "embroidered": {"syllables": ["em", "broi", "dered"],
                                "stresses": "020"},
                "besprinkled": {"syllables": ["be", "sprin", "kled"],
                                "stresses": "020"},
                "o’er": {"syllables": ["o’er"],
                         "stresses": "1"},
                "unmeek": {"syllables": ["un", "meek"],
                           "stresses": "01"},
                "poesy": {"syllables": ["po", "e", "sy"],
                          "stresses": "202"},
                "forsooth": {"syllables": ["for", "sooth"],
                             "stresses": "02"},
                "honeyed": {"syllables": ["ho", "neyed"],
                            "stresses": "20"},
                "casement": {"syllables": ["case", "ment"],
                             "stresses": "20"},
                "leaved": {"syllables": ["leaved"],
                           "stresses": "1"},
                "throstle": {"syllables": ["thro", "stle"],
                             "stresses": "20"},
                "farewell": {"syllables": ["fare", "well"],
                             "stresses": "12"},
                "’twas": {"syllables": ["’twas"],
                          "stresses": "2"},
                "dieted": {"syllables": ["di", "e", "ted"],
                           "stresses": "202"},
                "masque": {"syllables": ["masque"],
                           "stresses": "2"},
                "fall’n": {"syllables": ["fall’n"],
                           "stresses": "2"},
                "spright": {"syllables": ["spright"],
                            "stresses": "2"},
                "flowers": {"syllables": ["flowers"],
                            "stresses": "2"},
                "flower": {"syllables": ["flower"],
                           "stresses": "2"},
                "flowery": {"syllables": ["flow", "ery"],
                            "stresses": "21"},
                "deniest": {"syllables": ["de", "niest"],
                            "stresses": "20"},
                "know’st": {"syllables": ["know’st"],
                            "stresses": "2"},
                "triumph’st": {"syllables": ["tri", "umph’st"],
                               "stresses": "20"},
                "say’st": {"syllables": ["say’st"],
                           "stresses": "2"},
                "find’st": {"syllables": ["find’st"],
                            "stresses": "2"},
                "yield’st": {"syllables": ["yield’st"],
                             "stresses": "2"},
                "’tis": {"syllables": ["’tis"],
                         "stresses": "2"},
                "purpled": {"syllables": ["pur", "pled"],
                            "stresses": "20"},
                "maidenhead": {"syllables": ["mai", "den", "head"],
                               "stresses": "202"},
                "orisons": {"syllables": ["o", "ri", "son"],
                            "stresses": "201"},
                "mockeries": {"syllables": ["mocke", "ries"],
                              "stresses": "20"},
                "pallor": {"syllables": ["pa", "llor"],
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
        self._is_in_custom_dict = self._clean_word in self.custom_dict

    def __str__(self):
        """Create the informal string representation of the class."""
        return self.word

    def __repr__(self):
        """Create the formal string representation of the class."""
        return "WordBuilder('" + self.word + "')"

    @property
    def syllables(self):
        """Return the syllables of the original word."""
        if self._is_in_custom_dict:
            word_syllables = self.custom_dict[self._clean_word]["syllables"]
        else:
            word_syllables = SSP.tokenize(self.word)
        return word_syllables

    @property
    def stresses(self):
        """Return a list of the stresses for the given word."""
        if self._is_in_custom_dict:
            word_stresses = self.custom_dict[self._clean_word]["stresses"]
        else:
            try:
                word_stresses = stresses_for_word(str(self._clean_word))[0]
            except IndexError:
                word_stresses = ""
        if "è" in self.word:
            word_stresses += "1"
        return list(word_stresses)

    @property
    def _stressed_syllables(self):
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
    def _clean_word(self):
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

    def _tag_string(self, snippet, tag, style=""):
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
        for syllable, pronunciation_stress in self._stressed_syllables:
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

    @property
    def _rhyming_part(self):
        """Return the rhyming part of the original word."""
        if not self._is_in_custom_dict:
            phones = phones_for_word(self._clean_word)
            if phones != []:
                return rhyming_part(phones[0])
        return None

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
            result += self._tag_string(syllable,
                                       TAGS[stress],
                                       STYLES[match])
        return self._tag_string(result, "span")


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

    def _clean_line(self):
        """Prepare a line for splitting on spaces."""
        clean = self.line
        for sep in "—-":
            clean = clean.replace(sep, " ")
        return clean

    @property
    def _word_list(self):
        """Create the list of WordBuilder instances."""
        word_list = []
        for word in self._clean_line().split():
            word_list.append(WordBuilder(word, custom_dict=CUSTOM_DICT))
        return word_list

    @property
    def _rhyming_part(self):
        """Return the rhyming part of the line's last word."""
        return self._word_list[-1]._rhyming_part

    def stressed_HTML(self, stress_pattern):
        """Mark up the line based on the stress pattern provided."""
        MISSING = "<b style='color:red'> _ </b>"

        stressed_line = ""
        for word in self._word_list:
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
    lines = []
    with open(path, "r") as poem:
        for line in poem:
            if line != "\n":
                lines.append(LineBuilder(line))
            else:
                lines.append(None)

    result = "<div>\n<p>\n"
    for line in lines:
        if line is None:
            result += "</p>\n<p>"
        else:
            result += line.stressed_HTML(meter)
            if line._rhyming_part is not None:
                result += " ______ " + line._rhyming_part
            result += "<br>\n"
    result += "</p>\n</div>"
    return result


if __name__ == "__main__":
    print("This is a module, import it into a script to use.")
