import os
import secrets
from random import randint
from PIL import Image
from datetime import datetime,date
import pytz
from flask import render_template, url_for, flash, redirect, request, abort
from hospital import app, db, bcrypt
from hospital.forms import  LoginForm,DepoWithdrawForm,AccountStatementForm,TransferForm,SearchAccountrForm, CreatePatientForm, UpdatePatientForm,ProfilePatientForm ,SearchPatientForm, AccountForm
from hospital.models import User, Patient, Medicine,Diagonastic
from flask_login import login_user, current_user, logout_user, login_required


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

#patient section

@app.route("/createpatient", methods=['GET', 'POST'])
@login_required
def createPatient():
    
       
    form = CreatePatientForm()
    if form.validate_on_submit():
        tz = pytz.timezone("Asia/Kolkata")
        dateTime = tz.localize(datetime.now(), is_dst=None)
        
        patient=Patient(doj=dateTime,ssnid=form.ssnid.data,name=form.name.data,age=form.age.data,bed=form.bed.data,address=form.address.data,state=form.state.data,city=form.city.data,status='Active') 
        db.session.add(patient)
        db.session.commit()
        print("added")
        flash("Patient Created Succesfully",'success')


    print(form.errors)
    return render_template('patient/create_patient.html',legend='Create Patient', title='CreatePatient', form=form)
    
   
    


@app.route("/searchpatient/<tag>", methods=['GET', 'POST'])
@login_required
def search_patient(tag):
    form=SearchPatientForm()
    if form.validate_on_submit():
        if form.pid.data ==None:
            flash('Doesnt exist','danger')
            return redirect(url_for('home'))
        else:
            patient=Patient.query.filter_by(id=form.pid.data).first()
            if patient==None:
                flash('Doesnt exist','danger')
                return redirect(url_for('home'))
        flash('Patient found!', 'success')
        if tag =='uddate':
            return redirect(url_for('update_patient',post_id=patient.id))
        elif tag=='profile':
            return redirect(url_for('profile_patient',post_id=patient.id))
        elif tag=='bill':
            return redirect(url_for('update_patient',post_id=patient.id))
        else:
             return redirect(url_for('delete_patient',post_id=patient.id))   
        
    return render_template('patient/search_patient.html',title='search patient',form=form)

@app.route("/createpatient/<int:post_id>/update",methods=['POST','GET'])
@login_required
def update_patient(post_id):
    patient = Patient.query.get_or_404(post_id)
    tz = pytz.timezone("Asia/Kolkata")
    form = UpdatePatientForm()
    if form.validate_on_submit():
        dateTime = tz.localize(datetime.now(), is_dst=None)
        
        patient.name=form.newname.data
        patient.age=form.newage.data
        patient.address=form.newaddress.data
        patient.city=form.city.data
        patient.bed=form.bed.data
        patient.state=form.state.data
        patient.last_updated=dateTime
        db.session.commit()
        print('updated')
        flash('Your Patient has been updated!', 'success')
        
    elif request.method == 'GET':
        form.ssnid.data = patient.ssnid
        form.pid.data = patient.id
        form.newname.data=patient.name
        form.newage.data=patient.age
        form.newaddress.data=patient.address
        form.bed.data=patient.bed
        form.city.data=patient.city
        form.state.data=patient.state
    print(form.errors)
    return render_template('patient/update_patient.html', title='Update Post',form=form)



@app.route("/createpatient/<int:post_id>/delete",methods=['GET', 'POST'])
@login_required
def delete_patient(post_id):
    patient = Patient.query.get_or_404(post_id)
    form=CreatePatientForm()
    form.pid.data=patient.id
    form.ssnid.data=patient.ssnid
    form.name.data=patient.name
    form.age.data=patient.age
    form.address.data=patient.address
    form.bed.data=patient.bed
    form.city.data=patient.city
    form.state.data=patient.state
    return render_template('patient/delete_patient.html',patient=patient ,title='Delete patient',legend='Delete Patient',form=form)

@app.route("/patient/<int:post_id>/delete", methods=['GET', 'POST'])
def removePatient(post_id):
    patient = Patient.query.get_or_404(post_id)
    db.session.delete(patient)
    db.session.commit()
    flash('Your patient has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/profile_patient/<int:post_id>", methods=['GET', 'POST'])
@login_required
def profile_patient(post_id):
    patient = Patient.query.filter_by(id=post_id).first_or_404()
    form=ProfilePatientForm()
    form.name.data = patient.name
    form.age.data = patient.age
    form.pid.data = patient.id
    form.ssnid.data = patient.ssnid
    form.state.data = patient.state
    form.city.data = patient.city
    form.bed.data=patient.bed
    form.doj.data=patient.doj
    form.dodc.data=patient.dodc
    form.address.data = patient.address
    return render_template('patient/profile_patient.html',post_id=post_id, legend='Patient Information',title='Profile',form=form)


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
    patient=Patient.query.filter_by(cid=account.acid).first()
    form = TransferForm()
    if form.validate_on_submit():
        if form.sourcetype.data=='1':
            a=datetime.now()
            ts=a.timestamp()
            _date=str(date.fromtimestamp(ts))


            saccount=Account.query.filter_by(acid=patient.cid).filter_by(accounttype='1').first()
            taccount=Account.query.filter_by(acid=patient.cid).filter_by(accounttype='2').first()
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

            saccount=Account.query.filter_by(acid=patient.cid).filter_by(accounttype='2').first()
            taccount=Account.query.filter_by(acid=patient.cid).filter_by(accounttype='1').first()
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
    if tags=='patient':
        data=Patient.query.all()
        
    return render_template('patient/all_patient.html',tag=tags,items=data,legend='All Patient' ,title='Patients')

    
    


