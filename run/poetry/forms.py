"""Define the forms for the poetry blueprint."""

from ..models import Meter, Poet, Poem
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

    def validate_id(self, field):
        meter = Meter.query.get(field.data)
        if meter is None:
            raise ValidationError('This meter does not exist.')

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


class MeterDeleteForm(FlaskForm):
    """Allow user to delete an existing meter."""
    id = HiddenField()
    delete = SubmitField('Delete Meter')

    def validate_id(self, field):
        meter = Meter.query.get(field.data)
        if meter is None:
            raise ValidationError('This meter does not exist.')
        poems = Poem.query.filter_by(meter=meter).first()
        if poems is not None:
            raise ValidationError(
                f"'{meter.name}' is in used and cannot be deleted."
            )


class PoetUpdateForm(FlaskForm):
    """Allow user to update an existing poet."""
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
    submit = SubmitField('Update Poet')

    def validate_id(self, field):
        poet = Poet.query.get(field.data)
        if poet is None:
            raise ValidationError('This poet does not exist.')

    def validate_name(self, field):
        p = Poet.query.filter_by(name=field.data).first()
        if p:  # There is already a poet with this name
            if str(p.id) != self.id.data:  # and it is not the current poet
                raise ValidationError(
                    f"'{field.data}' already in use."
                )


class PoetAddForm(FlaskForm):
    """Allow user to add a new poet."""
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
    submit = SubmitField('Add Poet')

    def validate_name(self, field):
        p = Poet.query.filter_by(name=field.data).first()
        if p:  # There is already a poet with this name
            raise ValidationError(
                f"'{field.data}' already in use."
            )


class PoetDeleteForm(FlaskForm):
    """Allow user to delete an existing poet."""
    id = HiddenField()
    delete = SubmitField('Delete Poet')

    def validate_id(self, field):
        poet = Poet.query.get(field.data)
        if poet is None:
            raise ValidationError('This poet does not exist.')
        poems = Poem.query.filter_by(author=poet).first()
        if poems is not None:
            raise ValidationError(
                f"'{poet.name}' has poems and cannot be deleted."
            )
