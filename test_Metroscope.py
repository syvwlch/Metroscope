"""
Unit test the Metroscope package.

Work in progress, coverage not complete.
"""

import unittest
from Metroscope import clean_word, WordBuilder


class Test_WordBuilder(unittest.TestCase):
    """
    Test the WordBuilder class.

    Using TDD so coverage should be complete.
    """

    def test_syllables(self):
        """Should be a list of the original word's syllables."""
        WORDS = (
                 ("automatic",
                  [['au', '2'], ['to', '0'], ['ma', '1'], ['tic', '0']]),
                 ("serene",
                  [['se', '0'], ['rene', '1']]),
                 )
        for word, syllables in WORDS:
            with self.subTest('Original word: ' + word):
                actual_str = WordBuilder(word).syllables
                expected_str = syllables
                self.assertEqual(actual_str, expected_str)

    def test_str_magic_method(self):
        """Should return the original word."""
        WORDS = ("One",
                 "morn",
                 "belovèd",
                 "pass’d",
                 )
        for word in WORDS:
            with self.subTest('Original word: ' + word):
                actual_str = str(WordBuilder(word))
                expected_str = word
                self.assertEqual(actual_str, expected_str)

    def test_repr_magic_method(self):
        """Should evaluate to itself."""
        WORDS = ("One",
                 "morn",
                 "belovèd",
                 "pass’d",
                 )
        for word in WORDS:
            with self.subTest('Original word: ' + word):
                actual_str = repr(WordBuilder(word))
                expected_str = "WordBuilder('" + word + "')"
                self.assertEqual(actual_str, expected_str)


class Test_clean_word(unittest.TestCase):
    """
    Test the clean_word function.

    Coverage complete.
    """

    def test_word_already_clean(self):
        """Should return an already clean word unchanged."""
        WORDS = ("morn",
                 "three",
                 "figures",
                 )
        for word in WORDS:
            with self.subTest('Tried to clean: ' + word):
                self.assertEqual(word, clean_word(word))

    def test_word_has_grave_over_e(self):
        """Should change an 'è' to an 'e'."""
        WORDS = (("belovèd", "beloved"),
                 ("bowèd", "bowed"),
                 ("joinèd", "joined"),
                 )
        for word, cleaned_word in WORDS:
            with self.subTest('Tried to clean: ' + word):
                self.assertEqual(cleaned_word, clean_word(word))

    def test_word_has_elision(self):
        """Should replace ’d with ed."""
        WORDS = (("stepp’d", "stepped"),
                 ("pass’d", "passed"),
                 )
        for word, cleaned_word in WORDS:
            with self.subTest('Tried to clean: ' + word):
                self.assertEqual(cleaned_word, clean_word(word))

    def test_word_has_possessive(self):
        """Should strip ’s in a word."""
        WORDS = (("pleasure’s", "pleasure"),
                 ("man’s", "man"),
                 ("heart’s", "heart"),
                 )
        for word, cleaned_word in WORDS:
            with self.subTest('Tried to clean: ' + word):
                self.assertEqual(cleaned_word, clean_word(word))

    def test_word_has_uppercase(self):
        """Should force lowercase."""
        WORDS = (("Phidian", "phidian"),
                 ("Shadows", "shadows"),
                 ("One", "one"),
                 )
        for word, cleaned_word in WORDS:
            with self.subTest('Tried to clean: ' + word):
                self.assertEqual(cleaned_word, clean_word(word))

    def test_word_has_punctuation(self):
        """Should strip punctuation."""
        WORDS = (("seen,", "seen"),
                 ("faced;", "faced"),
                 (".,;:!?—", ""),
                 )
        for word, cleaned_word in WORDS:
            with self.subTest('Tried to clean: ' + word):
                self.assertEqual(cleaned_word, clean_word(word))


if __name__ == '__main__':
    unittest.main()
