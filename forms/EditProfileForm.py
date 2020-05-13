from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    username = StringField('Username')

    email = StringField('email')
    about = StringField('about')

    password = PasswordField('Password')
    repeat_password = PasswordField('Repeat Password')

    submit = SubmitField('Submit', validators=[DataRequired()])
