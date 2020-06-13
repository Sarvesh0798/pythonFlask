from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class SearchCustomerForm(FlaskForm):
    cSsnid = IntegerField('Customer ssnId', validators=[DataRequired()])
    cCid = IntegerField('Customer Id', validators=[DataRequired()])
    search = SubmitField('Search')

    def validate_cSsnid(self, cSsnid):
        
        if not len(str(cSsnid.data)) == 9:
            raise ValidationError('please enter 9 number digit.')
    
    def validate_cCid(self, cCid):
        
        if not len(str(cCid.data)) == 9:
            raise ValidationError('please enter 9 number digit.')



class CreateCustomerForm(FlaskForm):
    ssnid = IntegerField('Customer SSN ID',
                           validators=[DataRequired(), NumberRange(min=9, max=9)])
    cid = IntegerField('Customer Id', validators=[DataRequired()])
    name = StringField('Customer Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    age = IntegerField('Age',
                        validators=[DataRequired(), Length(min=1, max=3)])  
    address = StringField('Address',
                        validators=[DataRequired(), Length(min=2, max=20)])
    state =SelectField('State',choices=['mumbai','mumbai'], validators=[DataRequired()])
    city =SelectField('City',choices=['mumbai','mumbai'], validators=[DataRequired()])
    submit = SubmitField('Submit')
    reset = SubmitField('Reset')
    

    def validate_ssnid(self, ssnid):
        user = User.query.filter_by(ssnid=ssnid.data).first()
        if user:
            raise ValidationError('That SSNid is taken. Please choose a different one.')

    def validate_address(self, address):
        user = User.query.filter_by(address=address.data).first()
        if user:
            raise ValidationError('That address is taken. Please choose a different one.')

class UpdateCustomerForm(FlaskForm):
    ssnid = IntegerField('Customer SSN ID', )
    cid = IntegerField('Customer ID', )
    oldname = StringField('Old Customer Name',)
    newname = StringField('New Customer Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    oldage = IntegerField('Old Age',) 
    newage = IntegerField('New Age',
                        validators=[DataRequired(), Length(min=1, max=3)]) 
    oldaddress = StringField('Old Address',)
    newaddress = StringField('NewAddress',
                        validators=[DataRequired(), Length(min=2, max=20)])

    update = SubmitField('Update')
    

    def validate_newname(self, newname):
        user = User.query.filter_by(name=newname.data).first()
        if user:
            raise ValidationError('That name is taken. Please choose a different one.')

    def validate_newaddress(self, newaddress):
        user = User.query.filter_by(address=newaddress.data).first()
        if user:
            raise ValidationError('That address is taken. Please choose a different one.')
    def validate_newage(self, newage):
        user = User.query.filter_by(age=newage.data).first()
        if user:
            raise ValidationError('That age is taken. Please choose a different one.')
    
