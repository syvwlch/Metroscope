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


def test__word_list():
    """Should create a list of WordBuilder instances."""
    LINE = "Two Owls and a Hen,"
    for word in LineBuilder(LINE)._word_list:
        assert(repr(word) == "WordBuilder('" + str(word) + "')")


def test__rhyming_part():
    """Should return the rhyming part of the last word of the line."""
    LINES = {
             "Two Owls and a Hen,": "EH N",
             "I knew to be my demon Poesy.": None
             }
    for line, rhyme in LINES.items():
        assert(LineBuilder(line)._rhyming_part == rhyme)


def test_stressed_HTML():
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
             "Two Owls and a Poesy.":
             "<span>\
<span style='color:black'>Two</span></span> \
<span><strong style='color:black'>Owls</strong></span> \
<span><span style='color:black'>and</span></span> \
<span><span style='color:black'>a</span></span> \
<span><small style='color:red'>Poesy.</small></span> \
<span><small style='color:red'>_</small></span> ",
             }
    for line, HTML in LINES.items():
        METER = "01001"
        assert(LineBuilder(line).stressed_HTML(METER) == HTML)
