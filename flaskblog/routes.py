import secrets, os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required

posts = [
    {
        'author': 'M. Giunchi',
        'title': 'Blog post 1',
        'content': 'First post',
        'date_posted' : 'June 1 2020'
    },
    {
        'author': 'M. Giunchi',
        'title': 'Blog post 2',
        'content': 'Second post',
        'date_posted' : 'June 2 2020'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts = posts)

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
        #create instance of user
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        #insert instance in db
        db.session.add(user)
        db.session.commit()
        flash(f'Your accont has been created successfully!','success')
        return redirect(url_for('login')) #redirect to the function

    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next') #get next parameter in the url
            #if next parameter exists in the url redirect to account page, else to home page
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Check your email and password','danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return (redirect(url_for('home')))

def save_picture(form_picture):
    #randomize name so we don't have collisions
    random_hex = secrets.token_hex(8)
    #grab file extension in order to keep for image saved
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex+f_ext #new filename
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn) #destination directory for profile pics
    #resizing
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    #on update button
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        #update data on db
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        #fill form with existing data
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/'+current_user.image_file) #profile_pics is a dir
    return render_template('account.html', title='Account', image_file=image_file, form=form)
