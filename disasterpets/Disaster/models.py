from disasterpets import db, bcrypt, jwtmanager
from flask import Flask, current_app
import jwt

class Disaster(db.Model):
    __tablename__ = 'disaster'

    id = db.Column(db.Integer, primary_key =True, autoincrement=True)
    disaster_name = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable = False)
    end_date = db.Column(db.Date, nullable = False)
    disaster_location = db.Column(db.Integer, db.ForeignKey('location.id'))

    def __init__(self, role_name, disaster_name):
        self.role_name = role_name
        self.disaster_name = disaster_name

class DisasterPetJoin(db.Model):
    __tablename__ = "disasterpetjoin"

    id = db.Column(db.Integer, primary_key = True, autoincrement =True)
    petid = db.Column(db.Integer, db.ForeignKey('pets.id'))
    disasterid = db.Column(db.Integer, db.ForeignKey('disaster.id'))

    def __init__(self, petid, disasterid):
        self.petid = petid
        self.disasterid = disasterid

class DisasterLocationJoin(db.Model):
    __tablename__ = "disasterlocationjoin"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    disasterid = db.Column(db.Intger, db.ForeignKey('disaster.id'))
    dlocationid = db.Column(db.Integer, db.ForeignKey('location.id'))

    def __init__(self, disasterid, dlocationid):
        self.disasterid = disasterid
        self.dlocationid = dlocationid
