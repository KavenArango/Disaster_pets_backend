from disasterpets import db, bcrypt, jwtmanager
from flask import Flask, current_app
import jwt

class LostTable(db.Model):
    __tablename__ = 'losttable'

    id = db.Column(db.Integer, primary_key =True, autoincrement=True)
    petid = db.Column(db.Integer, db.ForeignKey('pets.id'))
    ownerrequest = db.Column(db.Integer, db.ForeignKey('ownerrequest.id'))
    reportinfo = db.Column(db.Integer, db.ForeignKey('reporterinfojoin.id'))
    startinglocation = db.Column(db.Integer, db.ForeignKey('locationjoin.id'))

    def __init__(self, petid, ownerrequest, reportinfo, startinglocation):
        self.petid = petid
        self.ownerrequest = ownerrequest
        self.reportinfo = reportinfo
        self.startinglocation =startinglocation

class OwnerRequest(db.Model):
    __tablename__ = 'ownerrequest'

    id = db.Column(db.Integer, primary_key =True, autoincrement=True)
    feeder = db.Column(db.String(120), nullable = True)
    fieldcrew = db.Column(db.String(120), nullable = True)
    notes = db.Column(db.String(200), nullable = True)
    propertyinfo = db.Column(db.Integer, db. ForeignKey('propertyinfo.id'))

    def __init__(self, feeder, fieldcrew, notes, propertyinfo):
        self.feeder = feeder
        self.fieldcrew = fieldcrew
        self.notes = notes
        self.propertyinfo = propertyinfo

class PropertyInfo(db.Model):
    __tablename__ = 'propertyinfo'
    
    id = db.Column(db.Integer, primary_key =True, autoincrement=True)
    permission = db.Column(db.Boolean, nullable = False)
    notes = db.Column(db.String(200), nullable = True)

    def __init__(self, permission, notes):
        self.permission = permission
        self.notes = notes

