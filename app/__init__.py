import os

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask import Flask

myapp_obj = Flask(__name__)
myapp_obj.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
myapp_obj.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(myapp_obj)
bcrypt = Bcrypt(myapp_obj)
login_manager = LoginManager(myapp_obj)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app import routes