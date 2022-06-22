
from os.path import exists

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField #PasswordField, BooleanField, 
from wtforms.validators import ValidationError, DataRequired, Optional, Length #Email, EqualTo,
from app.models import Institution

class IngestForm(FlaskForm):
    submit = SubmitField('Ingest Transactions')

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