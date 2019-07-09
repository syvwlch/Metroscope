"""Test the database models."""

import pytest
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


def test_Poem_ValueError(app):
    """Check that insert_samples() raises ValueError if meter/poet absent."""
    with pytest.raises(ValueError) as excinfo:
        Poem.insert_samples()
    assert "This poet does not exist." in str(excinfo.value)
    Poet.insert_samples()
    with pytest.raises(ValueError) as excinfo:
        Poem.insert_samples()
    assert "This meter pattern does not exist." in str(excinfo.value)
