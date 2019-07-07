"""Test the added flask CLI commands."""

from launch import make_shell_context, deploy_command


def test_make_shell_context(app):
    """Check the shell context processor adds the right objects."""
    context = make_shell_context()
    assert 'db' in context
    assert 'Meter' in context
    assert 'Poet' in context
    assert 'Poem' in context
    assert 'reset_db' in context


def test_deploy(runner):
    """Check that the deploy CLI command works."""
    # invoke the command directly
    result = runner.invoke(deploy_command)
    assert result.exit_code == 0
    assert 'INFO  [alembic.runtime.migration]' in result.output
    assert 'Adding meter ' in result.output
    assert 'Adding poet ' in result.output
    assert 'Adding poem ' in result.output

    # can't seem to invoke by name with runner.invoke(args=['deploy'])
    # because the cli command gets added after app creation
    # so I'd have to add it to the app fixture, which defeats the purpose.
