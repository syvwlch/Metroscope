"""The class that provides the representation for a line of verse."""

from metroscope import WordBuilder

CUSTOM_DICT = {
                "phidian": {"syllables": ["phi", "dian"],
                            "phones": "F IH1 D IY0 N"},
                "indolence": {"syllables": ["in", "do", "lence"],
                              "phones": "IH2 N D OW0 L EH1 N S"},
                "benumbed": {"syllables": ["be", "numbed"],
                             "phones": "B IY2 N AH1 M D"},
                "unhaunted": {"syllables": ["un", "haun", "ted"],
                              "phones": "AH0 N HH AO1 N T IH0 D"},
                "nothingness": {"syllables": ["no", "thing", "ness"],
                                "phones": "N AH1 TH IH0 NG N EH1 S",
                                "stresses": "101"},
                "embroidered": {"syllables": ["em", "broi", "dered"],
                                "phones": "IH0 M B R OY1 D ER0 D"},
                "besprinkled": {"syllables": ["be", "sprin", "kled"],
                                "phones": "B IY2 S P R IH1 NG K AH0 L D"},
                "o’er": {"syllables": ["o’er"],
                         "phones": "AO1 R"},
                "unmeek": {"syllables": ["un", "meek"],
                           "phones": "AH0 N M IY1 K"},
                "poesy": {"syllables": ["po", "e", "sy"],
                          "phones": "P OW1 AH0 Z AY1"},
                "forsooth": {"syllables": ["for", "sooth"],
                             "phones": "F AO2 R S UW1 TH"},
                "honeyed": {"syllables": ["ho", "neyed"],
                            "phones": "HH AH1 N IY0 D"},
                "casement": {"syllables": ["case", "ment"],
                             "phones": "K EY1 S M AH0 N T"},
                "leaved": {"syllables": ["leaved"],
                           "phones": "L IY1 V D"},
                "throstle": {"syllables": ["thro", "stle"],
                             "phones": "TH R AA1 S AH0 L"},
                "farewell": {"syllables": ["fare", "well"],
                             "phones": "F EH2 R W EH1 L"},
                "dieted": {"syllables": ["di", "e", "ted"],
                           "phones": "D AY1 AH0 T IH2 D"},
                "masque": {"syllables": ["masque"],
                           "phones": "M AE1 S K"},
                "fall’n": {"syllables": ["fall’n"],
                           "phones": "F AA1 L N"},
                "spright": {"syllables": ["spright"],
                            "phones": "S P R AY1 T"},
                "flowers": {"syllables": ["flowers"],
                            "phones": "F L AW1 ER Z"},
                "flower": {"syllables": ["flower"],
                           "phones": "F L AW1 ER"},
                "flowery": {"syllables": ["flowe", "ry"],
                            "phones": "F L AW1 ER IY0"},
                "deniest": {"syllables": ["de", "niest"],
                            "phones": "",
                            "stresses": "10"},
                "know’st": {"syllables": ["know’st"],
                            "phones": "",
                            "stresses": "1"},
                "triumph’st": {"syllables": ["tri", "umph’st"],
                               "phones": "",
                               "stresses": "10"},
                "say’st": {"syllables": ["say’st"],
                           "phones": "",
                           "stresses": "1"},
                "find’st": {"syllables": ["find’st"],
                            "phones": "",
                            "stresses": "1"},
                "yield’st": {"syllables": ["yield’st"],
                             "phones": "",
                             "stresses": "1"},
                "’tis": {"syllables": ["’tis"],
                         "phones": "",
                         "stresses": "1"},
                "purpled": {"syllables": ["pur", "pled"],
                            "phones": "",
                            "stresses": "10"},
                "maidenhead": {"syllables": ["mai", "den", "head"],
                               "phones": "",
                               "stresses": "101"},
                "orisons": {"syllables": ["o", "ri", "son"],
                            "phones": "",
                            "stresses": "102"},
                "mockeries": {"syllables": ["mocke", "ries"],
                              "phones": "",
                              "stresses": "10"},
                "pallor": {"syllables": ["pa", "llor"],
                           "phones": "",
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
            number_stresses = len(word.stress_list)
            word_meter = stress_pattern[0:number_stresses]
            stress_pattern = stress_pattern[number_stresses:]
            # use the stress pattern directly for the word stresses
            stressed_line += word.stressed_HTML(word_meter) + " "
        for stress in stress_pattern:
            stressed_line += MISSING
        return stressed_line
