import os

from flask import Flask
import files.middleware


def init_app(app: Flask):
    """ Ensure uploads folder exists. """

    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        print("Creating Upload folder at", app.config["UPLOAD_FOLDER"])
        os.mkdir(app.config["UPLOAD_FOLDER"])
