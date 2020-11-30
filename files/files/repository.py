"""
 * Project Name: RippedWebServer
 * File Name: repository.py
 * Programmer: Kai Prince
 * Date: Sat, Nov 21, 2020
 * Description: This file contains functions that call the dist_storage service API.
"""

import requests
from flask import current_app
from authlib.jose import jwt
from datetime import timedelta
from time import time


def _base_url():
    return current_app.config["DISK_STORAGE_SERVICE_URL"]


def get_file_content(file_path):
    """ Get the contents of the file at the given path. """
    response = requests.get(
        f"{_base_url()}/storage/file-content", headers={"file_path": file_path}
    )

    return response.content


def create_file(file_name, file_size):
    """ Consumes a file name and returns a file path. """

    return requests.post(
        _base_url() + "/storage/create",
        json={
            "file_path": file_name,
            "content_total": str(file_size),
        },
    )


def put_file(file_path, content_range, content_total, content):
    """ Consumes a file path, content, and content data, and produces a file size. """

    return requests.put(
        _base_url() + "/storage/create",
        headers={
            "Content-Range": f"bytes {content_range}/{content_total}",
            "file_path": file_path,
        },
        data=content,
    )


def download_file(file_path):
    """ Consumes a file path and returns an Http Response. """
    return requests.get(f"{_base_url()}/storage/download/{file_path}")


def delete_file(file_path):
    """ Delete a file at the given file path. """

    # TODO Delete this and use the auth service!
    # or better yet install a pub/sub message broker
    header = {"alg": "HS256"}

    payload = {
        "permissions": ["write: disk_storage"],
        "iat": int(time()),
        "exp": int(time()) + timedelta(hours=1).total_seconds(),
    }

    key = current_app.config["JWT_KEY"]
    token = jwt.encode(header, payload, key).decode("utf-8")

    response = requests.post(
        _base_url() + "/storage/delete",
        headers={
            "Authorization": token,
            "file_path": file_path,
        },
    )

    return response
