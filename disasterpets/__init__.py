# initializing the application
import os
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app(test_config=None, instance_relative_config=False):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.Config")

    db.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        from disasterpets.Account.routes import account

        app.register_blueprint(account)

        from disasterpets.Account.models import User
        from disasterpets.Pets.models import Pets

        migrate.init_app(app, db)
        db.create_all()

    return app