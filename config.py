from os import environ, path
from flask_jwt_extended import JWTManager



class Config:
    # General Config
    SECRET_KEY = "for_the_pets"
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")
    PROPAGATE_EXCEPTIONS = True
    BCRYPT_LOG_ROUNDS = 13
    DEBUG = True

    # JWT
    JWT_SECRET_KEY = "for_the_pets_jwt"
    JWT_DECODE_ALGORITHMS = ['HS512']

    # JWT_BLACKLIST_ENABLED = True
    # JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    # Database
    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc://pets_root:1234shan!@"
        "petreunification.database.windows.net:1433/disasterpetsdb?"
        "DRIVER={ODBC Driver 17 for SQL Server}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "pet.reunification22@gmail.com"
    MAIL_PASSWORD = "forthepets22"
    MAIL_DEFAULT_SENDER = "Pet Disasters"
    MAIL_MAX_EMAILS = None
    MAIL_SUPRESS_SEND = False
    MAIL_ASCII_ATTACHMENTS = False
    # UPLOAD_FOLDER =
    # ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'raw'}
