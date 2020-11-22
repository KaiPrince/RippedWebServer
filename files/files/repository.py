"""
 * Project Name: RippedWebServer
 * File Name: repository.py
 * Programmer: Kai Prince
 * Date: Sat, Nov 21, 2020
 * Description: This file contains functions that call the dist_storage service API.
"""

import requests

base_url = "http://localhost:5002"


def index():
    """ Get all files from files service. """

    response = requests.get(base_url + "/")

    return response.json()["files"]


def get_file(file_path):
    """ Get the file details at the given path. """
    pass


def get_file_content(file_path):
    """ Get the contents of the file at the given path. """
    pass


def create_file(file_name):
    """ Consumes a file name and returns a file path. """

    pass


def put_file(file_path, content_range, content_total, content):
    """ Consumes a file path, content, and content data, and produces a file size. """
    print("put_file", file_path, content_range, content_total, content)

    return requests.put(
        base_url + "/files/create",
        headers={
            "Content-Range": f"bytes {content_range}/{content_total}",
            "file_path": file_path,
        },
        data=content,
    )


def delete_file(file_path):
    """ Delete a file at the given file path. """
    pass
