from datetime import datetime
from flaskbank import login_manager,db
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), nullable=False)
    #email=db.Column(db.String(80),nullable=False,unique=True)
    
    def __repr__(self):
        return f"user('{self.username}','{self.password}')"

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, unique=True, )
    ssnid = db.Column(db.Integer,unique=True, nullable=False, )
    name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state= db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100),nullable= False)
    last_updated = db.Column(db.DateTime,nullable = False, default = datetime.utcnow)
    #operation = db.relationship('Accountoperation', backref='customerop', lazy='dynamic', primaryjoin="and_(Customer.cid==Accountoperation.ccid,Customer.status==Accountoperation.cstatus)")
    accountrelo=db.relationship('Account',backref='custm',lazy=True)

    def __repr__(self):
        return f"Customer('{self.cid}','{self.ssnid}','{self.name}','{self.age}','{self.address}','{self.city}','{self.state}','{self.status}','{self.last_updated}')"

class Account(db.Model):
    __tablename__ = 'account'
    aid = db.Column(db.Integer, primary_key=True)
    acid=db.Column(db.Integer,db.ForeignKey('customer.cid'))
    accounttype= db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Integer,nullable=False )
    status = db.Column(db.String(100),nullable= False)
    last_updated = db.Column(db.DateTime,nullable = False, default = datetime.utcnow)
    operation = db.relationship('Accountoperation', backref='accop', lazy='dynamic', primaryjoin="and_(Account.accounttype==Accountoperation.aaccounttype,Account.aid==Accountoperation.aaid)")
    customerrelo=db.relationship('Customer',backref='acc',lazy=True)
    def __repr__(self):
        return f"Account('{self.aid}','{self.accounttype}','{self.balance}')"

class Accountoperation(db.Model):
    __tablename__ = 'accountoperation'
    aoid = db.Column(db.Integer, primary_key=True)
    aaccounttype= db.Column(db.String(100), db.ForeignKey('account.accounttype'),nullable=False)
    #cstatus = db.Column(db.String(100),db.ForeignKey('customer.status'),nullable=False)
    message = db.Column(db.String(100),nullable=False)
    last_updated=db.Column(db.String,nullable=False)
    ccid=db.Column(db.Integer,db.ForeignKey('customer.cid'),nullable=False)
    aaid=db.Column(db.Integer,db.ForeignKey('account.aid'),nullable=False)
    amount=db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f"Account Status('{self.aoid}','{self.aaccounttype}','{self.amount}','{self.message}','{self.last_updated}','{self.ccid}','{self.aaid}')"
