"""Initialize the poetry blueprint."""

from flask import Blueprint

poetry = Blueprint('poetry', __name__)

from . import views
