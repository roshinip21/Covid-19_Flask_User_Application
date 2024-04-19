from flask_login import UserMixin
from . import db

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(1000))
    dob = db.Column(db.Date())
    gender = db.Column(db.String(10))
    phone = db.Column(db.Integer())
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Vaccination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email=db.Column(db.String(1000))
    dob = db.Column(db.Date())
    gender = db.Column(db.String(10))
    phone = db.Column(db.Integer())
    aadhar = db.Column(db.Integer())
    address = db.Column(db.String(1000))
    address2 = db.Column(db.String(1000))
    city = db.Column(db.String(1000))
    state = db.Column(db.String(1000))
    pincode = db.Column(db.Integer())
    insurancename = db.Column(db.String(1000))
    insuranceid = db.Column(db.String(1000))

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(1000))
    datetime = db.Column(db.String(1000))
    gender = db.Column(db.String(10))
    phone = db.Column(db.Integer())
    com=db.Column(db.String(1000))
