"""Test the Meter model."""

from run.models import Meter


def test_Meter_repr():
    """Test the __repr__ method."""
    assert repr(
        Meter(name='name', pattern='pattern')) == "<Meter 'name'>"
