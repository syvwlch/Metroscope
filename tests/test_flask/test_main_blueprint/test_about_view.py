"""Test the '/about' view using flask's test_client()."""


def test_about_default(client, monkeypatch):
    """Check that the about page is loading the default content."""
    monkeypatch.delenv("ABOUT_FILE", raising=False)
    response = client.get('/about')
    assert "200" in response.status
    assert b'What is Metroscope about?' in response.data


def test_about_missing_file(client, monkeypatch):
    """Check that the about page fails to load content gracefully."""
    monkeypatch.setenv("ABOUT_FILE", 'NONEXISTENT.file')
    response = client.get('/about')
    assert "200" in response.status
    assert b'Failed to load' in response.data
