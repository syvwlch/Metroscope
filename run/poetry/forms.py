"""Define the forms for the poetry blueprint."""

from ..models import Meter
from flask_wtf import FlaskForm
from wtforms import (
    SelectField, SubmitField, BooleanField, StringField, HiddenField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, Regexp


class PoemChangeMeterForm(FlaskForm):
    """Allow user to choose the meter to scan the poem."""
    pattern = SelectField('Switch to')
    submit = SubmitField('Refresh')


class PoemSetDefaultMeterForm(PoemChangeMeterForm):
    """Allow user to set the default meter for the poem."""
    set_as_default = BooleanField('Set as the default meter')


class MeterUpdateForm(FlaskForm):
    """Allow user to update an existing meter."""
    id = HiddenField()
    name = StringField(
        label='Name',
        validators=[
            DataRequired(),
            Length(min=4, max=40),
            Regexp(
                '^[a-z,A-Z,  ]*$',
                message="Only letters and spaces, please."
            )
        ]
    )
    pattern = StringField(
        label='Pattern',
        validators=[
            DataRequired(),
            Length(min=1, max=24),
            Regexp('^[0-1]*$', message="Only 1's and 0's, please.")
        ]
    )
    submit = SubmitField('Update Meter')

    def validate_name(self, field):
        m = Meter.query.filter_by(name=field.data).first()
        if m:  # There is already a meter with this name
            if str(m.id) != self.id.data:  # and it is not the current meter
                raise ValidationError(
                    f"'{field.data}' already in use."
                )

    def validate_pattern(self, field):
        m = Meter.query.filter_by(pattern=field.data).first()
        if m:  # There is already a meter with this pattern
            if str(m.id) != self.id.data:  # and it is not the current meter
                raise ValidationError(
                    f"'{field.data}' already used by {m.name}."
                )


class MeterAddForm(FlaskForm):
    """Allow user to add a new meter."""
    name = StringField(
        label='Name',
        validators=[
            DataRequired(),
            Length(min=4, max=40),
            Regexp(
                '^[a-z,A-Z,  ]*$',
                message="Only letters and spaces, please."
            )
        ]
    )
    pattern = StringField(
        label='Pattern',
        validators=[
            DataRequired(),
            Length(min=1, max=24),
            Regexp('^[0-1]*$', message="Only 1's and 0's, please.")
        ]
    )
    submit = SubmitField('Add Meter')

    def validate_name(self, field):
        m = Meter.query.filter_by(name=field.data).first()
        if m:  # There is already a meter with this name
            raise ValidationError(
                f"'{field.data}' already in use."
            )

    def validate_pattern(self, field):
        m = Meter.query.filter_by(pattern=field.data).first()
        if m:  # There is already a meter with this pattern
            raise ValidationError(
                f"'{field.data}' already used by {m.name}."
            )
