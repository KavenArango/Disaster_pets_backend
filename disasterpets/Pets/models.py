from flask import Flask
import jwt
from disasterpets import db

class Pets(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key =True, autoincrement=True)
    pet_name = db.Column(db.String(50), nullable=True)
    