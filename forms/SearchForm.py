from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    offer_name = StringField('Offer name', validators=[DataRequired()])
    lonlat = StringField('lon;lat', validators=[DataRequired()])
    advanced_checkbox = BooleanField('advanced')
