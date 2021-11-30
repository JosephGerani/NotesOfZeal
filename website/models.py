from website import db
from flask_login import UserMixin
from website import logging 


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(15), unique = True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(80))

class ToDoList(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    complete = db.Column(db.Boolean)

class FlashCards(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fcname = db.Column(db.String(50))
    fcdescription = db.Column(db.String(500))

@logging.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
