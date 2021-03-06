from hospital import app, db, bcrypt
from hospital.models import User, Patient, Medicine,Diagonastic,MedicineMaster,DiagonasticMaster 


username=input('Enter username')
password=input('Enter password')
print('What is your type? \n 1)Registeration Executive \n 2)Pharmacist \n 3)Diagnostic executive')

tchoice=input('type 1 2 3')
if tchoice=='1':
    utype='regExec'
elif tchoice=='2':
    utype='pharmacist'
elif tchoice=='3':
    utype='diagExec'
else :
    print('invalid choice')
    exit() 

choice=input('do you want to reset db? y/n')
if choice=='y':
    db.drop_all()                    #to rebuild entire db with new changes in DB
    db.create_all()
    for i in range(10):
        med=MedicineMaster(mName="abc"+str(i),qty=100,rate=20,status='available')
        db.session.add(med)  
    db.session.commit()
    for i in range(10):
        diag=DiagonasticMaster(dName=str(i)+"abc",amt=2000)
        db.session.add(diag)  
    db.session.commit()


user=User.query.filter_by(username=username).first()
if user==None:
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username,utype=utype ,password=hashed_password)
    db.session.add(user)
    db.session.commit()
