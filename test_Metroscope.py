"""
Unit test the Metroscope package.

Work in progress, coverage not complete.
"""

import unittest
from Metroscope import WordBuilder, LineBuilder


class Test_WordBuilder(unittest.TestCase):
    """
    Test the WordBuilder class.

    Using TDD so coverage needs to be complete.
    """

    def test_init(self):
        """Should initialize from the original word."""
        WORDS = (
                 "automatic",
                 "serene",
                 )
        for word in WORDS:
            with self.subTest('Original word: ' + word):
                self.assertEqual(WordBuilder(word).word,
                                 word)

    def test_str_magic_method(self):
        """Should return the original word."""
        WORDS = ("One",
                 "morn",
                 "belovèd",
                 "pass’d",
                 )
        for word in WORDS:
            with self.subTest('Original word: ' + word):
                self.assertEqual(str(WordBuilder(word)),
                                 word)

    def test_repr_magic_method(self):
        """Should evaluate to itself."""
        WORDS = ("One",
                 "morn",
                 "belovèd",
                 "pass’d",
                 )
        for word in WORDS:
            with self.subTest('Original word: ' + word):
                self.assertEqual(repr(WordBuilder(word)),
                                 "WordBuilder('" + word + "')")

    def test__is_in_custom_dict(self):
        """Should return True if the word is in the provided custom_dict."""
        CUSTOM_DICT = {"indolence": "200"}
        WORDS = {
                 "indolence": True,
                 "batman": False,
                 }
        for word, bool in WORDS.items():
            with self.subTest('Word is in custom_dict: ' + str(bool)):
                wb = WordBuilder(word, custom_dict=CUSTOM_DICT)
                self.assertEqual(wb._is_in_custom_dict, bool)

    def test_syllables(self):
        """Should set the syllables from the original word."""
        WORDS = {
                 "automatic": ['au', 'to', 'ma', 'tic'],
                 "serene": ['se', 're', 'ne'],
                 }
        for word, syllables in WORDS.items():
            with self.subTest('Original word: ' + word):
                self.assertEqual(WordBuilder(word).syllables,
                                 syllables)

    def test_stresses(self):
        """Should set the stresses from the original word."""
        WORDS = {
                 "automatic": ['2', '0', '1', '0'],
                 "serene": ['0', '1'],
                 }
        for word, stresses in WORDS.items():
            with self.subTest('Original word: ' + word):
                self.assertEqual(WordBuilder(word).stresses,
                                 stresses)

    def test_custom_dict(self):
        """Should retrieve stresses from custom dict if provided."""
        WORDS = {
                "phidian": "20",
                "indolence": "200",
                 }
        for word, stresses in WORDS.items():
            with self.subTest('Original word: ' + word):
                self.assertNotEqual(WordBuilder(word).stresses,
                                    list(stresses))
                self.assertEqual(WordBuilder(word, custom_dict=WORDS).stresses,
                                 list(stresses))

    def test_stressed_syllables(self):
        """Should be a list of the original word's syllables with stress."""
        WORDS = {
                 "automatic":
                 [['au', '2'], ['to', '0'], ['ma', '1'], ['tic', '0']],
                 "serene": [['se', '0'], ['rene', '1']],
                 }
        for word, stressed_syllables in WORDS.items():
            with self.subTest('Original word: ' + word):
                self.assertEqual(WordBuilder(word).stressed_syllables,
                                 stressed_syllables)

    def test_word_already_clean(self):
        """Should return an already clean word unchanged."""
        WORDS = ("automatic",
                 "serene",
                 )
        for word in WORDS:
            with self.subTest('Tried to clean: ' + word):
                self.assertEqual(WordBuilder(word).clean_word,
                                 word)

    def test_word_has_grave_over_e(self):
        """Should change an 'è' to an 'e'."""
        WORDS = {
                 "belovèd": "beloved",
                 "bowèd": "bowed",
                 "joinèd": "joined",
                 }
        for word, cleaned_word in WORDS.items():
            with self.subTest('Tried to clean: ' + word):
                self.assertEqual(WordBuilder(word).clean_word,
                                 cleaned_word)

    def test_word_has_elision(self):
        """Should replace ’d with ed."""
        WORDS = {
                 "stepp’d": "stepped",
                 "pass’d": "passed",
                 }
        for word, cleaned_word in WORDS.items():
            with self.subTest('Tried to clean: ' + word):
                self.assertEqual(WordBuilder(word).clean_word,
                                 cleaned_word)

    def test_word_has_possessive(self):
        """Should strip final ’s without touching longer strings."""
        WORDS = {
                 "pleasure’s": "pleasure",
                 "man’s": "man",
                 "know’st": "know’st",
                 }
        for word, cleaned_word in WORDS.items():
            with self.subTest('Tried to clean: ' + word):
                self.assertEqual(WordBuilder(word).clean_word,
                                 cleaned_word)

    def test_word_has_uppercase(self):
        """Should force lowercase."""
        WORDS = {
                 "Phidian": "phidian",
                 "Shadows": "shadows",
                 "One": "one",
                 }
        for word, cleaned_word in WORDS.items():
            with self.subTest('Tried to clean: ' + word):
                self.assertEqual(WordBuilder(word).clean_word,
                                 cleaned_word)

    def test_word_has_punctuation(self):
        """Should strip punctuation."""
        WORDS = {
                 "seen,": "seen",
                 "faced;": "faced",
                 ".,;:!?—'\"": "",
                 }
        for word, cleaned_word in WORDS.items():
            with self.subTest('Tried to clean: ' + word):
                self.assertEqual(WordBuilder(word).clean_word,
                                 cleaned_word)

    def test_tag_string(self):
        """Should wrap a string with an HTML tag and optional style attr."""
        wb = WordBuilder("Test")
        with self.subTest('Without a style'):
            self.assertEqual(wb.tag_string("copy", "span"),
                             "<span>copy</span>")
        with self.subTest('With a style'):
            self.assertEqual(wb.tag_string("text", "strong", "color:red"),
                             "<strong style='color:red'>text</strong>")

    def test__matched_syllables(self):
        """Should give a list of list with the word's fit to meter."""
        WORDS = {
                 "automatic":
                 [['au', False, False],
                  ['to', True, False],
                  ['ma', False, True],
                  ['tic', None, False]],
                 "Shadows":
                 [['Sha', False, True],
                  ['dows', True, True]],
                 "One":
                 [['One', False, True]],
                 }
        for word, matches in WORDS.items():
            with self.subTest('Original word: ' + word):
                METER = [0, 1, 0]
                self.assertEqual(WordBuilder(word)._matched_syllables(METER),
                                 matches)

    def test_stressed_HTML(self):
        """Should give an HTML representation of the word's fit to meter."""
        WORDS = {
                 "automatic":
                 "<span>\
<span style='color:red'>au</span>\
<strong style='color:red'>to</strong>\
<span style='color:black'>ma</span>\
<small style='color:red'>tic</small>\
</span>",
                 "Shadows":
                 "<span>\
<span style='color:black'>Sha</span>\
<strong style='color:black'>dows</strong>\
</span>",
                 "One":
                 "<span>\
<span style='color:black'>One</span>\
</span>",
                 }
        for word, HTML in WORDS.items():
            with self.subTest('Original word: ' + word):
                METER = [0, 1, 0]
                self.assertEqual(WordBuilder(word).stressed_HTML(METER),
                                 HTML)


class Test_LineBuilder(unittest.TestCase):
    """
    Test the LineBuilder class.

    Using TDD so coverage needs to be complete.
    """

    def test_init(self):
        """Should initialize from the original line."""
        LINES = (
                 "One morn before me were three figures seen,",
                 "And once more came they by:-alas! wherefore?",
                 )
        for line in LINES:
            with self.subTest('Original line: ' + line):
                self.assertEqual(LineBuilder(line).line,
                                 line)

    def test_str_magic_method(self):
        """Should return the original word."""
        LINES = (
                 "One morn before me were three figures seen,",
                 "And once more came they by:-alas! wherefore?",
                 )
        for line in LINES:
            with self.subTest('Original line: ' + line):
                self.assertEqual(str(LineBuilder(line)),
                                 line)

    def test_repr_magic_method(self):
        """Should evaluate to itself."""
        LINES = (
                 "One morn before me were three figures seen,",
                 "And once more came they by:-alas! wherefore?",
                 )
        for line in LINES:
            with self.subTest('Original line: ' + line):
                self.assertEqual(repr(LineBuilder(line)),
                                 "LineBuilder('" + line + "')")

    def test_clean_line(self):
        """Should replace hyphens and emlines with spaces."""
        LINES = {
                 "One morn before me were three figures seen,":
                 "One morn before me were three figures seen,",
                 "And once—more came they by:-alas! wherefore?":
                 "And once more came they by: alas! wherefore?",
                 }
        for line, clean_line in LINES.items():
            with self.subTest('Original line: ' + line):
                self.assertEqual(LineBuilder(line).clean_line(),
                                 clean_line)

    def test_word_list(self):
        """Should create a list of WordBuilder instances."""
        LINE = "Two Owls and a Hen,"
        for word in LineBuilder(LINE).word_list():
            with self.subTest('Original word: ' + str(word)):
                self.assertEqual(repr(word),
                                 "WordBuilder('" + str(word) + "')")

    def test_stressed_HTML(self):
        """Should give an HTML representation of the line's fit to meter."""
        LINES = {
                 "Two Owls and a Hen,":
                 "<span>\
<span style='color:black'>Two</span></span> \
<span><strong style='color:black'>Owls</strong></span> \
<span><span style='color:black'>and</span></span> \
<span><span style='color:black'>a</span></span> \
<span><strong style='color:black'>Hen,</strong>\
</span> ",
                 }
        for line, HTML in LINES.items():
            with self.subTest('Original line: ' + line):
                METER = [0, 1, 0, 0, 1]
                self.assertEqual(LineBuilder(line).stressed_HTML(METER),
                                 HTML)


if __name__ == '__main__':
    unittest.main()
