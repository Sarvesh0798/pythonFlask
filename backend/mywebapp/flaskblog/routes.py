import os
import secrets
from random import randint
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import  LoginForm,DepoWithdrawForm,AccountStatementForm,TransferForm,SearchAccountrForm, CreateCustomerForm, UpdateCustomerForm, SearchCustomerForm, AccountForm
from flaskblog.models import User, Customer, Accountoperation, Customerstatus,Account
from flask_login import login_user, current_user, logout_user, login_required


db.create_all()
user=User.query.filter_by(username='admin').first()
if user==None:
    hashed_password = bcrypt.generate_password_hash("ggbhai").decode('utf-8')
    user = User(username="admin", email="aa@gmail.com", password=hashed_password)
    db.session.add(user)
    db.session.commit()


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
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route("/createcustomer", methods=['GET', 'POST'])
@login_required
def createCustomer():
    
       
    form = CreateCustomerForm()
    if form.validate_on_submit():
        n = 9
        cid=''.join(["{}".format(randint(0, 9)) for num in range(0, n)])
        while Customer.query.filter_by(cid=cid).first():
            cid=''.join(["{}".format(randint(0, 9)) for num in range(0, n)])

        customer=Customer(ssnid=form.ssnid.data,name=form.name.data,age=form.age.data,address=form.address.data,state=form.state.data,city=form.city.data,cid=cid,status='Active') 
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
        if form.cSsnid.data =='':
            customer=Customer.query.filter_by(cid=form.cCid.data).first()
        else:
            customer=Customer.query.filter_by(ssnid=form.cSsnid.data).first()
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
    
    form = UpdateCustomerForm()
    if form.validate_on_submit():
        customer.name=form.newname.data
        customer.age=form.newage.data
        customer.address=form.newaddress.data
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

#---------------------------------------------------------------------------------------------------#


@app.route("/createaccount", methods=['GET', 'POST'])
def create_account():
    if current_user.is_authenticated:
        
        form = AccountForm()
        if form.validate_on_submit():
            
            flash("added",'success')
           
        print(form.errors)
        return render_template('account/create_account.html',legend='Create Account', title='Create Account', form=form)
    
    else:
        
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
 


@app.route("/searchaccount/<tag>", methods=['GET', 'POST'])
@login_required
def search_account(tag,post_id):
    form=SearchAccountrForm()
    if form.validate_on_submit():
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
    post = Post.query.get_or_404(post_id)
    form=AccountForm()
    form.aid.data=account.aid
    form.accounttype.data=account.accounttype
    print(form.errors)
    return render_template('account/delete_account.html',title='Delete accouunt',legend='Delete account',form=form)




@app.route("/account/<int:post_id>/delete", methods=['GET', 'POST'])
def removeAccount(post_id):
    
    flash('Your Account has been deleted!', 'success')
    return redirect(url_for('home'))

#----------------------------------------------------------------------------------------------#
   
@app.route("/searchaccount/<int:post_id>/deposit",methods=['POST','GET'])
@login_required
def deposit(post_id):
    post = Post.query.get_or_404(post_id)
    
    form = DepoWithdrawForm(acctype=1)
    if form.validate_on_submit():
        form.balance.data=1000
        flash('Amount desposited!', 'success')
        
    else:
        form.cid.data = account.ccid
        form.aid.data = account.aid
        #form.acctype.default='type1'
        form.balance.data=account.deposit
    return render_template('account/deposit_withdraw.html',label='Deposit Amount' ,title='Deposit',form=form)

    
@app.route("/searchaccount/<int:post_id>/withdraw",methods=['POST','GET'])
@login_required
def withdraw(post_id):
    post = Post.query.get_or_404(post_id)
    form = DepoWithdrawForm(acctype=2)
    if form.validate_on_submit():

        flash('Amount withdrawed!', 'success')
        print('withdraweddddd')
            
    else:
        #request.method == 'GET':
        form.cid.data = account.ccid
        form.aid.data = account.aid
        #form.acctype.data=2
        form.balance.data=account.deposit
        print(form.errors)
    return render_template('account/deposit_withdraw.html',label='Withdraw Amount' ,title='Withdraw',form=form)


@app.route("/transfer/<int:post_id>",methods=['POST','GET'])
@login_required
def transfer(post_id):
    
    form = TransferForm()
    if form.validate_on_submit():
        flash('Amount transfered!', 'success')
        print('transfered')

    form.cid.data=123456789
    form.srcBalbf.data=1000
    form.srcBalaf.data=3000
    form.trgBalbf.data=1000
    form.trgBalaf.data=500  
    print(form.errors)
    return render_template('account/transfer.html',label='Withdraw Amount',legend='Transfer amount' ,title='Withdraw',form=form)

@app.route("/statement/<int:post_id>",methods=['POST','GET'])
@login_required
def statement(post_id):
    
    form = AccountStatementForm()
    if form.validate_on_submit():
        flash('Amount transfered!', 'success')
        print('show table')

    form.aid.data=12345678
     
    print(form.errors)
    return render_template('account/accstatement.html',label='Withdraw Amount',legend='Account statement' ,title='Withdraw',form=form)

@app.route("/status/<tags>",methods=['POST','GET'])
@login_required
def status(tags):
 
    return render_template('customer/customer_accstatus.html',tag=tags,legend='Account statement' ,title='Withdraw')

    
    

