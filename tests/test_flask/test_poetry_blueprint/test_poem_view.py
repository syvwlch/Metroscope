"""Test the poem view using flask's test_client()."""


def test_200(client_poems):
    """Check the poem should always return a 200."""
    response = client_poems.get('/poetry/poem')
    assert "200" in response.status
    assert b'Ode' in response.data
    assert b'Flea' in response.data


def test_poem_keyword(client_poems):
    """Check the poem the poem route with a keyword."""
    response = client_poems.get('/poetry/poem/Flea')
    assert b'Flea' in response.data
    assert "200" in response.status
    assert "404" in client_poems.get('/poetry/poem/foo').status
