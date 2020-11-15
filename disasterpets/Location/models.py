from disasterpets import db, bcrypt, jwtmanager
from flask import Flask, current_app
import jwt

class Location(db.Model):
    __tablename__ = 'location'

    id = db.Column(db.Integer, primary_key =True, autoincrement=True)
    street_name = db.Column(db.String(50), nullable = True)
    house_number = db.Column(db.String(20), nullable = True)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(20), nullable = False)
    zipcode = db.Columne(db.String(20), nullable = True)

    def __init__(self, street_name, house_number, city, state, zipcode):
        self.street_name = street_name
        self.house_number = house_number
        self.city = city
        self.state = state
        self.zipcode = zipcode
    