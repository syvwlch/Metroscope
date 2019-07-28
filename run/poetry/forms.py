"""Define the forms for the poetry blueprint."""

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class ChangeMeterForm(FlaskForm):
    """Define the poem form."""
    pattern = SelectField('')
    submit = SubmitField('Scan')
