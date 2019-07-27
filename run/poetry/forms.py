"""Define the forms for the poetry blueprint."""

from flask_wtf import FlaskForm
# from ..models import Meter
from wtforms import SelectField, SubmitField


class PoemForm(FlaskForm):
    """Define the poem form."""
    # meters = []
    # meters = [
    #     ('01001001', 'Anapestic Trimeter'),
    #     ('0101010101', 'Iambic Pentameter'),
    # ]
    # pattern = SelectField('Meter', choices=meters)

    pattern = SelectField('Meter')
    submit = SubmitField('Scan Poem')
