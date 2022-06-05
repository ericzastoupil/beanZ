from os import listdir
from os.path import isfile, join, abspath, dirname, exists
from ast import Sub
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField ('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username already taken")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Email already in use")

class IngestForm(FlaskForm):
    submit = SubmitField('Ingest Transactions')
    
    #hardcoding is bad
    #ingestPath = join(abspath(dirname(__file__)), 'ingest')
    #files = [f for f in listdir(ingestPath) if isfile(join(ingestPath, f))]

    def validate_fileLocation(self, location):
        if not exists('lskdjfdslkfjdsf'):
            raise ValidationError('No file to ingest')

'''
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
'''