from flaskbank import app, db, bcrypt
from flaskbank.models import User, Customer, Accountoperation,Account 


username=input('Enter username')
password=input('Enter password')

choice=input('do you want to reset db? y/n')
if choice=='y':
    db.drop_all()                    #to rebuild entire db with new changes in DB

          
db.create_all()
user=User.query.filter_by(username=username).first()
if user==None:
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.add(user)
    db.session.commit()
