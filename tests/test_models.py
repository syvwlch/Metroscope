"""Test the database models."""

from run.models import Meter, Poet, Poem


def test_Meter_repr():
    """Test the __repr__ method."""
    assert repr(
        Meter(name='name', pattern='pattern')) == "<Meter 'name'>"


def test_Poet_repr():
    """Test the __repr__ method."""
    assert repr(
        Poet(name='name')
    ) == "<Poet 'name'>"


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
