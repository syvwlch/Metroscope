"""
Test the views.

This only covers tests that aren't in the smoketest.
"""

from run import create_app, db


def test_about_default(monkeypatch):
    """Check that the about page is loading the default content."""
    monkeypatch.delenv("ABOUT_FILE", raising=False)
    app = create_app('testing')
    app.config['TESTING'] = True
    app_context = app.app_context()
    app_context.push()
    client = app.test_client()

    assert b'What is Metroscope about?' in client.get('/about').data

    db.session.remove()
    db.drop_all()
    app_context.pop()


def test_about_missing_file(monkeypatch):
    """Check that the about page fails to load content gracefully."""
    monkeypatch.setenv("ABOUT_FILE", 'NONEXISTENT.file')
    app = create_app('testing')
    app.config['TESTING'] = True
    app_context = app.app_context()
    app_context.push()
    client = app.test_client()

    assert b'Failed to load' in client.get('/about').data

    db.session.remove()
    db.drop_all()
    app_context.pop()
