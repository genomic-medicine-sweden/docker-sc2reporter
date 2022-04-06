from flask_wtf import FlaskForm  
from wtforms import StringField, PasswordField, BooleanField 
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):  
    """Login form"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

