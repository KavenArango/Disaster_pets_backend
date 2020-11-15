from disasterpets import db, bcrypt, jwtmanager
from flask import Flask, current_app
import jwt

class PotentialMatch(db.Model):
    __tablename__ = 'potentialmatch'

    id = db.Column(db.Integer, primary_key =True, autoincrement=True)
    petid = db.Column(db.Integer, db.ForeignKey('pets.id'))
    admincheck = db.Column(db.Boolean)

    def __init__(self, petid, admincheck):
        self.petid = petid
        self.admincheck = admincheck

class PotentialMatchJoin(db.Model):
    __tablename__ = 'potentialjoin'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    petid = db.Column(db.Integer, db.ForeignKey('pets.id'))
    potentialid = db.Column(db.Integer, db.ForeignKey('potentialmatch.id'))

    def __init__(self, petid, potentialid):
        self.petid = petid
        self.potentialid = potentialid

class RejectMatch(db.Model):
    __tablename__ = 'rejectmatch'

    id = db.Column(db.Integer, primary_key = True, Autoincrement=True)
    petid = db.Column(db.Integer, db.ForeignKey('pets.id'))
    admincheck = db.Column(db.Boolean)

    def __init__(self, petid, admincheck):
        self.petid = petid
        self.admincheck = admincheck

class RejectMatchJoin(db.Model):
    __tablename__ = 'rejectjoin'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    petid = db.Column(db.Integer, db.ForeignKey('pets.id'))
    rejectid = db.Column(db.Integer, db.ForeignKey('rejectmatch.id'))

    def __init__(self, petid, rejectid):
        self.petid = petid
        self.rejectid = rejectid

    
       