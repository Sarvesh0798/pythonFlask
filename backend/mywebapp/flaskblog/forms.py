from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField,SubmitField, BooleanField, TextAreaField, IntegerField, SelectField
<<<<<<< HEAD
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange,Optional
from wtforms.fields.html5 import DateField 
from flaskblog.models import User, Customer
=======
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from wtforms.fields.html5 import DateField 
from flaskblog.models import User
>>>>>>> c5ebdc3467f09a485195f438e5351d2825a7342e


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AccountForm(FlaskForm):
    cid = IntegerField('Customer Id', validators=[DataRequired()])
    aid = IntegerField('Account Id')
    acctype =SelectField('Account Type',choices=[('1','current'),('2','savings')], validators=[DataRequired()])
    deposit = IntegerField('Deosit Amount', validators=[DataRequired()])
    submit = SubmitField('Submit')
    search = SubmitField('Search')

<<<<<<< HEAD
    
    def validate_cid(self,cid):
        customer = Customer.query.filter_by(cid=cid.data).first()
        if not customer:
            raise ValidationError('customer does not exist.')
    def validate_deposit(self,deposit):
        if not deposit.data>0:
            raise ValidationError('Enter amount greater than 0')
=======
    def validate_cid(self,cid):
        if not cid.data==123456789:
            raise ValidationError('customer does not exist.')
    def validate_deposit(self,deposit):
        if not deposit.data>0:
            raise ValidationError('customer does not exist.')
>>>>>>> c5ebdc3467f09a485195f438e5351d2825a7342e

class DepoWithdrawForm(FlaskForm):
    cid = IntegerField('Customer Id', validators=[DataRequired()])
    aid = IntegerField('Account Id', validators=[DataRequired()])
    acctype =SelectField('Account Type',choices=[('1','current'),('2','savings')],validate_choice=False)
    deposit = IntegerField('Deosit Amount', validators=[DataRequired()])
    balance = IntegerField('Balance', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    def validate_cid(self,cid):
        if not cid.data==123456789:
            raise ValidationError('customer does not exist.')
    def validate_deposit(self,deposit):
        if not deposit.data>0:
            raise ValidationError('customer does not exist.')

class TransferForm(FlaskForm):
    cid = IntegerField('Customer Id', validators=[DataRequired()])
    sourcetype =SelectField('Source Account Type',choices=[('1','current'),('2','savings')])
    targettype =SelectField('Target Account Type',choices=[('1','current'),('2','savings')])
    transferamt = IntegerField('Transfer Amount', validators=[DataRequired()])
    srcBalbf = IntegerField('Source Balance before')
    srcBalaf = IntegerField('Source Balance after')
    trgBalbf = IntegerField('Target Balance before')
    trgBalaf = IntegerField('Targer Balance after')

    transfer = SubmitField('Transfer')
    
   
    def validate_transferamt(self,transferamt):
        if not transferamt.data>0:
            raise ValidationError('customer does not exist.')

class SearchAccountrForm(FlaskForm):
    cid = IntegerField('Customer Id', validators=[DataRequired()])
    aid = IntegerField('Account Id', validators=[DataRequired()])
    search = SubmitField('Search')

    def validate_cid(self,cid):
        if not cid.data==123456789:
            raise ValidationError('customer does not exist.')



class SearchCustomerForm(FlaskForm):
<<<<<<< HEAD
    cSsnid = IntegerField('Customer ssnId', validators=[Optional()])
    cCid = IntegerField('Customer Id', validators=[Optional()])
=======
    cSsnid = IntegerField('Customer ssnId', validators=[DataRequired()])
    cCid = IntegerField('Customer Id', validators=[DataRequired()])
>>>>>>> c5ebdc3467f09a485195f438e5351d2825a7342e
    search = SubmitField('Search')

    def validate_cSsnid(self, cSsnid):
        
        if not len(str(cSsnid.data)) == 9:
            raise ValidationError('please enter 9 number digit.')
    
    def validate_cCid(self, cCid):
        
        if not len(str(cCid.data)) == 9:
            raise ValidationError('please enter 9 number digit.')



class CreateCustomerForm(FlaskForm):
    ssnid = IntegerField('Customer SSN ID',
                           validators=[DataRequired()])
    cid = IntegerField('Customer Id', )
    name = StringField('Customer Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    age = IntegerField('Age',
                        validators=[DataRequired(), NumberRange(min=10, max=150)])  
    address = StringField('Address',
                        validators=[DataRequired(), Length(min=2, max=200)])
    state =SelectField('State',choices=[('1','mumbai'),('2','umbai')], validators=[DataRequired()])
    city =SelectField('City',choices=[('1','mumbai'),('2','umbai')], validators=[DataRequired()])
    submit = SubmitField('Submit')
    reset = SubmitField('Reset')
<<<<<<< HEAD

    
    def validate_ssnid(self, ssnid):
        customer = Customer.query.filter_by(ssnid=ssnid.data).first()
        if customer:
            raise ValidationError('That SSNid is taken. Please choose a different one.')

    def validate_address(self, address):
        customer = Customer.query.filter_by(address=address.data).first()
        if customer:
=======
    

    def validate_ssnid(self, ssnid):
        user = User.query.filter_by(username=ssnid.data).first()
        if user:
            raise ValidationError('That SSNid is taken. Please choose a different one.')

    def validate_address(self, address):
        user = User.query.filter_by(username=address.data).first()
        if user:
>>>>>>> c5ebdc3467f09a485195f438e5351d2825a7342e
            raise ValidationError('That address is taken. Please choose a different one.')

class UpdateCustomerForm(FlaskForm):
    ssnid = IntegerField('Customer SSN ID', )
    cid = IntegerField('Customer ID', )
    oldname = StringField('Old Customer Name',)
    newname = StringField('New Customer Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    oldage = IntegerField('Old Age',) 
    newage = IntegerField('New Age',
                        validators=[DataRequired(), NumberRange(min=10, max=150)]) 
    oldaddress = StringField('Old Address',)
    newaddress = StringField('NewAddress',
                        validators=[DataRequired(), Length(min=2, max=200)])

    update = SubmitField('Update')
    

    def validate_newname(self, newname):
<<<<<<< HEAD
        customer = Customer.query.filter_by(name=newname.data).first()
        if customer:
            raise ValidationError('That name is taken. Please choose a different one.')

    def validate_newaddress(self, newaddress):
        customer = Customer.query.filter_by(address=newaddress.data).first()
        if customer:
            raise ValidationError('That address is taken. Please choose a different one.')
    def validate_newage(self, newage):
        customer = Customer.query.filter_by(age=newage.data).first()
        if customer:
=======
        user = User.query.filter_by(username=newname.data).first()
        if user:
            raise ValidationError('That name is taken. Please choose a different one.')

    def validate_newaddress(self, newaddress):
        user = User.query.filter_by(username=newaddress.data).first()
        if user:
            raise ValidationError('That address is taken. Please choose a different one.')
    def validate_newage(self, newage):
        user = User.query.filter_by(username=newage.data).first()
        if user:
>>>>>>> c5ebdc3467f09a485195f438e5351d2825a7342e
            raise ValidationError('That age is taken. Please choose a different one.')
    
class AccountStatementForm(FlaskForm):
    aid = IntegerField('Account ID', )
    lasttr =SelectField('Last N transcations',choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], validators=[DataRequired()])
    startdate=DateField('StartDate',format='%Y/%m/%d', validators=[DataRequired()])
    enddate=DateField('StartDate',format='%Y/%m/%d', validators=[DataRequired()])
<<<<<<< HEAD
    submit=SubmitField('submit')
=======
    submit=SubmitField('submit')
>>>>>>> c5ebdc3467f09a485195f438e5351d2825a7342e
