#initializing the application
import os
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from jwt import PyJWT
import jwt
from flask_jwt_extended import JWTManager



db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
api = Api()
jwtmanager = JWTManager()

def create_app(test_config=None, instance_relative_config=False):

    app = Flask(__name__, instance_relative_config=True)
    api.init_app(app)
    app.config.from_object("config.Config")
    register_extensions(app)
    register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app

def register_extensions(app):
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwtmanager.init_app(app)
    
    return None

def register_blueprints(app):
    from disasterpets.Account.routes import account
    from disasterpets.Pets.routes import petbp
    app.register_blueprint(account)
    app.register_blueprint(petbp)
    return None

# @jwtmanager.token_in_blacklist_loader
# def check_if_token_in_blacklist(decrypted_token):   
#     jti = decrypted_token['jti']
#     return Model.RevokedTokenModel.is_jti_blacklisted(jti)


