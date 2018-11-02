from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length,Email, EqualTo

class reg_form(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    password_comfirm = PasswordField('Comfirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
class logIn_form(FlaskForm):
    
    username = StringField('Username',validators=[DataRequired(),Length(min=2, max=20)])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('LogIn')    
    
class Updateform(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    submit = SubmitField('Update')    