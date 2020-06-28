import os
import secrets
from random import randint
from PIL import Image
from datetime import datetime,date
import pytz
from flask import render_template, url_for, flash, redirect, request, abort
from hospital import app, db, bcrypt
from hospital.forms import  LoginForm, CreatePatientForm, UpdatePatientForm,ProfilePatientForm ,SearchPatientForm, MedicineForm
from hospital.models import User, Patient, Medicine,Diagonastic,MedicineMaster,DiagonasticMaster
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
  
        ts=dateTime.timestamp()
        _date=str(date.fromtimestamp(ts))
        
        patient=Patient(doj=_date,ssnid=form.ssnid.data,name=form.name.data,age=form.age.data,bed=form.bed.data,address=form.address.data,state=form.state.data,city=form.city.data,status='Active') 
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
            return redirect(url_for('status',tags='bill',post_id=patient.id))
        elif tag=='med':
            return redirect(url_for('status',tags='med',post_id=patient.id))
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
        ts=dateTime.timestamp()
        _date=str(date.fromtimestamp(ts))

        patient.name=form.newname.data
        patient.age=form.newage.data
        patient.address=form.newaddress.data
        patient.city=form.city.data
        patient.bed=form.bed.data
        patient.state=form.state.data
        patient.last_updated=_date
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

@app.route("/status/<tags>/<int:post_id>",methods=['POST','GET'])
@login_required
def status(tags,post_id):
    if tags=='patient':
        data=Patient.query.all()
        return render_template('patient/all_patient.html',tag=tags,items=data,legend='All Patient' ,title='Patients')
    elif tags=='bill':
        data=Patient.query.filter_by(id=post_id).first()
        medData=Medicine.query.filter_by(pid=data.id).all()
        diagData=Diagonastic.query.filter_by(pid=data.id).all()
        return render_template('patient/bill_patient.html',tag=tags,pat=data,medItems=medData,diagItems=diagData,legend='All Patient' ,title='Patients')    
    elif tags=='med':
        data=Patient.query.filter_by(id=post_id).first()
        medData=Medicine.query.filter_by(pid=data.id).all()
        
        return render_template('medTest/medicine_patient.html',pat=data,medItems=medData,legend='All Patient' ,title='Patients')    
    
    

@app.route("/newmedicine/<int:post_id>",methods=['POST','GET'])
@login_required
def newMedicine(post_id):
    form=MedicineForm()
    data=Patient.query.filter_by(id=post_id).first()
    medMaster=MedicineMaster.query.all()
    if form.validate_on_submit():
        
        return redirect(url_for('searchMedicine',medname=form.searchMed.data,post_id=data.id))
    print(form.errors)
    return render_template('medTest/new_medicine.html',qty='disable',pat=data,medMast=medMaster,legend='All Patient' ,title='Patients',form=form)    

@app.route("/searchmedicine/<medname>/<int:post_id>",methods=['POST','GET'])
@login_required
def searchMedicine(medname,post_id):
    form=MedicineForm()
    data=Patient.query.filter_by(id=post_id).first()
    medMaster=MedicineMaster.query.filter_by(mName=medname).all()
    _medMaster=MedicineMaster.query.filter_by(mName=medname).first()
    if form.validate_on_submit():
        _medMaster.qty=_medMaster.qty - form.quantity.data
        med= Medicine(mName=_medMaster.mName,qty=form.quantity.data,rate=_medMaster.rate,amount=(_medMaster.rate * form.quantity.data),pid=data.id)
        db.session.add(med)
        db.session.commit()
        return redirect(url_for('status',tags='med',post_id=data.id))
    print(form.errors)
    return render_template('medTest/new_medicine.html',pat=data,qty='enable',medMast=medMaster,legend='All Patient' ,title='Patients',form=form)    

#---------------------------------------------------------------------------------------------------#


