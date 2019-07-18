"""Configure shared resources for entire test suite."""

import pytest


@pytest.fixture
def app():
    """Set up and tear down the test app."""
    from run import create_app, db

    app = create_app('testing')

    app.config['TESTING'] = True

    app_context = app.app_context()
    app_context.push()

    db.create_all()

    yield app

    db.session.remove()
    db.drop_all()
    app_context.pop()


@pytest.fixture
def client(app):
    """Set up and tear down a test client without sample poems in the db."""
    yield app.test_client()


@pytest.fixture
def runner(app):
    """Return a cli test fixture with app context."""
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def register(
        self,
        display_name='John',
        email='john@metro.scope',
        password='cat',
        follow_redirects=False,
    ):
        return self._client.post(
            '/auth/register',
            data={
                'display_name': display_name,
                'email': email,
                'password': password,
                'password2': password,
            },
            follow_redirects=follow_redirects,
        )

    def login(
        self,
        email='john@metro.scope',
        password='cat',
        follow_redirects=False,
        next=None,
    ):
        url = '/auth/login'
        if next is not None:
            url += f'?next={next}'
        return self._client.post(
            url,
            data={
                'email': email,
                'password': password,
            },
            follow_redirects=follow_redirects,
        )

    def logout(
        self,
        follow_redirects=False,
    ):
        return self._client.get(
            '/auth/logout',
            follow_redirects=follow_redirects,
        )


@pytest.fixture
def auth(client):
    return AuthActions(client)
