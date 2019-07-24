"""Unit test the WordBuilder Class."""

import pytest
from metroscope import WordBuilder


def test_init():
    """Should initialize from the original word."""
    WORDS = (
             "Automatic",
             "serene",
             )
    for word in WORDS:
        wb = WordBuilder(word)
        assert wb.word == word
        assert wb._phones_index == 0


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


def test__phones():
    """Should set the phones from the original word."""
    CUSTOM_DICT = {
                   "phidian": {"syllables": ["phi", "dian"],
                               "phones": ["F IH1 D IY0 N"]},
                   }
    WORDS = {
             "Automatic": 'AO2 T AH0 M AE1 T IH0 K',
             "hen": 'HH EH1 N',
             "Phidian": "F IH1 D IY0 N",
             "Poesy.": None,
             }
    for word, phones in WORDS.items():
        wb = WordBuilder(word, custom_dict=CUSTOM_DICT)
        assert wb._phones == phones


def test_index():
    """Should set the index to use with the _phones list."""
    CUSTOM_DICT = {
                   "blarghe": {"syllables": ["blarghe"],
                               "phones": ["B L AE1 R G AE0",
                                          "B L AE1 R G E2"]},
                   }
    WORDS = {
             "blarghe": ["B L AE1 R G AE0",
                         "B L AE1 R G E2"]
             }
    for word, phones_list in WORDS.items():
        wb = WordBuilder(word, custom_dict=CUSTOM_DICT)
        wb.index = 0
        assert wb._phones_index == 0
        assert wb.index == 0
        assert wb._phones == phones_list[0]
        wb.index = 1
        assert wb._phones_index == 1
        assert wb.index == 1
        assert wb._phones == phones_list[1]
        with pytest.raises(IndexError):
            wb.index = 2


def test_syllables():
    """Should set the syllables from the original word."""
    CUSTOM_DICT = {
                   "phidian": {"syllables": ["phi", "dian"],
                               "phones": ["F IH1 D IY0 N"]},
                   }
    WORDS = {
             "Automatic": ['Au', 'to', 'ma', 'tic'],
             "serene": ['se', 're', 'ne'],
             "phidian": ["phi", "dian"],
             "Poesy.": ["Poe", "sy."],
             }
    for word, syllables in WORDS.items():
        wb = WordBuilder(word, custom_dict=CUSTOM_DICT)
        assert wb.syllables == syllables


def test_stress_list():
    """Should set the stresses from the original word."""
    CUSTOM_DICT = {
                   "phidian": {"syllables": ["phi", "dian"],
                               "phones": ["F IH1 D IY0 N"]},
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
        assert wb.stress_list == stresses


def test__stressed_syllables():
    """Should be a list of the original word's syllables with stress."""
    CUSTOM_DICT = {
                   "phidian": {"syllables": ["phi", "dian"],
                               "phones": ["F IH1 D IY0 N"]},
                   }
    WORDS = {
             "automatic":
             [['au', '2'], ['to', '0'], ['ma', '1'], ['tic', '0']],
             "serene": [['se', '0'], ['rene', '1']],
             "phidian": [['phi', '1'], ['dian', '0']],
             "Poesy.": None
             }
    for word, stressed_syllables in WORDS.items():
        wb = WordBuilder(word, custom_dict=CUSTOM_DICT)
        assert(wb._stressed_syllables
               == stressed_syllables)


def test_word_already_clean():
    """Should return an already clean word unchanged."""
    WORDS = ("automatic",
             "serene",
             )
    for word in WORDS:
        assert WordBuilder(word)._clean_word == word


def test_word_has_grave_over_e():
    """Should change an 'è' to an 'e'."""
    WORDS = {
             "belovèd": "beloved",
             "bowèd": "bowed",
             "joinèd": "joined",
             }
    for word, cleaned_word in WORDS.items():
        assert WordBuilder(word)._clean_word == cleaned_word


def test_word_has_elision():
    """Should replace ’d with ed."""
    WORDS = {
             "stepp’d": "stepped",
             "pass’d": "passed",
             }
    for word, cleaned_word in WORDS.items():
        assert WordBuilder(word)._clean_word == cleaned_word


def test_word_has_possessive():
    """Should strip final ’s without touching longer strings."""
    WORDS = {
             "pleasure’s": "pleasure",
             "man’s": "man",
             "know’st": "know’st",
             }
    for word, cleaned_word in WORDS.items():
        assert WordBuilder(word)._clean_word == cleaned_word


def test_word_has_uppercase():
    """Should force lowercase."""
    WORDS = {
             "Phidian": "phidian",
             "Shadows": "shadows",
             "One": "one",
             }
    for word, cleaned_word in WORDS.items():
        assert WordBuilder(word)._clean_word == cleaned_word


def test_word_has_punctuation():
    """Should strip punctuation."""
    WORDS = {
             "seen,": "seen",
             "faced;": "faced",
             ".,;:!?—'\"": "",
             }
    for word, cleaned_word in WORDS.items():
        assert WordBuilder(word)._clean_word == cleaned_word


def test__tag_string():
    """Should wrap a string with an HTML tag and optional class attr."""
    wb = WordBuilder("Irrelevant")
    assert(wb._tag_string("Without a style passed", "span")
           == "<span>Without a style passed</span>")
    assert(wb._tag_string("With a class passed", "strong", "stressed")
           == "<strong class='stressed'>With a class passed</strong>")


def test__matched_syllables():
    """Should give a list of list with the word's fit to meter."""
    CUSTOM_DICT = {
                   "phidian": {"syllables": ["phi", "dian"],
                               "phones": ["F IH1 D IY0 N"]},
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
        assert wb._matched_syllables() == matches


def test__rhyming_part():
    """Should return the rhyming part of the word."""
    CUSTOM_DICT = {
                   "phidian": {"syllables": ["phi", "dian"],
                               "phones": ["F IH1 D IY0 N"]},
                   }
    LINES = {
             "Hen,": "EH N",
             "Phidian": "IH D IY N",
             "Poesy": None
             }
    for line, rhyme in LINES.items():
        wb = WordBuilder(line, custom_dict=CUSTOM_DICT)
        assert wb._rhyming_part == rhyme


def test_stressed_HTML():
    """Should give an HTML representation of the word's fit to meter."""
    CUSTOM_DICT = {
        "phidian": {
            "syllables": ["phi", "dian"],
            "phones": ["F IH1 D IY0 N"]
        },
    }
    WORDS = {
        "automatic":
            "<span class='match unstressed'>au</span>\
<span class='mismatch stressed'>to</span>\
<span class='mismatch unstressed'>ma</span>\
<span class='mismatch missing'>tic</span>",
        "Shadows":
            "<span class='mismatch unstressed'>Sha</span>\
<span class='match stressed'>dows</span>",
        "One":
            "<span class='match unstressed'>One</span>",
        "Phidian":
            "<span class='mismatch unstressed'>Phi</span>\
<span class='mismatch stressed'>dian</span>",
        "Poesy.":
            "<span class='mismatch missing'>Poesy.</span>",
             }
    for word, HTML in WORDS.items():
        wb = WordBuilder(
            word=word,
            pattern="010",
            custom_dict=CUSTOM_DICT,
        )
        assert wb.stressed_HTML() == HTML
