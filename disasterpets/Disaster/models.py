from disasterpets import db, bcrypt, jwtmanager
from flask import Flask, current_app
import jwt


class Disaster(db.Model):
    __tablename__ = 'disaster'

    id = db.Column(db.Integer, primary_key =True, autoincrement=True)
    disaster_name = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable = False)
    end_date = db.Column(db.Date, nullable = True)

    def __init__(self, disaster_name, start_date, end_date):
        self.disaster_name = disaster_name
        self.start_date = start_date
        self.end_date = end_date
        

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
    disasterid = db.Column(db.Integer, db.ForeignKey('disaster.id'))
    dis = db.relationship("Disaster", uselist=False, lazy='select', foreign_keys=[disasterid])
    dlocationid = db.Column(db.Integer, db.ForeignKey('countytable.id'))
    county = db.relationship("CountyTable", uselist=False, lazy='select', foreign_keys=[dlocationid])

    def __init__(self, disasterid, dlocationid):
        self.disasterid = disasterid
        self.dlocationid = dlocationid
