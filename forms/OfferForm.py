from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired


class OfferForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description')

    lon = FloatField('lon', validators=[DataRequired()])
    lat = FloatField('lat', validators=[DataRequired()])
