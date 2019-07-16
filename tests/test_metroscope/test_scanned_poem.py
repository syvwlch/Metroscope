"""Unit test the scanned_poem module."""

from metroscope import rhyme_designator


def test_rhyme_designator():
    """Should return a short string designating an index."""

    assert rhyme_designator(0) == "A"
    assert rhyme_designator(26) == "A1"
    assert rhyme_designator(52) == "A2"
    assert rhyme_designator(1) == "B"
    assert rhyme_designator(27) == "B1"
    assert rhyme_designator(53) == "B2"
