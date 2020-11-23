"""
 * Project Name: RippedWebServer
 * File Name: repository.py
 * Programmer: Kai Prince
 * Date: Sat, Nov 21, 2020
 * Description: This file contains functions that call the dist_storage service API.
"""

import requests

base_url = "http://rippedwebserver_disk_storage_1:5000"


def index():
    """ Get all files from files service. """

    response = requests.get(base_url + "/")

    return response.json()["files"]


def get_file(file_path):
    """ Get the file details at the given path. """
    pass


def get_file_content(file_path):
    """ Get the contents of the file at the given path. """
    response = requests.get(
        f"{base_url}/storage/file-content", headers={"file_path": file_path}
    )

    return response.content


def create_file(file_name, file_size):
    """ Consumes a file name and returns a file path. """

    return requests.post(
        base_url + "/storage/create",
        json={
            "file_path": file_name,
            "content_total": str(file_size),
        },
    )


def put_file(file_path, content_range, content_total, content):
    """ Consumes a file path, content, and content data, and produces a file size. """

    return requests.put(
        base_url + "/storage/create",
        headers={
            "Content-Range": f"bytes {content_range}/{content_total}",
            "file_path": file_path,
        },
        data=content,
    )


def delete_file(file_path):
    """ Delete a file at the given file path. """
    response = requests.post(
        base_url + "/storage/delete",
        headers={
            "file_path": file_path,
        },
    )

    return response
