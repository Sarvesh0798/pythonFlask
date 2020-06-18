import os
import secrets
from random import randint
from PIL import Image
from datetime import datetime,date
import pytz
from flask import render_template, url_for, flash, redirect, request, abort
from flaskbank import app, db, bcrypt
from flaskbank.forms import  LoginForm,DepoWithdrawForm,AccountStatementForm,TransferForm,SearchAccountrForm, CreateCustomerForm, UpdateCustomerForm, SearchCustomerForm, AccountForm
from flaskbank.models import User, Customer, Accountoperation,Account
from flask_login import login_user, current_user, logout_user, login_required

'''db.drop_all()          #to rebuild entire db with new changes in DB
db.create_all()
user=User.query.filter_by(username='aExecutive').first()
user=User.query.filter_by(username='Teller').first()
if user==None:
    hashed_password = bcrypt.generate_password_hash("executive").decode('utf-8')
    user = User(username="aExecutive", password=hashed_password)
    db.session.add(user)
    hashed_password = bcrypt.generate_password_hash("cashier").decode('utf-8')
    user = User(username="Teller", password=hashed_password)
    db.session.add(user)
    db.session.commit()'''


@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/contact")
def contact():
    return render_template('contact.html', title='Contact')

@app.route("/",methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

#customer section

@app.route("/createcustomer", methods=['GET', 'POST'])
@login_required
def createCustomer():
    
       
    form = CreateCustomerForm()
    if form.validate_on_submit():
        tz = pytz.timezone("Asia/Kolkata")
        dateTime = tz.localize(datetime.now(), is_dst=None)
        n = 9
        cid=''.join(["{}".format(randint(0, 9)) for num in range(0, n)])
        while Customer.query.filter_by(cid=cid).first():
            cid=''.join(["{}".format(randint(0, 9)) for num in range(0, n)])

        customer=Customer(last_updated=dateTime,ssnid=form.ssnid.data,name=form.name.data,age=form.age.data,address=form.address.data,state=form.state.data,city=form.city.data,cid=cid,status='Active') 
        db.session.add(customer)
        db.session.commit()
        print("added")
        flash("Customer Created Succesfully",'success')


    print(form.errors)
    return render_template('customer/create_customer.html',legend='Create Customer', title='CreateCustomer', form=form)
    
   
    


@app.route("/searchcustomer/<tag>", methods=['GET', 'POST'])
@login_required
def search_customer(tag):
    form=SearchCustomerForm()
    if form.validate_on_submit():
        if form.cSsnid.data ==None:
            customer=Customer.query.filter_by(cid=form.cCid.data).first()
            if customer==None:
                flash('Doesnt exist','danger')
                return redirect(url_for('home'))
        else:
            customer=Customer.query.filter_by(ssnid=form.cSsnid.data).first()
            if customer==None:
                flash('Doesnt exist','danger')
                return redirect(url_for('home'))
        flash('Customer found!', 'success')
        if tag =='update':
            return redirect(url_for('update_customer',post_id=customer.id))
        
        else:
             return redirect(url_for('delete_customer',post_id=customer.id))   
        
    return render_template('customer/update.html',title='search customer',form=form)

@app.route("/createcustomer/<int:post_id>/update",methods=['POST','GET'])
@login_required
def update_customer(post_id):
    customer = Customer.query.get_or_404(post_id)
    tz = pytz.timezone("Asia/Kolkata")
    form = UpdateCustomerForm()
    if form.validate_on_submit():
        dateTime = tz.localize(datetime.now(), is_dst=None)
        
        customer.name=form.newname.data
        customer.age=form.newage.data
        customer.address=form.newaddress.data
        customer.last_updated=dateTime
        db.session.commit()
        print('updated')
        flash('Your Customer has been updated!', 'success')
        
    elif request.method == 'GET':
        form.ssnid.data = customer.ssnid
        form.cid.data = customer.cid
        form.oldname.data=customer.name
        form.oldage.data=customer.age
        form.oldaddress.data=customer.address
    print(form.errors)
    return render_template('customer/update_customer.html', title='Update Post',form=form)



@app.route("/createcustomer/<int:post_id>/delete",methods=['GET', 'POST'])
@login_required
def delete_customer(post_id):
    customer = Customer.query.get_or_404(post_id)
    form=CreateCustomerForm()
    form.ssnid.data=customer.ssnid
    form.cid.data=customer.cid
    form.name.data=customer.name
    form.age.data=customer.age
    form.address.data=customer.address
    return render_template('customer/delete_customer.html',customer=customer ,title='Delete customer',legend='Delete Customer',form=form)

@app.route("/customer/<int:post_id>/delete", methods=['GET', 'POST'])
def removeCustomer(post_id):
    customer = Customer.query.get_or_404(post_id)
    db.session.delete(customer)
    db.session.commit()
    flash('Your customer has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/profile_customer/<int:post_id>", methods=['GET', 'POST'])
@login_required
def profile_customer(post_id):
    customer = Customer.query.filter_by(cid=post_id).first_or_404()
    form=CreateCustomerForm()
    form.name.data = customer.name
    form.age.data = customer.age
    form.cid.data = customer.cid
    form.ssnid.data = customer.ssnid
    form.state.data = customer.state
    form.city.data = customer.city
    form.address.data = customer.address
    return render_template('customer/profile_customer.html',post_id=post_id, legend='Customer Information',title='Profile',form=form)


#---------------------------------------------------------------------------------------------------#
#account section

@app.route("/createaccount", methods=['GET', 'POST'])
@login_required
def create_account():

    
    form = AccountForm()
    if form.validate_on_submit():
        caccount=Account.query.filter_by(acid=form.cid.data).filter_by(accounttype='1').first()
        saccount=Account.query.filter_by(acid=form.cid.data).filter_by(accounttype='2').first()
        if caccount==None:
            tz = pytz.timezone("Asia/Kolkata")
            dateTime = tz.localize(datetime.now(), is_dst=None)
            acc=Account(last_updated=dateTime,accounttype=form.acctype.data,balance=form.deposit.data,acid=form.cid.data,status='Active')
            db.session.add(acc)
            db.session.commit()
            flash("Account Created",'success')
        elif saccount==None:
            tz = pytz.timezone("Asia/Kolkata")
            dateTime = tz.localize(datetime.now(), is_dst=None)
            acc=Account(last_updated=dateTime,accounttype=form.acctype.data,balance=form.deposit.data,acid=form.cid.data,status='Active')
            db.session.add(acc)
            db.session.commit()
            flash("Account Created",'success')
        else:

            flash("Account Exist",'danger')
        
    print(form.errors)
    return render_template('account/create_account.html',legend='Create Account', title='Create Account', form=form)

 


@app.route("/searchaccount/<tag>", methods=['GET', 'POST'])
@login_required
def search_account(tag):
    form=SearchAccountrForm()
    if form.validate_on_submit():
        
        if form.cid.data==None:
            account=Account.query.filter_by(aid=form.aid.data).first()
            if account==None:
                flash('Doesnt exist','danger')
                return redirect(url_for('home'))
        else:
            account=Account.query.filter_by(acid=form.cid.data).first()
            if account==None:
                flash('Doesnt exist','danger')
                return redirect(url_for('home'))
        flash('Account found!', 'success')
        if tag =='delete':
            return redirect(url_for('delete_account',post_id=account.aid))
        elif tag=='deposit':
             return redirect(url_for('deposit',post_id=account.aid))
        elif  tag=='withdraw':
            return redirect(url_for('withdraw',post_id=account.aid))
        elif tag=='transfer':
            return redirect(url_for('transfer',post_id=account.aid))
        elif tag=='statement':
            return redirect(url_for('statement',post_id=account.aid))
        else:
            flash('Url does not exist','danger')   
    else:  
        
        return render_template('account/search_account.html',title='search account',form=form)   
    



@app.route("/createaccount/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_account(post_id):
    account = Account.query.get_or_404(post_id)
    form=AccountForm()
    form.aid.data=account.aid
    form.acctype.data=account.accounttype
    print(form.errors)
    return render_template('account/delete_account.html',account=account,title='Delete accouunt',legend='Delete account',form=form)




@app.route("/account/<int:post_id>/delete", methods=['GET', 'POST'])
def removeAccount(post_id):
    account = Account.query.get_or_404(post_id)
    db.session.delete(account)
    db.session.commit()
    flash('Your Account has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/profile_account/<int:post_id>", methods=['GET', 'POST'])
@login_required
def profile_account(post_id):
    account = Account.query.filter_by(aid=post_id).first_or_404()
    form=AccountForm()
    form.aid.data=account.aid
    form.acctype.data=account.accounttype
    form.cid.data=account.acid
    form.deposit.data=account.balance
    return render_template('account/profile_account.html',post_id=post_id, legend='Account Information',title='Profile',form=form)


#----------------------------------------------------------------------------------------------#
#operations   
@app.route("/searchaccount/<int:post_id>/deposit",methods=['POST','GET'])
@login_required
def deposit(post_id):
    account = Account.query.get_or_404(post_id)

    
    form = DepoWithdrawForm(acctype=account.accounttype)
    if form.validate_on_submit():
        a=datetime.now()
        ts=a.timestamp()
        _date=str(date.fromtimestamp(ts))

        account.balance=account.balance+form.deposit.data
        accoperation=Accountoperation(message="deposit",last_updated=_date,aaccounttype=account.accounttype,ccid=account.acid,aaid=account.aid,amount=form.deposit.data)
        db.session.add(accoperation)
        db.session.commit()
        flash('Amount desposited!', 'success')
        
    else:
        form.cid.data = account.acid
        form.aid.data = account.aid
        form.balance.data=account.balance
    return render_template('account/deposit_withdraw.html',label='Deposit Amount' ,title='Deposit',form=form)

    
@app.route("/searchaccount/<int:post_id>/withdraw",methods=['POST','GET'])
@login_required
def withdraw(post_id):
    account = Account.query.get_or_404(post_id)
    form = DepoWithdrawForm(acctype=account.accounttype)
    if form.validate_on_submit():
        a=datetime.now()
        ts=a.timestamp()
        _date=str(date.fromtimestamp(ts))
 
        account.balance=account.balance-form.deposit.data
        accoperation=Accountoperation(message="withdraw",last_updated=_date,aaccounttype=account.accounttype,ccid=account.acid,aaid=account.aid,amount=form.deposit.data)
        db.session.add(accoperation)
        db.session.commit()
        flash('Amount withdrawed!', 'success')
        
            
    else:
        
        form.cid.data = account.acid
        form.aid.data = account.aid
        
        form.balance.data=account.balance
        print(form.errors)
    return render_template('account/deposit_withdraw.html',label='Withdraw Amount' ,title='Withdraw',form=form)




@app.route("/transfer/<int:post_id>",methods=['POST','GET'])
@login_required
def transfer(post_id):
    account=Account.query.get_or_404(post_id)
    customer=Customer.query.filter_by(cid=account.acid).first()
    form = TransferForm()
    if form.validate_on_submit():
        if form.sourcetype.data=='1':
            a=datetime.now()
            ts=a.timestamp()
            _date=str(date.fromtimestamp(ts))


            saccount=Account.query.filter_by(acid=customer.cid).filter_by(accounttype='1').first()
            taccount=Account.query.filter_by(acid=customer.cid).filter_by(accounttype='2').first()
            saccount.balance=saccount.balance-form.transferamt.data
            taccount.balance=taccount.balance+form.transferamt.data

            accoperation=Accountoperation(message="transfer",last_updated=_date,aaccounttype=saccount.accounttype,ccid=saccount.acid,aaid=saccount.aid,amount=form.transferamt.data)
            db.session.add(accoperation)
            db.session.commit()
            
            form.srcBalbf.data=saccount.balance+form.transferamt.data
            form.srcBalaf.data=0 if form.transferamt.data==None else (saccount.balance)
            form.trgBalbf.data=taccount.balance-form.transferamt.data
            form.trgBalaf.data=0 if form.transferamt.data==None else (taccount.balance)
            print(account)
        elif form.sourcetype.data=='2':
            a=datetime.now()
            ts=a.timestamp()
            _date=str(date.fromtimestamp(ts))

            saccount=Account.query.filter_by(acid=customer.cid).filter_by(accounttype='2').first()
            taccount=Account.query.filter_by(acid=customer.cid).filter_by(accounttype='1').first()
            saccount.balance=saccount.balance-form.transferamt.data
            taccount.balance=taccount.balance+form.transferamt.data

            accoperation=Accountoperation(message="transfer",last_updated=_date,aaccounttype=saccount.accounttype,ccid=saccount.acid,aaid=saccount.aid,amount=form.transferamt.data)
            db.session.add(accoperation)
            db.session.commit()

            db.session.commit()
            form.srcBalbf.data=saccount.balance+form.transferamt.data
            form.srcBalaf.data=0 if form.transferamt.data==None else (saccount.balance)
            form.trgBalbf.data=taccount.balance-form.transferamt.data
            form.trgBalaf.data=0 if form.transferamt.data==None else (taccount.balance)
            print(account)  
        

        flash('Amount transfered!', 'success')
        print('transfered')
    
    form.cid.data=account.acid
    print(form.errors)
    

    return render_template('account/transfer.html',label='Withdraw Amount',legend='Transfer amount' ,title='Withdraw',form=form)

@app.route("/statement/<int:post_id>",methods=['POST','GET'])
@login_required
def statement(post_id):
    account=Account.query.get_or_404(post_id)
    acop=Accountoperation.query.filter_by(ccid=account.acid)
    form = AccountStatementForm()
    if form.validate_on_submit():
        
        flash('Amount Statements!', 'success')
        print('show table')
        

    form.aid.data=account.aid
    if account.accounttype=='1':
        form.atype.data='Current'
    elif account.accounttype=='2':
        form.atype.data='Savings'    
      
    print(form.errors)
    return render_template('account/accstatement.html',label='Withdraw Amount',accs=acop,legend='Account statement' ,title='Withdraw',form=form)

@app.route("/status/<tags>",methods=['POST','GET'])
@login_required
def status(tags):
    if tags=='cust':
        data=Customer.query.all()
    elif tags=='acc':
        data=Account.query.all()    
    return render_template('customer/customer_accstatus.html',tag=tags,items=data,legend='Account statement' ,title='Withdraw')

    
    


