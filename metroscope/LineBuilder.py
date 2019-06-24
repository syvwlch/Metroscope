"""The class that provides the representation for a line of verse."""

from metroscope import WordBuilder

CUSTOM_DICT = {
                "phidian": {"syllables": ["phi", "dian"],
                            "stresses": "10"},
                "indolence": {"syllables": ["in", "do", "lence"],
                              "stresses": "102"},
                "benumbed": {"syllables": ["be", "numbed"],
                             "stresses": "01"},
                "unhaunted": {"syllables": ["un", "haun", "ted"],
                              "stresses": "010"},
                "nothingness": {"syllables": ["no", "thing", "ness"],
                                "stresses": "101"},
                "embroidered": {"syllables": ["em", "broi", "dered"],
                                "stresses": "010"},
                "besprinkled": {"syllables": ["be", "sprin", "kled"],
                                "stresses": "010"},
                "o’er": {"syllables": ["o’er"],
                         "stresses": "2"},
                "unmeek": {"syllables": ["un", "meek"],
                           "stresses": "02"},
                "poesy": {"syllables": ["po", "e", "sy"],
                          "stresses": "101"},
                "forsooth": {"syllables": ["for", "sooth"],
                             "stresses": "01"},
                "honeyed": {"syllables": ["ho", "neyed"],
                            "stresses": "10"},
                "casement": {"syllables": ["case", "ment"],
                             "stresses": "10"},
                "leaved": {"syllables": ["leaved"],
                           "stresses": "2"},
                "throstle": {"syllables": ["thro", "stle"],
                             "stresses": "10"},
                "farewell": {"syllables": ["fare", "well"],
                             "stresses": "21"},
                "’twas": {"syllables": ["’twas"],
                          "stresses": "1"},
                "dieted": {"syllables": ["di", "e", "ted"],
                           "stresses": "101"},
                "masque": {"syllables": ["masque"],
                           "stresses": "1"},
                "fall’n": {"syllables": ["fall’n"],
                           "stresses": "1"},
                "spright": {"syllables": ["spright"],
                            "stresses": "1"},
                "flowers": {"syllables": ["flowers"],
                            "stresses": "1"},
                "flower": {"syllables": ["flower"],
                           "stresses": "1"},
                "flowery": {"syllables": ["flow", "ery"],
                            "stresses": "12"},
                "deniest": {"syllables": ["de", "niest"],
                            "stresses": "10"},
                "know’st": {"syllables": ["know’st"],
                            "stresses": "1"},
                "triumph’st": {"syllables": ["tri", "umph’st"],
                               "stresses": "10"},
                "say’st": {"syllables": ["say’st"],
                           "stresses": "1"},
                "find’st": {"syllables": ["find’st"],
                            "stresses": "1"},
                "yield’st": {"syllables": ["yield’st"],
                             "stresses": "1"},
                "’tis": {"syllables": ["’tis"],
                         "stresses": "1"},
                "purpled": {"syllables": ["pur", "pled"],
                            "stresses": "10"},
                "maidenhead": {"syllables": ["mai", "den", "head"],
                               "stresses": "101"},
                "orisons": {"syllables": ["o", "ri", "son"],
                            "stresses": "102"},
                "mockeries": {"syllables": ["mocke", "ries"],
                              "stresses": "10"},
                "pallor": {"syllables": ["pa", "llor"],
                           "stresses": "10"},
              }


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
