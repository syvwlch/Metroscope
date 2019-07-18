"""Test the reset password process using flask's test_client()."""


from flask import url_for, get_flashed_messages
from flask_login import current_user


def test_200(client):
    """Check the password reset view should always return a 200."""
    response = client.get("/auth/reset")
    assert "200" in response.status
    assert b"Email" in response.data
    assert b"New Password" not in response.data
    assert b"Confirm Password" not in response.data


def test_password_reset_authenticated_user(client, auth):
    """Check that password reset redirects when user is authenticated."""
    with client:
        auth.register()
        auth.login(follow_redirects=True)
        response = client.get('/auth/reset')
        assert current_user.is_authenticated
        assert "302" in response.status
        assert url_for('main.home', _external=True) == response.location
        assert get_flashed_messages() == []


def get_token_from_reset_email(body):
    """Return the token from reset email body"""
    reset_url = url_for(
        'auth.password_reset',
        token='',
        _external=True,
    )
    for line in body.splitlines():
        if line.startswith(reset_url):
            return line.replace(reset_url, '')
    return None


def test_reset_password(client, auth):
    """Check the reset password request works."""
    from run import mail
    from run.models import User
    with client:
        auth.register(follow_redirects=True)

        with mail.record_messages() as outbox:
            response = client.post(
                '/auth/reset',
                data={
                    'email': 'john@metro.scope',
                    },
            )
            assert len(outbox) == 1
            assert outbox[0].subject == "[Metroscope] Reset Your Password"
            assert User.reset_password(
                get_token_from_reset_email(outbox[0].body),
                'cat',
            )
            assert not current_user.is_authenticated
            assert "302" in response.status
            assert url_for('auth.login', _external=True) == response.location
            assert get_flashed_messages() == ['An email with instructions \
to reset your password has been sent to you.']


def test_reset_password_bad_email(client, auth):
    """Check the reset password request fails with bad email."""
    from run import mail
    with client:
        auth.register(follow_redirects=True)

        with mail.record_messages() as outbox:
            response = client.post(
                '/auth/reset',
                data={
                    'email': 'not-john@metro.scope',
                    },
            )
            assert len(outbox) == 0
            assert not current_user.is_authenticated
            assert "302" in response.status
            assert url_for('auth.login', _external=True) == response.location
            assert get_flashed_messages() == ['An email with instructions \
to reset your password has been sent to you.']


def test_reset_password_no_email(client, auth):
    """Check the reset password request fails with no email."""
    from run import mail
    with client:
        auth.register(follow_redirects=True)

        with mail.record_messages() as outbox:
            response = client.post(
                '/auth/reset',
                data={
                    },
            )
            assert len(outbox) == 0
            assert not current_user.is_authenticated
            assert "200" in response.status
            assert b"This field is required." in response.data
            assert get_flashed_messages() == []


def test_reset_token(client, auth):
    """Check that with a valid token the password can be reset."""
    from run.models import User

    auth.register(follow_redirects=True)
    token = User.query.first().generate_reset_token()

    assert User.query.first().verify_password('cat')
    assert "200" in client.get('/auth/reset/' + token).status

    with client:
        response = client.post(
            '/auth/reset/' + token,
            data={
                'password': 'dog',
                'password2': 'dog',
            },
        )
        assert not current_user.is_authenticated
        assert "302" in response.status
        assert url_for('auth.login', _external=True) == response.location
        assert get_flashed_messages() == ['Your password has been updated.']
        assert User.query.first().verify_password('dog')


def test_reset_token_authenticated_user(client, auth):
    """Check that reset with token redirects when user is authenticated."""
    from run.models import User

    auth.register(follow_redirects=True)
    token = User.query.first().generate_reset_token()
    with client:
        auth.register()
        auth.login(follow_redirects=True)
        response = client.get('/auth/reset/' + token)
        assert current_user.is_authenticated
        assert "302" in response.status
        assert url_for('main.home', _external=True) == response.location
        assert get_flashed_messages() == []


def test_reset_bad_token(client, auth):
    """Check that with a bad token the password cannot be reset."""
    from run.models import User

    auth.register(follow_redirects=True)
    token = 'bad token'

    assert User.query.first().verify_password('cat')

    with client:
        response = client.post(
            '/auth/reset/' + token,
            data={
                'password': 'dog',
                'password2': 'dog',
            },
        )
        assert not current_user.is_authenticated
        assert "302" in response.status
        assert url_for('main.home', _external=True) == response.location
        assert get_flashed_messages() == []
        assert not User.query.first().verify_password('dog')
