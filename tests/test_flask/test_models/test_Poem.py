"""Test the Poem model."""

import pytest
from run.models import Meter, Poet, Poem


def test_Poem_repr():
    """Test the __repr__ method."""
    assert repr(
        Poem(
            title='title',
            keyword='keyword',
            raw_text='raw text',
            poet_id=1,
            meter_id=1,
        )
    ) == "<Poem 'title'>"


def test_Poem_ValueError(app):
    """Check that insert_samples() raises ValueError if meter/poet absent."""
    with pytest.raises(ValueError) as excinfo:
        Poem.insert_samples()
    assert "This poet does not exist." in str(excinfo.value)
    Poet.insert_samples()
    with pytest.raises(ValueError) as excinfo:
        Poem.insert_samples()
    assert "This meter pattern does not exist." in str(excinfo.value)


def test_Poem_insert_samples(app):
    """Test the insert_samples static method of Poem."""
    assert Poem.query.first() is None
    Meter.insert_samples()
    Poet.insert_samples()
    Poem.insert_samples()
    assert Poem.query.first() is not None
    for poem in Poem.query.all():
        assert isinstance(poem.title, str)
        assert isinstance(poem.keyword, str)
        assert isinstance(poem.raw_text, str)
        assert isinstance(poem.author, Poet)
        assert isinstance(poem.meter, Meter)
