"""Unit test the WordBuilder Class."""

from metroscope import WordBuilder
from metroscope.WordBuilder import clean_word


def test_init():
    """Should initialize from the original word."""
    WORDS = (
             "Automatic",
             "serene",
             )
    for word in WORDS:
        wb = WordBuilder(word)
        assert wb.word == word


def test_str_magic_method():
    """Should return the original word."""
    WORDS = ("One",
             "morn",
             "belovèd",
             "pass’d",
             )
    for word in WORDS:
        assert str(WordBuilder(word)) == word


def test_repr_magic_method():
    """Should evaluate to itself."""
    WORDS = ("One",
             "morn",
             "belovèd",
             "pass’d",
             )
    for word in WORDS:
        assert(repr(WordBuilder(word))
               == "WordBuilder('" + word + "')")


def test_phones():
    """Should set the phones from the original word."""
    CUSTOM_DICT = {
                   "phidian": {"syllables": ["phi", "dian"],
                               "phones": "F IH1 D IY0 N"},
                   }
    WORDS = {
             "Automatic": 'AO2 T AH0 M AE1 T IH0 K',
             "hen": 'HH EH1 N',
             "Phidian": "F IH1 D IY0 N",
             "Poesy.": '',
             }
    for word, phones in WORDS.items():
        wb = WordBuilder(word, custom_dict=CUSTOM_DICT)
        assert wb.phones == phones


def test__raw_syllables():
    """Should set the syllables from the original word."""
    CUSTOM_DICT = {
                   "phidian": {"syllables": ["phi", "dian"],
                               "phones": "F IH1 D IY0 N"},
                   }
    WORDS = {
             "Automatic": ['Au', 'to', 'ma', 'tic'],
             "serene": ['se', 're', 'ne'],
             "phidian": ["phi", "dian"],
             "Poesy.": ["Poe", "sy."],
             }
    for word, syllables in WORDS.items():
        wb = WordBuilder(word, custom_dict=CUSTOM_DICT)
        assert wb._raw_syllables == syllables


def test_stresses():
    """Should set the stresses from the original word."""
    CUSTOM_DICT = {
                   "phidian": {"syllables": ["phi", "dian"],
                               "phones": "F IH1 D IY0 N"},
                   }
    WORDS = {
             "Automatic": "2010",
             "serene": "01",
             "phidian": "10",
             "Poesy.": "",
             "bowèd": "12"
             }
    for word, stresses in WORDS.items():
        wb = WordBuilder(word, custom_dict=CUSTOM_DICT)
        assert wb.stresses == stresses


def test_word_already_clean():
    """Should return an already clean word unchanged."""
    WORDS = ("automatic",
             "serene",
             )
    for word in WORDS:
        assert clean_word(word) == word


def test_word_has_grave_over_e():
    """Should change an 'è' to an 'e'."""
    WORDS = {
             "belovèd": "beloved",
             "bowèd": "bowed",
             "joinèd": "joined",
             }
    for word, cleaned_word in WORDS.items():
        assert clean_word(word) == cleaned_word


def test_word_has_elision():
    """Should replace ’d with ed."""
    WORDS = {
             "stepp’d": "stepped",
             "pass’d": "passed",
             }
    for word, cleaned_word in WORDS.items():
        assert clean_word(word) == cleaned_word


def test_word_has_possessive():
    """Should strip final ’s without touching longer strings."""
    WORDS = {
             "pleasure’s": "pleasure",
             "man’s": "man",
             "know’st": "know’st",
             }
    for word, cleaned_word in WORDS.items():
        assert clean_word(word) == cleaned_word


def test_word_has_uppercase():
    """Should force lowercase."""
    WORDS = {
             "Phidian": "phidian",
             "Shadows": "shadows",
             "One": "one",
             }
    for word, cleaned_word in WORDS.items():
        assert clean_word(word) == cleaned_word


def test_word_has_punctuation():
    """Should strip punctuation."""
    WORDS = {
             "seen,": "seen",
             "faced;": "faced",
             ".,;:!?—'\"": "",
             }
    for word, cleaned_word in WORDS.items():
        assert clean_word(word) == cleaned_word


def test_syllables():
    """Should give a list of list with the word's fit to meter."""
    CUSTOM_DICT = {
                   "phidian": {"syllables": ["phi", "dian"],
                               "phones": "F IH1 D IY0 N"},
                   }
    from collections import namedtuple
    Syllable = namedtuple('Syllable', 'text stress match')
    WORDS = {
             "automatic":
             [Syllable(text='au', stress=False, match=True),
              Syllable(text='to', stress=True, match=False),
              Syllable(text='ma', stress=False, match=False),
              Syllable(text='tic', stress=None, match=False)],
             "Shadows":
             [Syllable(text='Sha', stress=False, match=False),
              Syllable(text='dows', stress=True, match=True)],
             "One":
             [Syllable(text='One', stress=False, match=True)],
             "Phidian":
             [Syllable(text='Phi', stress=False, match=False),
              Syllable(text='dian', stress=True, match=False)],
             "Poesy.":
             [Syllable(text='Poesy.', stress=None, match=False)],
             }
    for word, matches in WORDS.items():
        wb = WordBuilder(
            word=word,
            pattern="010",
            custom_dict=CUSTOM_DICT,
        )
        assert wb.syllables == matches


def test_rhyming_part():
    """Should return the rhyming part of the word."""
    CUSTOM_DICT = {
                   "phidian": {"syllables": ["phi", "dian"],
                               "phones": "F IH1 D IY0 N"},
                   }
    LINES = {
             "Hen,": "EH N",
             "Phidian": "IH D IY N",
             "Poesy": None
             }
    for line, rhyme in LINES.items():
        wb = WordBuilder(line, custom_dict=CUSTOM_DICT)
        assert wb.rhyming_part == rhyme
