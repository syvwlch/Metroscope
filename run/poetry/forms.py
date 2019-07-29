"""Define the forms for the poetry blueprint."""

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, BooleanField


class ChangeMeterForm(FlaskForm):
    """Allow user to choose the meter to scan the poem."""
    pattern = SelectField('')
    scan = SubmitField('Scan')


class SetDefaultMeterForm(ChangeMeterForm):
    """Allow user to set the default meter for the poem."""
    set_as_default = BooleanField('Set as the default meter')
