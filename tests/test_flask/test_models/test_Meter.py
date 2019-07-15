"""Test the Meter model."""

from run.models import Meter


def test_Meter_repr():
    """Test the __repr__ method."""
    assert repr(
        Meter(name='name', pattern='pattern')) == "<Meter 'name'>"


def test_Meter_insert_samples(app):
    """Test the insert_samples static method of Meter."""
    assert Meter.query.first() is None

    Meter.insert_samples()
    assert Meter.query.first() is not None

    meters = Meter.query.all()
    for meter in meters:
        # Check the name is a string and includes 'meter'
        assert 'meter' in meter.name
        pattern = meter.pattern
        for char in ['0', '1']:
            pattern = pattern.replace(char, '')
        # Check the pattern is a string and only has "0" and "1" characters.
        assert pattern == ''

    Meter.insert_samples()
    # Check the operation is idempotent
    assert meters == Meter.query.all()


def test_Meter_relationship_Poem(app):
    """Test the relationship between Meter and Poem."""
    from run.models import Poet, Poem
    Meter.insert_samples()
    Poet.insert_samples()
    Poem.insert_samples()

    for meter in Meter.query.all():
        for poem in meter.poems:
            assert isinstance(poem, Poem)
