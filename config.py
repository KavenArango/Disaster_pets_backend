from os import environ, path
from flask_jwt_extended import JWTManager



class Config:
    # General Config
    SECRET_KEY = 'for_the_pets'
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    PROPAGATE_EXCEPTIONS = True
    BCRYPT_LOG_ROUNDS = 13
    DEBUG = True

    #JWT
    JWT_SECRET_KEY = 'for_the_pets_jwt'

    #JWT_BLACKLIST_ENABLED = True
    #JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


    # Database
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://pets_root:1234shan!@" \
                                "petreunification.database.windows.net:1433/disasterpetsdb?" \
                                "DRIVER={ODBC Driver 17 for SQL Server}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

