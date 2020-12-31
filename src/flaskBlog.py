from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from src.forms import RegistrationForm, LoginForm
app = Flask(__name__) #var

#Set secret  cookie
app.config['SECRET_KEY'] = 'e4f3b857d3c940c8a2683afa6055ad29'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # /// relative path (site.db is db file)

db = SQLAlchemy(app) #instance of DB

#define DB structure
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    #This is a relationship non a field, but I can query user.posts (launch a query)
    #author field is linked with user_id to User table
    posts = db.relationship('Post', backref='author', lazy=True) #the user can create many posts, but every post has one user

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) #we pass function and non current time datetime.utcnow()
    content = db.Column(db.Text, nullable=False)
    #This fiel is the primary key of User Table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),  nullable=False) #user.id is the name of field

    #This method prints the obj representation
    def __repr__(self):
        return f"User('{self.title}','{self.date_posted}')"

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Accont created for {form.username.data}!','success')
        return redirect(url_for('home')) #redirect to the function

    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!','success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Check your username and password','danger')
    return render_template('login.html', title='Login', form=form)

# if __name__ == "__main__":
#     app.run(debug=True)