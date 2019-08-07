"""Define the forms for the poetry blueprint."""

from ...models import Poet, Poem
from flask_wtf import FlaskForm
from wtforms import (
    SubmitField, StringField, HiddenField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, Regexp


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
