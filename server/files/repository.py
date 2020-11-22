"""
 * Project Name: RippedWebServer
 * File Name: repository.py
 * Programmer: Kai Prince
 * Date: Sat, Nov 21, 2020
 * Description: This file contains functions that call the files service API.
"""

import requests


def index():
    """ Get all files from files service. """

    response = requests.get("localhost:5003")

    return response.json


def get_file(id):
    """ Get a file with the matching id. """
    pass


def get_file_content(id):
    """ Get the contents of the file with the matching id. """
    pass


def delete_file(id):
    """ Delete a file with the matching id. """
    pass
