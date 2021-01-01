from flaskblog import db
from datetime import datetime

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
