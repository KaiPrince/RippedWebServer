import os
import logging
from flask import (
    current_app,
    send_from_directory,
)

from werkzeug.utils import secure_filename


def list_files():
    folder = current_app.config["UPLOAD_FOLDER"]
    files = os.listdir(folder)

    return files


def get_file(file_name):
    content = ""
    with open(file_name, "rb") as f:
        content = f.read()

    return content


def create_file(file_name, file):

    filename = secure_filename(file_name)
    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    return file_path


def delete_file(file_name):

    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], file_name)

    try:
        os.remove(file_path)

    except FileNotFoundError as e:
        logging.error(f"Failed to delete {file_path}.", exc_info=e)
        raise e
