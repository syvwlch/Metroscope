"""Unit test the WordBuilder Class."""

from metroscope import WordBuilder


def test_init():
    """Should initialize from the original word."""
    WORDS = (
             "automatic",
             "serene",
             )
    for word in WORDS:
        assert(WordBuilder(word).word == word)


def test_str_magic_method():
    """Should return the original word."""
    WORDS = ("One",
             "morn",
             "belovèd",
             "pass’d",
             )
    for word in WORDS:
        assert(str(WordBuilder(word)) == word)


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


def test__is_in_custom_dict():
    """Should return True if the word is in the provided custom_dict."""
    CUSTOM_DICT = {"indolence": {"syllable": ["in", "do", "lence"],
                                 "stresses": "200"}}
    WORDS = {
             "indolence": True,
             "batman": False,
             }
    for word, bool in WORDS.items():
        wb = WordBuilder(word, custom_dict=CUSTOM_DICT)
        assert(wb._is_in_custom_dict == bool)


def test__phones():
    """Should set the phones from the original word."""
    WORDS = {
             "automatic": 'AO2 T AH0 M AE1 T IH0 K',
             "serene": 'S ER0 IY1 N',
             }
    for word, phones in WORDS.items():
        assert(WordBuilder(word)._phones == phones)


def test_syllables():
    """Should set the syllables from the original word."""
    WORDS = {
             "automatic": ['au', 'to', 'ma', 'tic'],
             "serene": ['se', 're', 'ne'],
             }
    for word, syllables in WORDS.items():
        assert(WordBuilder(word).syllables == syllables)


def test_stresses():
    """Should set the stresses from the original word."""
    WORDS = {
             "automatic": ['2', '0', '1', '0'],
             "serene": ['0', '1'],
             }
    for word, stresses in WORDS.items():
        assert(WordBuilder(word).stresses == stresses)


def test_custom_dict():
    """Should retrieve stresses from custom dict if provided."""
    CUSTOM_DICT = {
                   "phidian": {"syllable": ["phi", "dian"],
                               "stresses": "20"},
                   "indolence": {"syllable": ["in", "do", "lence"],
                                 "stresses": "200"}
             }
    for word, entry in CUSTOM_DICT.items():
        assert(WordBuilder(word).stresses
               == [])
        assert(WordBuilder(word, custom_dict=CUSTOM_DICT).stresses
               == list(entry["stresses"]))


def test__stressed_syllables():
    """Should be a list of the original word's syllables with stress."""
    WORDS = {
             "automatic":
             [['au', '2'], ['to', '0'], ['ma', '1'], ['tic', '0']],
             "serene": [['se', '0'], ['rene', '1']],
             }
    for word, stressed_syllables in WORDS.items():
        assert(WordBuilder(word)._stressed_syllables
               == stressed_syllables)


def test_word_already_clean():
    """Should return an already clean word unchanged."""
    WORDS = ("automatic",
             "serene",
             )
    for word in WORDS:
        assert(WordBuilder(word)._clean_word == word)


def test_word_has_grave_over_e():
    """Should change an 'è' to an 'e'."""
    WORDS = {
             "belovèd": "beloved",
             "bowèd": "bowed",
             "joinèd": "joined",
             }
    for word, cleaned_word in WORDS.items():
        assert(WordBuilder(word)._clean_word == cleaned_word)


def test_word_has_elision():
    """Should replace ’d with ed."""
    WORDS = {
             "stepp’d": "stepped",
             "pass’d": "passed",
             }
    for word, cleaned_word in WORDS.items():
        assert(WordBuilder(word)._clean_word == cleaned_word)


def test_word_has_possessive():
    """Should strip final ’s without touching longer strings."""
    WORDS = {
             "pleasure’s": "pleasure",
             "man’s": "man",
             "know’st": "know’st",
             }
    for word, cleaned_word in WORDS.items():
        assert(WordBuilder(word)._clean_word == cleaned_word)


def test_word_has_uppercase():
    """Should force lowercase."""
    WORDS = {
             "Phidian": "phidian",
             "Shadows": "shadows",
             "One": "one",
             }
    for word, cleaned_word in WORDS.items():
        assert(WordBuilder(word)._clean_word == cleaned_word)


def test_word_has_punctuation():
    """Should strip punctuation."""
    WORDS = {
             "seen,": "seen",
             "faced;": "faced",
             ".,;:!?—'\"": "",
             }
    for word, cleaned_word in WORDS.items():
        assert(WordBuilder(word)._clean_word == cleaned_word)


def test__tag_string():
    """Should wrap a string with an HTML tag and optional style attr."""
    wb = WordBuilder("Irrelevant")
    assert(wb._tag_string("Without a style passed", "span")
           == "<span>Without a style passed</span>")
    assert(wb._tag_string("With a style passed", "strong", "color:red")
           == "<strong style='color:red'>With a style passed</strong>")


def test__matched_syllables():
    """Should give a list of list with the word's fit to meter."""
    WORDS = {
             "automatic":
             [['au', False, True],
              ['to', True, False],
              ['ma', False, False],
              ['tic', None, False]],
             "Shadows":
             [['Sha', False, False],
              ['dows', True, True]],
             "One":
             [['One', False, True]],
             }
    for word, matches in WORDS.items():
        METER = [0, 1, 0]
        assert(WordBuilder(word)._matched_syllables(METER)
               == matches)


def test__rhyming_part():
    """Should return the rhyming part of the word."""
    LINES = {
             "Hen,": "EH1 N",
             "Poesy": None
             }
    for line, rhyme in LINES.items():
        assert(WordBuilder(line)._rhyming_part == rhyme)


def test_stressed_HTML():
    """Should give an HTML representation of the word's fit to meter."""
    WORDS = {
             "automatic":
             "<span>\
<span style='color:black'>au</span>\
<strong style='color:red'>to</strong>\
<span style='color:red'>ma</span>\
<small style='color:red'>tic</small>\
</span>",
             "Shadows":
             "<span>\
<span style='color:red'>Sha</span>\
<strong style='color:black'>dows</strong>\
</span>",
             "One":
             "<span>\
<span style='color:black'>One</span>\
</span>",
             }
    for word, HTML in WORDS.items():
        METER = [0, 1, 0]
        assert(WordBuilder(word).stressed_HTML(METER) == HTML)
