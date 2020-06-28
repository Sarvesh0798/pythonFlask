from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField,SubmitField, BooleanField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange,Optional
from wtforms.fields.html5 import DateField 
from hospital.models import User, Patient, Medicine, Diagonastic


class LoginForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

#-----------------------------------------------------------------------------------------------------------
#patient section
class SearchPatientForm(FlaskForm):
    pid = IntegerField('Patient Id', validators=[DataRequired()])
    
    search = SubmitField('Search')

    
    


class CreatePatientForm(FlaskForm):
    ssnid = IntegerField('Patient SSN ID',
                           validators=[DataRequired(),NumberRange(min=100000000,max=999999999)])
    pid = IntegerField('Patient ID', )
    name = StringField('Patient Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    age = IntegerField('Age',
                        validators=[DataRequired(), NumberRange(min=10, max=150)])  
    address = StringField('Address',
                        validators=[DataRequired(), Length(min=2, max=200)])
    state =SelectField('State',choices=[('1','mumbai'),('2','umbai')], validators=[DataRequired()])
    city =SelectField('City',choices=[('1','mumbai'),('2','umbai')], validators=[DataRequired()])
    bed =SelectField('City',choices=[('general','genral ward'),('semi','semi sharing'),('single','single room')], validators=[DataRequired()])
    submit = SubmitField('Submit')
    reset = SubmitField('Reset')

    
    def validate_ssnid(self, ssnid):
        patient = Patient.query.filter_by(ssnid=ssnid.data).first()
        if patient:
            raise ValidationError('That SSNid is taken. Please choose a different one.')

    def validate_address(self, address):
        patient = Patient.query.filter_by(address=address.data).first()
        if patient:
            raise ValidationError('That address is taken. Please choose a different one.')

class UpdatePatientForm(FlaskForm):
    ssnid = IntegerField('Patient SSN ID', )
    pid = IntegerField('Patient ID' )
    
    newname = StringField('New Patient Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    
    newage = IntegerField('New Age',
                        validators=[DataRequired(), NumberRange(min=10, max=150)]) 
    
    newaddress = StringField('NewAddress',
                        validators=[DataRequired(), Length(min=2, max=200)])
    state =SelectField('State',choices=[('1','mumbai'),('2','umbai')], validators=[DataRequired()])
    city =SelectField('City',choices=[('1','mumbai'),('2','umbai')], validators=[DataRequired()])
    bed =SelectField('City',choices=[('general','genral ward'),('semi','semi sharing'),('single','single room')], validators=[DataRequired()])
    

    update = SubmitField('Update')
    
class ProfilePatientForm(FlaskForm):
    ssnid = IntegerField('Patient SSN ID',
                           validators=[DataRequired(),NumberRange(min=100000000,max=999999999)])
    pid = IntegerField('Patient ID', )
    name = StringField('Patient Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    age = IntegerField('Age',
                        validators=[DataRequired(), NumberRange(min=10, max=150)])  
    address = StringField('Address',
                        validators=[DataRequired(), Length(min=2, max=200)])
    state =SelectField('State',choices=[('1','mumbai'),('2','umbai')], validators=[DataRequired()])
    city =SelectField('City',choices=[('1','mumbai'),('2','umbai')], validators=[DataRequired()])
    bed =SelectField('City',choices=[('general','genral ward'),('semi','semi sharing'),('single','single room')], validators=[DataRequired()])
    doj=StringField('Date of  admission',)
    dodc=StringField('Date of discharge',)

class MedicineForm(FlaskForm):
    searchMed = StringField('Search Medicine',validators=[Optional()])
    quantity = IntegerField('Quantity',validators=[Optional(), NumberRange(min=1, max=200)] )
    searchbtn = SubmitField('Search')
    addMed = SubmitField('Add medicine')
    
