from flask import Flask, current_app
import jwt
from disasterpets import db
from datetime import datetime

    

class Breeds(db.Model):
    __tablename__ = 'breeds'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    breed = db.Column(db.String(50), nullable = False)

    def __init__(self, breed):
        self.breed = breed
    

class AlteredStatus(db.Model):
    __tablename__ = 'alteredstatus'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(50), unique = True, nullable = False)

    def __init__(self, status):
        self.status = status

class Animals(db.Model):
    __tablename__ = 'animals'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    animal = db.Column(db.String(50), unique = True, nullable = False)

    def __init__(self, breed):
        self.animal = animal

class PetsJoin(db.Model):
    __tablename__ = 'petsjoin'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))

    def __init__(self, user_id, pet_id):
        self.user_id = user_id
        self.pet_id = pet_id

class UniqueFeature(db.Model):
    __tablename__ ='uniquefeature'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    breed = db.Column(db.Integer, db.ForeignKey('breeds.id'))
    animal = db.Column(db.Integer, db.ForeignKey('animals.id'))
    feature = db.Column(db.String(50))

    def __init__(self, breed, animal, feature):
        self.breed = breed
        self.animal = animal
        self.feature = feature

class UniqueFeaturesJoin(db.Model):
    __tablename__ = 'uniquefeaturesjoin'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    petid = db.Column(db.Integer, db.ForeignKey('pets.id'))
    featureid = db.Column(db.Integer, db.ForeignKey('uniquefeature.id'))

    def __init__(self, petid, featureid):
        self.petid = petid
        self.featureid = featureid

class PetStatus(db.Model):
    __tablename__ = 'petstatus' 

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    status = db.Column(db.String(20))

    def __init__(self, status):
        self.status = status

class Gender(db.Model):
    __tablename__ = 'gender'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    gender = db.Column(db.String(10))

    def __init__(self, gender):
        self.gender = gender


class Pets(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key =True, autoincrement=True)
    pet_name = db.Column(db.String(50), nullable=True)
    animal_type = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable = True)
    animal = db.relationship("Animals", backref=db.backref("pets", lazy="dynamic"))
    primary_breed = db.Column(db.Integer, db.ForeignKey('breeds.id'), nullable = True)
    secondary_breed = db.Column(db.Integer, db.ForeignKey('breeds.id'), nullable = True)
    breed = db.relationship("Breeds", foreign_keys=[primary_breed])
    breedtwo = db.relationship("Breeds", foreign_keys=[secondary_breed])
    gender = db.Column(db.Integer(), db.ForeignKey("gender.id"), nullable = False)
    sex = db.relationship("Gender", backref=db.backref("pets", lazy="dynamic"))
    altered_status = db.Column(db.Integer, db.ForeignKey('alteredstatus.id'), nullable = True)
    altered = db.relationship("AlteredStatus", backref=db.backref("pets", lazy="dynamic"))
    pet_status = db.Column(db.Integer, db.ForeignKey('petstatus.id'), nullable = True)
    petstatus = db.relationship("PetStatus", backref=db.backref("pets", lazy="dynamic"))
    trapper_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = True)
    date_created = db.Column(db.Date,nullable = False )

    def __init__(self, pet_name, animal_type, gender, primary_breed, secondary_breed, altered_status, trapper_id, pet_status):
        self.pet_name = pet_name
        self.animal_type = animal_type
        self.gender = gender
        self.primary_breed = primary_breed
        self.secondary_breed = secondary_breed
        self.altered_status = altered_status
        self.pet_status = pet_status
        self.date_created = datetime.now()