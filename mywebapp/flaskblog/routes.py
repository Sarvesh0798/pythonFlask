import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm,  CreateCustomerForm, UpdateCustomerForm, SearchCustomerForm
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
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)



@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/")
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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)



@app.route("/searchcustomer/<tag>", methods=['GET', 'POST'])
@login_required
def search_customer(tag):
    form=SearchCustomerForm()
    if form.validate_on_submit():
        
        flash('Account found!', 'success')
        if tag =='update':
            return redirect(url_for('update_customer',post_id='1'))
        else:
             return redirect(url_for('delete_customer',post_id='1'))   
        
    return render_template('customer/update.html',title='search customer',form=form)



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

@app.route("/post/<int:post_id>/delete",)
@login_required
def removeCustomer(post_id):
    post = Post.query.get_or_404(post_id)
    form=CreateCustomerForm()
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/createcustomer", methods=['GET', 'POST'])
def createCustomer():
    if current_user.is_authenticated:
        
        form = CreateCustomerForm()
        if form.validate_on_submit():
            print("added")
        return render_template('customer/create_customer.html',legend='Delete Customer', title='CreateCustomer', form=form)
        
    else:
        
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    
@app.route("/createcustomer/<int:post_id>/update")
@login_required
def update_customer(post_id):
    post = Post.query.get_or_404(post_id)
    
    form = UpdateCustomerForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.ssnid.data = '123456'
        form.cid.data = '120544'
        form.oldname.data='mr. shah'
        form.oldage.data="23"
        form.oldaddress.data='mumbai'
    return render_template('customer/update_customer.html', title='Update Post',form=form)
    
    


