from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__) #var
#Set secret  cookie
app.config['SECRET_KEY'] = 'e4f3b857d3c940c8a2683afa6055ad29'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # /// relative path (site.db is db file)
db = SQLAlchemy(app) #instance of DB
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' #if you try to visit a page that require authentication, redirect to login
login_manager.login_message_category = 'info' #bootstrap class
from flaskblog import routes