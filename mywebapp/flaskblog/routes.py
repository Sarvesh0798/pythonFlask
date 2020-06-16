import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import  LoginForm,DepoWithdrawForm,AccountStatementForm,TransferForm,SearchAccountrForm, CreateCustomerForm, UpdateCustomerForm, SearchCustomerForm, AccountForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


db.create_all()
user=User.query.filter_by(username='admin').one()
if not user:
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



@app.route("/searchcustomer/<tag>", methods=['GET', 'POST'])
@login_required
def search_customer(tag):
    form=SearchCustomerForm()
    if form.validate_on_submit():
        
        flash('Customer found!', 'success')
        if tag =='update':
            return redirect(url_for('update_customer',post_id='1'))
        
        else:
             return redirect(url_for('delete_customer',post_id='1'))   
        
    return render_template('customer/update.html',title='search customer',form=form)


@app.route("/searchaccount/<tag>", methods=['GET', 'POST'])
@login_required
def search_account(tag):
    form=SearchAccountrForm()
    if form.validate_on_submit():
        flash('Account found!', 'success')
        if tag =='delete':
            return redirect(url_for('delete_account',post_id='1'))
        elif tag=='deposit':
             return redirect(url_for('deposit',post_id='1'))
        elif  tag=='withdraw':
            return redirect(url_for('withdraw',post_id='1'))
        elif tag=='transfer':
            return redirect(url_for('transfer',post_id='1'))
        elif tag=='statement':
            return redirect(url_for('statement',post_id='1'))
        else:
            flash('Url does not exist','danger')   
    else:  
        
        return render_template('account/search_account.html',title='search account',form=form)   
    


@app.route("/createcustomer/<int:post_id>/delete",)
@login_required
def delete_customer(post_id):
    post = Post.query.get_or_404(post_id)
    form=CreateCustomerForm()
    form.ssnid.data='123456789'
    form.cid.data='123456789'
    form.name.data='mr. shah'
    form.age.data='23'
    form.address.data='mumbai'
    return render_template('customer/delete_customer.html',title='Delete customer',legend='Delete Customer',form=form)

@app.route("/createaccount/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_account(post_id):
    post = Post.query.get_or_404(post_id)
    form=AccountForm()
    form.aid.data='123456789'
    form.acctype.data='savings'
    print(form.errors)
    return render_template('account/delete_account.html',title='Delete accouunt',legend='Delete account',form=form)


@app.route("/customer/<int:post_id>/delete", methods=['GET', 'POST'])
def removeCustomer(post_id):
    
    flash('Your customer has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/account/<int:post_id>/delete", methods=['GET', 'POST'])
def removeAccount(post_id):
    
    flash('Your Account has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/createcustomer", methods=['GET', 'POST'])
def createCustomer():
    if current_user.is_authenticated:
        
        form = CreateCustomerForm()
        if form.validate_on_submit():
            
            print("added")
        print(form.errors)
        return render_template('customer/create_customer.html',legend='Delete Customer', title='CreateCustomer', form=form)
        
    else:
        
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    
@app.route("/createcustomer/<int:post_id>/update",methods=['POST','GET'])
@login_required
def update_customer(post_id):
    post = Post.query.get_or_404(post_id)
    
    form = UpdateCustomerForm()
    if form.validate_on_submit():
        print('updated')
        flash('Your Customer has been updated!', 'success')
        
    elif request.method == 'GET':
        form.ssnid.data = '123456'
        form.cid.data = '120544'
        form.oldname.data='mr. shah'
        form.oldage.data="23"
        form.oldaddress.data='mumbai'
    print(form.errors)
    return render_template('customer/update_customer.html', title='Update Post',form=form)

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
    
@app.route("/searchaccount/<int:post_id>/deposit",methods=['POST','GET'])
@login_required
def deposit(post_id):
    post = Post.query.get_or_404(post_id)
    
    form = DepoWithdrawForm(acctype=1)
    if form.validate_on_submit():
        form.balance.data=3000
        flash('Amount desposited!', 'success')
        
    else:
        form.cid.data = 123456789
        form.aid.data = 120544
        #form.acctype.default='type1'
        form.balance.data=2300
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
        form.cid.data = 123456789
        form.aid.data = 120544
        #form.acctype.data=2
        form.balance.data=2300
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

    
    


