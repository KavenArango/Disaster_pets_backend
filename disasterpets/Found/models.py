from disasterpets import db, bcrypt, jwtmanager
from flask import Flask, current_app
import jwt


class FoundTable(db.Model):
    __tablename__ = 'foundtable'

    id = db.Column(db.Integer, primary_key =True, autoincrement=True)
    vetcheck = db.Column(db.Boolean)
    locationfound = db.Column(db.Integer, db.ForeignKey('locationjoin.id'))

    def __init__(self, vetcheck, locationfound):
        self.vetcheck = vetcheck
        self.locationfound = locationfound


        