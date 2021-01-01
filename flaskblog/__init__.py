from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #var
#Set secret  cookie
app.config['SECRET_KEY'] = 'e4f3b857d3c940c8a2683afa6055ad29'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # /// relative path (site.db is db file)
db = SQLAlchemy(app) #instance of DB

from flaskblog import routes