from datetime import datetime
from hospital import login_manager,db
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), nullable=False)
    utype = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return f"user('{self.username}','{self.password}')"

class Patient(db.Model):
    __tablename__ = 'Patient'
    id = db.Column(db.Integer, primary_key=True)
    ssnid = db.Column(db.Integer,unique=True, nullable=False, )
    name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state= db.Column(db.String(100), nullable=False)
    bed = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    doj = db.Column(db.String(50),nullable = False)
    dodc=db.Column(db.String(50))
    medrelo=db.relationship('Medicine',backref='diag',lazy=True)
    diagrelo=db.relationship('Diagonastic',backref='med',lazy=True)

    def __repr__(self):
        return f"Patient('{self.id}','{self.ssnid}','{self.name}','{self.age}','{self.address}','{self.city}','{self.state}','{self.bed}','{self.doj}','{self.dodc}')"

class Medicine(db.Model):
    __tablename__ = 'Medicine'
    mName = db.Column(db.String(20),primary_key=True ,nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    pid = db.Column(db.Integer, db.ForeignKey('Patient.id'), nullable=False)
    
    def __repr__(self):
        return f"Medicine('{self.mName}','{self.qty}','{self.rate}','{self.amount}')"

class MedicineMaster(db.Model):
    __tablename__ = 'MedicineMaster'
    mName = db.Column(db.String(20),primary_key=True ,nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, )
    
    
    def __repr__(self):
        return f"Medicine('{self.mName}','{self.qty}','{self.rate}','{self.status}')"
 

class Diagonastic(db.Model):
    __tablename__='Diagonastic'
    dName = db.Column(db.String(20),primary_key=True ,nullable=False)
    amt = db.Column(db.Integer, nullable=False)
    pid = db.Column(db.Integer, db.ForeignKey('Patient.id'), nullable=False)
    
    def __repr__(self):
        return f"Diagonastic('{self.dName}','{self.amt}')"

class DiagonasticMaster(db.Model):
    __tablename__='DiagonasticMaster'
    dName = db.Column(db.String(20),primary_key=True ,nullable=False)
    amt = db.Column(db.Integer, nullable=False)
    
    
    def __repr__(self):
        return f"Diagonastic('{self.dName}','{self.amt}')"
