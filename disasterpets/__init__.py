#initializing the application
import os
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_cors import CORS
from itsdangerous import URLSafeTimedSerializer
from jwt import PyJWT
import jwt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow



db = SQLAlchemy()
mail = Mail()
migrate = Migrate()
bcrypt = Bcrypt()
api = Api()
jwtmanager = JWTManager()
ma = Marshmallow()
url = URLSafeTimedSerializer('for_the_pets')

def create_app(test_config=None, instance_relative_config=False):
    app = Flask(__name__, instance_relative_config=True)
    api.init_app(app)
    app.config.from_object("config.Config")
    register_extensions(app, db)
    register_blueprints(app)
    with app.app_context():
        db.create_all()

    return app

def register_extensions(app, db):
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    jwtmanager.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    CORS(app)
    return None

def register_blueprints(app):
    #db
    from disasterpets.Account.models import User, Role, ReporterInfo, ReporterInfoJoin
    from disasterpets.Disaster.models import Disaster, DisasterLocationJoin, DisasterPetJoin
    #from disasterpets.Found.models import 
    #from disasterpets.Housing.models import 
    from disasterpets.Location.models import Location, LocationJoin
    from disasterpets.Lost.models import LostTable, OwnerRequest, PropertyInfo
    from disasterpets.Matching.models import PotentialMatch, PotentialMatchJoin, RejectMatch, RejectMatchJoin
    from disasterpets.Pets.models import Pets, PetsJoin, PetStatus, Breeds, AlteredStatus, Animals, UniqueFeature, UniqueFeaturesJoin
    from disasterpets.Pictures.models import PetImage, PetImageJoin
    #routes
    from disasterpets.Account.routes import account
    from disasterpets.Pets.routes import petbp
    from disasterpets.Matching.routes import matchingbp
    from disasterpets.Pictures.routes import petgallerybp, rainbowgallerybp
    app.register_blueprint(account)
    app.register_blueprint(petbp)
    app.register_blueprint(matchingbp)
    app.register_blueprint(petgallerybp)
    app.register_blueprint(rainbowgallerybp)
    return None



# @jwtmanager.token_in_blacklist_loader
# def check_if_token_in_blacklist(decrypted_token):   
#     jti = decrypted_token['jti']
#     return Model.RevokedTokenModel.is_jti_blacklisted(jti)


