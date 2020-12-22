import logging
import os

from dotenv import find_dotenv, load_dotenv
from flask import Flask


class Config(object):

    # Import config from .env file
    load_dotenv(find_dotenv())

    # Import config from environment
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE = os.getenv("DATABASE")
    JWT_KEY = os.getenv("JWT_KEY")
    MONGO_USERNAME = os.getenv("MONGO_USERNAME")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_DBNAME = os.getenv("MONGO_DBNAME")

    def __init__(self, app: Flask):

        if self.SECRET_KEY is None:
            logging.warning("SECRET_KEY environment variable not set.")

        if self.DATABASE is None:
            logging.warning("DATABASE environment variable not set.")
            self.DATABASE = os.path.join(app.instance_path, "web_server.sqlite")

        if self.JWT_KEY is None:
            logging.warning("JWT_KEY environment variable not set.")
            self.JWT_KEY = "dev"

        if self.MONGO_USERNAME is None:
            logging.warning("MONGO_USERNAME environment variable not set.")
            self.MONGO_USERNAME = "dbAdmin"

        if self.MONGO_PASSWORD is None:
            logging.warning("MONGO_PASSWORD environment variable not set.")

        if self.MONGO_DBNAME is None:
            logging.warning("MONGO_DBNAME environment variable not set.")
            self.MONGO_DBNAME = "auth"


# class Config(object):
#     DEBUG = False
#     TESTING = False
#     DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    # DATABASE_URI = "mysql://user@localhost/foo"
    MODE = "PRODUCTION"


class DevelopmentConfig(Config):
    MODE = "DEVELOPMENT"
    DEBUG = True

    def __init__(self, app: Flask):

        if self.SECRET_KEY is None:
            self.SECRET_KEY = "dev"

        super().__init__(app)


class TestingConfig(Config):
    MODE = "TESTING"
    TESTING = True

    def __init__(self, app: Flask):

        if self.SECRET_KEY is None:
            self.SECRET_KEY = "dev"

        super().__init__(app)


def getConfig(app: Flask):
    mode = os.getenv("FLASK_ENV")
    if mode is not None:
        mode = mode.upper()  # Normalize case

    if mode == "DEVELOPMENT":
        return DevelopmentConfig(app)
    elif mode == "PRODUCTION":
        return ProductionConfig(app)
    elif mode == "TESTING":
        return TestingConfig(app)
    else:
        logging.warning(
            "FLASK_ENV environment variable not set. Defaulting to DEVELOPMENT mode."
        )
        return DevelopmentConfig(app)
