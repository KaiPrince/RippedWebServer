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
    FILES_SERVICE_URL = os.getenv("FILES_SERVICE_URL")
    PUBLIC_FILES_SERVICE_URL = os.getenv("PUBLIC_FILES_SERVICE_URL")
    AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
    DISK_STORAGE_SERVICE_URL = os.getenv("DISK_STORAGE_SERVICE_URL")
    JWT_KEY = os.getenv("JWT_KEY")

    def __init__(self, app: Flask):

        if self.SECRET_KEY is None:
            logging.warning("SECRET_KEY environment variable not set.")

        if self.FILES_SERVICE_URL is None:
            logging.warning("FILES_SERVICE_URL environment variable not set.")
            self.FILES_SERVICE_URL = "http://rippedwebserver_files_1:5000"

        if self.PUBLIC_FILES_SERVICE_URL is None:
            logging.warning("PUBLIC_FILES_SERVICE_URL environment variable not set.")
            self.PUBLIC_FILES_SERVICE_URL = "http://files.kaiprince.xyz"

        if self.AUTH_SERVICE_URL is None:
            logging.warning("AUTH_SERVICE_URL environment variable not set.")
            self.AUTH_SERVICE_URL = "http://rippedwebserver_auth_1:5000"

        if self.DISK_STORAGE_SERVICE_URL is None:
            logging.warning("DISK_STORAGE_SERVICE_URL environment variable not set.")
            self.DISK_STORAGE_SERVICE_URL = "http://rippedwebserver_disk_storage_1:5000"

        if self.JWT_KEY is None:
            logging.warning("JWT_KEY environment variable not set.")
            self.JWT_KEY = "dev"


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
