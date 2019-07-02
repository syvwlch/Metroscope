"""Init script for the website."""

from flask import Flask


app = Flask(__name__)


import run.views
