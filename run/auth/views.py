"""Route definitions for the auth blueprint."""

from flask import render_template
from . import auth


@auth.route('/login')
def login():
    """Define the login route."""
    return render_template('auth/login.html')
