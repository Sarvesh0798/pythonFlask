from datetime import datetime
<<<<<<< HEAD
from flaskblog import login_manager,db
from flask_login import UserMixin



=======
from flaskblog import db, login_manager
from flask_login import UserMixin


>>>>>>> c5ebdc3467f09a485195f438e5351d2825a7342e
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


<<<<<<< HEAD
class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), nullable=False)
    email=db.Column(db.String(80),nullable=False,unique=True)
    
    def __repr__(self):
        return f"user('{self.username}','{self.password}','{self.email}')"

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
    customerstatus = db.relationship('Customerstatus', backref='customer', lazy='dynamic',primaryjoin="and_(Customer.ssnid==Customerstatus.cssnid,Customer.cid==Customerstatus.ccid,Customer.status==Customerstatus.cstatus)")
    operation = db.relationship('Accountoperation', backref='customer', lazy='dynamic', primaryjoin="and_(Customer.cid==Accountoperation.ccid,Customer.status==Accountoperation.cstatus)")
                                                      
    def __repr__(self):
        return f"Customer('{self.cid}','{self.ssnid}','{self.name}','{self.age}','{self.address}','{self.city}','{self.state}','{self.status}','{self.last_updated}')"

class Account(db.Model):
    __tablename__ = 'account'
    aid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    accounttype= db.Column(db.String(100), unique=True, nullable=False)
    deposit = db.Column(db.Integer,nullable=False )
    operation = db.relationship('Accountoperation', backref='account', lazy='dynamic', primaryjoin="and_(Account.accounttype==Accountoperation.aaccounttype,Account.aid==Accountoperation.aaid)")

    def __repr__(self):
        return f"Account('{self.aid}','{self.accounttype}','{self.deposit}')"

class Customerstatus(db.Model):
    __tablename__ = 'Customerstatus'
    csid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(100),nullable=False)
    last_updated=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    cssnid=db.Column(db.Integer,db.ForeignKey('customer.ssnid'),nullable=False)
    ccid=db.Column(db.Integer,db.ForeignKey('customer.cid'),nullable=False)
    cstatus=db.Column(db.Integer,db.ForeignKey('customer.status'),nullable=False)
    
    def __repr__(self):
        return f"Customer Status('{self.csid}','{self.cstatus}','{self.message}','{self.last_updated}','{self.cssnid}','{self.ccid}')"

class Accountoperation(db.Model):
    __tablename__ = 'accountoperation'
    aoid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aaccounttype= db.Column(db.String(100), db.ForeignKey('account.accounttype'),nullable=False)
    cstatus = db.Column(db.String(100),db.ForeignKey('customer.status'),nullable=False)
    message = db.Column(db.String(100),nullable=False)
    last_updated=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    ccid=db.Column(db.Integer,db.ForeignKey('customer.cid'),nullable=False)
    aaid=db.Column(db.Integer,db.ForeignKey('account.aid'),nullable=False)

    def __repr__(self):
        return f"Account Status('{self.aoid}','{self.aaccounttype}','{self.cstatus}','{self.message}','{self.last_updated}','{self.ccid}','{self.aaid}')"
=======
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
>>>>>>> c5ebdc3467f09a485195f438e5351d2825a7342e
