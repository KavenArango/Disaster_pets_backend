from flask import Flask, current_app
import jwt
from datetime import datetime, timedelta
from disasterpets import db, bcrypt, jwtmanager


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key =True, autoincrement=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False) 
    password = db.Column(db.VARCHAR(255), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    phone2 = db.Column(db.String(20), nullable = True)
    date_created = db.Column(db.Date,nullable = False )
    last_logged = db.Column(db.Date, nullable = True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    social = db.Column(db.Integer, db.ForeignKey('socialmedia.id'), nullable=True)


    def __init__(self, fname, lname, email, password, phone, phone2, role_id, social):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.phone = phone
        self.phone2 = phone2
        self.date_created = datetime.now()
        self.last_logged = datetime.now()
        self.role_id = role_id
        #self.reporter = reporter
        #self.owner = owner
        self.social = social


        
        
    def encode_auth_token(self, user_id, user_role_id):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
                'sub': user_id,
                'role': user_role_id
            }
            return jwt.encode(
                payload,
                current_app.secret_key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, current_app.secret_key)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key =True, autoincrement=True)
    role_name = db.Column(db.String(50), nullable=False)

    def __init__(self, role_name):
        self.role_name = role_name

class SocialMedia(db.Model):
    __tablename__ = 'socialmedia'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    fb = db.Column(db.String(150), nullable = True)
    twitter = db.Column(db.String(150), nullable = True)
    insta = db.Column(db.String(150), nullable = True)

    def __init__(self, fb, twitter, insta):
        self.fb = fb
        self.twitter = twitter
        self.insta = insta


class ReporterInfo(db.Model):
    __tablename__ = "reporter"

    id = db.Column(db.Integer, primary_key =True, autoincrement=True)
    spottedlocation = db.Column(db.Integer, db.ForeignKey("locationjoin.id"))
    spottedimage = db.Column(db.Integer, db.ForeignKey("petimage.id"), nullable = True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    notes = db.Column(db.String(100), nullable = True)

class ReporterInfoJoin(db.Model):
    __tablename__ = "reporterinfojoin"

    id = db.Column(db.Integer, primary_key =True, autoincrement=True)
    petid = db.Column(db.Integer, db.ForeignKey("pets.id"))
    reporterid = db.Column(db.Integer, db.ForeignKey('reporter.id'))

    def __init__(self, petid, reporterid):
        self.petid = petid
        self.reporterid = reporterid

    
