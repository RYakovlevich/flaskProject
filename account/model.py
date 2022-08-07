from settings import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)


    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email
