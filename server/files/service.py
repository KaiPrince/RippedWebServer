import os
from db.service import get_db
from flask import current_app
import logging
import files.repository as repository


def get_index():
    """ Consumes nothing and produces a list of files. """

    return repository.index()


def get_file(id):
    """ Consumes an ID and produces a file name. """

    return repository.get_file(id)


def get_file_content(id):
    """ Consumes an ID and produces the file's contents. """

    return repository.get_file_content(id)


def download_file(id):
    """ Consumes an ID and produces a response which includes the file. """
    pass


def create_file(file_name, user_id, file_path, content_total):
    """ Consumes file details and produces a file id. """
    return repository.create_file(file_name, user_id, file_path, content_total)


def put_file(file_id, content_range, content_total, content):
    """Consumes a file id, file content and content-range,
    and produces a file size."""
    return repository.put_file(file_id, content_range, content_total, content)


def delete_file(id):
    """ Deletes a file from storage. """

    return repository.delete_file(id)
