from os import environ, path


class Config:
    # General Config
    SECRET_KEY = "for_the_pets"
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")
    BCRYPT_LOG_ROUNDS = 13

    # Database
    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc://pets_root:1234shan!@"
        "petreunification.database.windows.net:1433/disasterpetsdb?"
        "pyodbc_driver_name={ODBC Driver 17 for SQL Server}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False