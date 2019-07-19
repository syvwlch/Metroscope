"""Test the poem view using flask's test_client()."""


def test_200(client_poems):
    """Check the poem should always return a 200."""
    response = client_poems.get('/analyze/poem/Flea')
    assert b'Flea' in response.data
    assert "200" in response.status
    assert "404" in client_poems.get('/poem/foo').status
