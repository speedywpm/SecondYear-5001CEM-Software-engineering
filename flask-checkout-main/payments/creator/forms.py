from wtforms import (
    StringField,
    validators,
)

from ..forms import Form


class KeyRequestForm(Form):
    seller = StringField('Seller name', [validators.DataRequired(), validators.Length(min=2, max=64)])
