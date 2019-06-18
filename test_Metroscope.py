"""
Unit test the Metroscope package.

Work in progress, coverage not complete.
"""

import unittest
from Metroscope import WordBuilder


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

    def test_syllables(self):
        """Should set the syllables from the original word."""
        WORDS = (
                 ("automatic",
                  ['au', 'to', 'ma', 'tic']),
                 ("serene",
                  ['se', 're', 'ne']),
                 )
        for word, syllables in WORDS:
            with self.subTest('Original word: ' + word):
                self.assertEqual(WordBuilder(word).syllables,
                                 syllables)

    def test_stresses(self):
        """Should set the stresses from the original word."""
        WORDS = (
                 ("automatic",
                  ['2', '0', '1', '0']),
                 ("serene",
                  ['0', '1']),
                 )
        for word, stresses in WORDS:
            with self.subTest('Original word: ' + word):
                self.assertEqual(WordBuilder(word).stresses,
                                 stresses)

    def test_stressed_syllables(self):
        """Should be a list of the original word's syllables with stress."""
        WORDS = (
                 ("automatic",
                  [['au', '2'], ['to', '0'], ['ma', '1'], ['tic', '0']]),
                 ("serene",
                  [['se', '0'], ['rene', '1']]),
                 )
        for word, stressed_syllables in WORDS:
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
        WORDS = (("belovèd", "beloved"),
                 ("bowèd", "bowed"),
                 ("joinèd", "joined"),
                 )
        for word, cleaned_word in WORDS:
            with self.subTest('Tried to clean: ' + word):
                self.assertEqual(WordBuilder(word).clean_word,
                                 cleaned_word)

    def test_word_has_elision(self):
        """Should replace ’d with ed."""
        WORDS = (("stepp’d", "stepped"),
                 ("pass’d", "passed"),
                 )
        for word, cleaned_word in WORDS:
            with self.subTest('Tried to clean: ' + word):
                self.assertEqual(WordBuilder(word).clean_word,
                                 cleaned_word)

    def test_word_has_possessive(self):
        """Should strip final ’s without touching longer strings."""
        WORDS = (("pleasure’s", "pleasure"),
                 ("man’s", "man"),
                 ("know’st", "know’st"),
                 )
        for word, cleaned_word in WORDS:
            with self.subTest('Tried to clean: ' + word):
                self.assertEqual(WordBuilder(word).clean_word,
                                 cleaned_word)

    def test_word_has_uppercase(self):
        """Should force lowercase."""
        WORDS = (("Phidian", "phidian"),
                 ("Shadows", "shadows"),
                 ("One", "one"),
                 )
        for word, cleaned_word in WORDS:
            with self.subTest('Tried to clean: ' + word):
                self.assertEqual(WordBuilder(word).clean_word,
                                 cleaned_word)

    def test_word_has_punctuation(self):
        """Should strip punctuation."""
        WORDS = (("seen,", "seen"),
                 ("faced;", "faced"),
                 (".,;:!?—'\"", ""),
                 )
        for word, cleaned_word in WORDS:
            with self.subTest('Tried to clean: ' + word):
                self.assertEqual(WordBuilder(word).clean_word,
                                 cleaned_word)

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


if __name__ == '__main__':
    unittest.main()
