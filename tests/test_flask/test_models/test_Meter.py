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
    for meter in Meter.query.all():
        assert 'meter' in meter.name

        pattern = meter.pattern
        for char in ['0', '1']:
            pattern = pattern.replace(char, '')
        assert pattern == ''
