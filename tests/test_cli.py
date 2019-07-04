"""Test the added flask CLI commands."""

from run import db, make_shell_context
from run.models import Meter, Poet, Poem


def test_make_shell_context():
    """Check the shell context processor adds the right objects."""
    context = make_shell_context()
    assert context['db'] == db
    assert context['Meter'] == Meter
    assert context['Poet'] == Poet
    assert context['Poem'] == Poem
