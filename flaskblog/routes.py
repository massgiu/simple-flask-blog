from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
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

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')