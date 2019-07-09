"""Test the Poet model."""

from run.models import Poet


def test_Poet_repr():
    """Test the __repr__ method."""
    assert repr(
        Poet(name='name')
    ) == "<Poet 'name'>"
