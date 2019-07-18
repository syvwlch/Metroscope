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

    poets = Poet.query.all()
    for poet in poets:
        assert isinstance(poet.name, str)

    Poet.insert_samples()
    # Check the operation is idempotent
    assert poets == Poet.query.all()


def test_Poet_relationship_Poem(app):
    """Test the relationship between Poet and Poem."""
    from run.models import Meter, Poem
    Meter.insert_samples()
    Poet.insert_samples()
    Poem.insert_samples()

    for poet in Poet.query.all():
        for poem in poet.poems:
            assert isinstance(poem, Poem)
