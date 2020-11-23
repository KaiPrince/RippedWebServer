"""
 * Project Name: RippedWebServer
 * File Name: repository.py
 * Programmer: Kai Prince
 * Date: Sat, Nov 21, 2020
 * Description: This file contains functions that call the files service API.
"""

import requests
from flask import current_app


def _base_url():
    return current_app.config["FILES_SERVICE_URL"]


def index():
    """ Get all files from files service. """

    response = requests.get(_base_url() + "/")

    return response.json()["files"]


def get_file(id):
    """ Get a file with the matching id. """

    response = requests.get(f"{_base_url()}/files/{id}")

    response.raise_for_status()

    return response.json()


def get_file_content(id):
    """ Get the contents of the file with the matching id. """
    response = requests.get(f"{_base_url()}/files/content/{id}")

    return response.content


def create_file(file_name, user_id, file_path, content_total):
    """ Consumes file details and returns a file id. """

    response = requests.post(
        _base_url() + "/files/create",
        json={
            "file_name": file_name,
            "user_id": user_id,
            "file_path": file_path,
            "content_total": str(content_total),
        },
    )
    return response.json()["file_id"]


def put_file(file_id, content_range, content_total, content):
    """ Consumes a file id, content, and content data, and produces a file size. """

    return requests.put(
        _base_url() + "/files/create",
        headers={
            "Content-Range": f"bytes {content_range}/{content_total}",
            "file_id": str(file_id),
        },
        data=content,
    )


def download_file(id):
    """ Consumes a file id and returns an Http Response. """
    return requests.get(f"{_base_url()}/files/download/{id}")


def delete_file(id):
    """ Delete a file with the matching id. """
    response = requests.post(f"{_base_url()}/files/delete/{id}")

    return response
