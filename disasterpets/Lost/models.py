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

    def __init__(self, petid, admincheck):
        self.petid = petid
        self.admincheck = admincheck
