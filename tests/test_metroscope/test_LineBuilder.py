"""Unit test the LineBuilder Class."""

from metroscope import LineBuilder


def test_init():
    """Should initialize from the original line."""
    LINES = (
             "One morn before me were three figures seen,",
             "And once more came they by:-alas! wherefore?",
             )
    for line in LINES:
        assert(LineBuilder(line).line == line)


def test_str_magic_method():
    """Should return the original word."""
    LINES = (
             "One morn before me were three figures seen,",
             "And once more came they by:-alas! wherefore?",
             )
    for line in LINES:
        assert(str(LineBuilder(line)) == line)


def test_repr_magic_method():
    """Should evaluate to itself."""
    LINES = (
             "One morn before me were three figures seen,",
             "And once more came they by:-alas! wherefore?",
             )
    for line in LINES:
        assert(repr(LineBuilder(line))
               == "LineBuilder('" + line + "')")


def test__clean_line():
    """Should replace hyphens and emlines with spaces."""
    LINES = {
             "One morn before me were three figures seen,":
             "One morn before me were three figures seen,",
             "And once—more came they by:-alas! wherefore?":
             "And once more came they by: alas! wherefore?",
             }
    for line, clean_line in LINES.items():
        assert(LineBuilder(line)._clean_line() == clean_line)


def test_words():
    """Should create a list of WordBuilder instances."""
    LINE = "Two Owls and a Hen,"
    for word in LineBuilder(LINE).words:
        assert(repr(word) == "WordBuilder('" + str(word) + "')")


def test_rhyming_part():
    """Should return the rhyming part of the last word of the line."""
    LINES = {
             "Two Owls and a Hen,": "EH N",
             "I knew to be my demon Poesy.": None
             }
    for line, rhyme in LINES.items():
        assert(LineBuilder(line).rhyming_part == rhyme)
