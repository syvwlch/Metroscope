"""Test the added flask CLI commands."""

from launch import make_shell_context, samples_command, insert_roles_command


def test_make_shell_context(app):
    """Check the shell context processor adds the right objects."""
    context = make_shell_context()
    assert 'db' in context
    assert 'Meter' in context
    assert 'Poet' in context
    assert 'Poem' in context
    assert 'Role' in context
    assert 'User' in context


def test_samples(runner):
    """Check that the `samples` CLI command works."""
    # invoke the command directly
    result = runner.invoke(samples_command)
    assert result.exit_code == 0
    assert 'Adding meter ' in result.output
    assert 'Adding poet ' in result.output
    assert 'Adding poem ' in result.output


def test_insert_roles(runner):
    """Check that the `insert_roles` CLI command works."""
    # invoke the command directly
    result = runner.invoke(insert_roles_command)
    assert result.exit_code == 0
    assert 'Creating role ' in result.output
    assert 'Resetting permissions for role ' in result.output
