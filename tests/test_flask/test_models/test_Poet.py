"""Test the Poet model."""

from run.models import Poet


def test_Poet_repr():
    """Test the __repr__ method."""
    assert repr(
        Poet(name='name')
    ) == "<Poet 'name'>"


def test_Poet_insert_samples(app):
    """Test the insert_samples static method of Poet."""
    assert Poet.query.first() is None
    Poet.insert_samples()
    assert Poet.query.first() is not None
    for poet in Poet.query.all():
        assert isinstance(poet.name, str)
