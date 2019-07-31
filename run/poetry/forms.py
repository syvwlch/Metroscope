"""Define the forms for the poetry blueprint."""

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, BooleanField, StringField


class PoemChangeMeterForm(FlaskForm):
    """Allow user to choose the meter to scan the poem."""
    pattern = SelectField('Switch to')
    submit = SubmitField('Refresh')


class PoemSetDefaultMeterForm(PoemChangeMeterForm):
    """Allow user to set the default meter for the poem."""
    set_as_default = BooleanField('Set as the default meter')


class MeterUpdateForm(FlaskForm):
    """Allow user to update an existing meter."""
    name = StringField('Name')
    pattern = StringField('Pattern')
    submit = SubmitField('Update')
