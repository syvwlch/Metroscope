"""Initialize the analyze blueprint."""

from flask import Blueprint

analyze = Blueprint('analyze', __name__)

from . import views
