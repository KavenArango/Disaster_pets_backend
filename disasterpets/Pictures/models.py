from flask import Flask, current_app
import jwt
from disasterpets import db


class PetImage(db.Model):
    __tablename__ = 'petimage'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    image_url =db.Column(db.String(200), nullable = False)

    def __init__ (self, image_url)
        self.image_url = image_url

class PetImageJoin(db.Model):
    __tablename__ = 'petimagejoin'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    petimage_id = db.Column(db.Integer, db.ForeignKey('petimage.id'))

    def __init__ (self, pet_id, petimage_id):
        self.pet_id = pet_id
        self.petimage_id = petimage_id