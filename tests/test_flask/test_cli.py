"""Test the added flask CLI commands."""

from launch import make_shell_context, samples_command, add_admin_command


def test_make_shell_context(app):
    """Check the shell context processor adds the right objects."""
    context = make_shell_context()
    assert 'db' in context
    assert 'Meter' in context
    assert 'Poet' in context
    assert 'Poem' in context
    assert 'reset_db' in context


def test_samples(runner):
    """Check that the `samples` CLI command works."""
    # invoke the command directly
    result = runner.invoke(samples_command)
    assert result.exit_code == 0
    assert 'Adding meter ' in result.output
    assert 'Adding poet ' in result.output
    assert 'Adding poem ' in result.output


def test_add_admin(runner):
    """Check that the `add_admin` CLI command works."""
    # invoke the command directly
    result = runner.invoke(add_admin_command)
    assert result.exit_code == 0
    assert 'Adding role ' in result.output
    assert 'Adding user ' in result.output
