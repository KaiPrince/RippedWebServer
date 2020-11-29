import logging
import os

from flask import current_app, flash

import files.repository as repository
from werkzeug.exceptions import abort
from requests import HTTPError, ConnectionError


def get_index():
    """ Consumes nothing and produces a list of files. """

    try:
        files = repository.index()
    except (HTTPError, ConnectionError):
        flash("Could not retrieve file index.", category="error")
        files = []

    return files


def get_file(id):
    """ Consumes an ID and produces a file name. """

    return repository.get_file(id)


def get_file_content(id):
    """ Consumes an ID and produces the file's contents. """

    return repository.get_file_content(id)


def download_file(id):
    """ Consumes an ID and produces binary data and meta data. """

    file_path = repository.get_file(id)["file_path"]
    result = repository.download_file(id)

    result.raise_for_status()

    raw = result.raw

    headers = dict(raw.headers)

    def generate():
        for chunk in raw.stream(decode_content=False):
            yield chunk

    # return (result.content, result.headers["Content-Type"], file_path)
    return (generate(), headers, file_path)


def create_file(file_name, user_id, file_path, content_total):
    """ Consumes file details and produces a file id. """
    current_app.logger.debug(
        "create_file "
        + str({"file_name": file_name, "user_id": user_id, "file_path": file_path}),
    )

    return repository.create_file(file_name, user_id, file_path, content_total)


def put_file(file_id, content_range, content_total, content):
    """Consumes a file id, file content and content-range,
    and produces a file size."""
    current_app.logger.debug(
        "put_file "
        + str(
            {
                "file_id": file_id,
                "content_range": content_range,
                "content_total": content_total,
                "content": content,
            }
        ),
    )

    response = repository.put_file(file_id, content_range, content_total, content)

    response.raise_for_status()

    return response.json()["file_size"]


def delete_file(id):
    """ Deletes a file from storage. """

    return repository.delete_file(id)
