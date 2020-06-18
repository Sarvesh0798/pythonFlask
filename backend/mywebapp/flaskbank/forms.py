from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField,SubmitField, BooleanField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange,Optional
from wtforms.fields.html5 import DateField 
from flaskbank.models import User, Customer, Account


class LoginForm(FlaskForm):
    #email = StringField('Email',validators=[DataRequired(), Email()])
    username=StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

#operation section

class DepoWithdrawForm(FlaskForm):
    cid = IntegerField('Customer Id', validators=[DataRequired()])
    aid = IntegerField('Account Id', validators=[DataRequired()])
    acctype =SelectField('Account Type',choices=[('1','current'),('2','savings')],validate_choice=False)
    deposit = IntegerField('Deosit Amount', validators=[DataRequired()])
    balance = IntegerField('Balance', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    def validate_deposit(self,deposit):
        if not deposit.data>0:
            raise ValidationError('Enter amount greater than 0')

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
#--------------------------------------------------------------------------------------------------------
#acount section

class AccountForm(FlaskForm):
    cid = IntegerField('Customer Id', validators=[DataRequired()])
    aid = IntegerField('Account Id')
    acctype =SelectField('Account Type',choices=[('1','current'),('2','savings')], validators=[DataRequired()])
    deposit = IntegerField('Deosit Amount', validators=[DataRequired()])
    submit = SubmitField('Submit')
    search = SubmitField('Search')

    
    def validate_cid(self,cid):
        customer = Customer.query.filter_by(cid=cid.data).first()
        if not customer:
            raise ValidationError('customer does not exist.')
    def validate_deposit(self,deposit):
        if not deposit.data>0:
            raise ValidationError('Enter amount greater than 0')


class SearchAccountrForm(FlaskForm):
    cid = IntegerField('Customer Id', validators=[Optional()])
    aid = IntegerField('Account Id', validators=[Optional()])
    search = SubmitField('Search')

    def validate_cid(self,cid):
        account=Account.query.filter_by(acid=cid)
        if not account:
            raise ValidationError('customer does not exist.')

class AccountStatementForm(FlaskForm):
    aid = IntegerField('Account ID', )
    atype= StringField('Account Type')
    lasttr =SelectField('Last N transcations',choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], validators=[DataRequired()])
    startdate=DateField('StartDate',format='%Y/%m/%d', validators=[DataRequired()])
    enddate=DateField('StartDate',format='%Y/%m/%d', validators=[DataRequired()])
    submit=SubmitField('submit')

#-----------------------------------------------------------------------------------------------------------
#customer section
class SearchCustomerForm(FlaskForm):
    cSsnid = IntegerField('Customer ssnId', validators=[Optional()])
    cCid = IntegerField('Customer Id', validators=[Optional()])
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

    
    def validate_ssnid(self, ssnid):
        customer = Customer.query.filter_by(ssnid=ssnid.data).first()
        if customer:
            raise ValidationError('That SSNid is taken. Please choose a different one.')

    def validate_address(self, address):
        customer = Customer.query.filter_by(address=address.data).first()
        if customer:
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
            raise ValidationError('That age is taken. Please choose a different one.')
    
