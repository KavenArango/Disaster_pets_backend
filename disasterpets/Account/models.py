from flask import Flask, current_app
import jwt
from datetime import datetime, timedelta
from disasterpets import db, bcrypt



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

    def __init__(self, fname, lname, email, password, phone, phone2, role_id):
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
        

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, seconds=5),
                'iat': datetime.utcnow(),
                'sub': user_id
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
    
