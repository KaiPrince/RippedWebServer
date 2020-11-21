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


def delete_file(id):
    """ Deletes a file from storage. """

    return repository.delete_file(id)
