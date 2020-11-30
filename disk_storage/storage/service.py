import logging
import os

import sys

from flask import current_app  # send_from_directory,
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


def pass_in_chunks(file_name: str, func):
    with open(file_name, "rb") as f:
        for chunk in read_in_chunks(f):
            func(chunk)


def read_in_chunks(file_object, chunk_size=1024):
    """ Consumes an open file handle and generatively produces binary data. """
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def create_file(file_name, file_size):

    filename = secure_filename(file_name)
    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

    # TODO check enough free space

    with open(file_path, "wb"):
        pass

    return filename


def put_file(file_path, seek_position, content):
    """Consumes a file path, insertion position, and file content,
    and produces a file size."""

    filename = secure_filename(file_path)
    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

    current_app.logger.info(f"Writing {sys.getsizeof(content)} bytes to {filename}.")
    with open(file_path, "ab") as f:
        f.seek(seek_position)
        f.write(content)

    file_size = os.path.getsize(file_path)
    return file_size


def delete_file(file_name):

    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], file_name)

    try:
        os.remove(file_path)

    except FileNotFoundError as e:
        logging.error(f"Failed to delete {file_path}.", exc_info=e)
        raise e
