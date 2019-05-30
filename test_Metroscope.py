"""
Unit test the Metroscope package.

Work in progress, coverage not complete.
"""

import unittest
from Metroscope import clean_word


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
        """Should replace ’d and ’r with ed and er."""
        WORDS = (("stepp’d", "stepped"),
                 ("pass’d", "passed"),
                 ("flow’rs", "flowers"),
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
