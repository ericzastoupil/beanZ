from lib2to3.pgen2.token import OP
from os import listdir
from os.path import isfile, join, abspath, dirname, exists
from ast import Sub
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional, Length
from app.models import User, Institution
from collections import namedtuple

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=24, message='Cannot be more than 24 characters')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=32, message='Must be at least 8 and no more than 32 characters')])
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

class AddInstituteForm(FlaskForm):
    institution_name = StringField('Bank Name', validators=[DataRequired(), Length(max=32, message='Cannot be more than 32 characters')])
    desc = StringField("Description", validators=[Optional(), Length(max=160, message='Cannot be more than 160 characters')])
    submit = SubmitField("Add Financial Institution")

    def validate_institution_name(self, institution_name):
        institution = Institution.query.filter_by(institution_name=institution_name.data).first()
        if institution is not None:
            raise ValidationError("Financial institution already in use")

class AddAccountForm(FlaskForm):
    institution_name = StringField('Institution Name', validators=[DataRequired()])
    account_type = StringField('Account Type', validators=[DataRequired()])
    account_name = StringField('Account Name', validators=[DataRequired()])
    desc = StringField("Description", validators=[Optional(), Length(max=160, message='Cannot be more than 160 characters')])
    submit = SubmitField("Add Account")

'''
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
'''