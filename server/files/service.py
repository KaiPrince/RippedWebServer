import logging
import os

from flask import current_app, flash, session

from files.repository import get_repository as _get_repository, IRepository
from werkzeug.exceptions import abort
from requests import HTTPError, ConnectionError


def get_repository() -> IRepository:
    base_url = current_app.config["FILES_SERVICE_URL"]
    auth_token = session.get("auth_token")

    return _get_repository(base_url, auth_token)


def get_index():
    """ Consumes nothing and produces a list of files. """

    repository = get_repository()

    try:
        files = repository.index()
    except (HTTPError, ConnectionError):
        # TODO move library-specific errors to repo and make custom errors
        flash("Could not retrieve file index.", category="error")
        files = []

    return files


def get_file(id):
    """ Consumes an ID and produces a file name. """

    repository = get_repository()

    return repository.get_by_id(id)


def download_file(id):
    """ Consumes an ID and produces binary data and meta data. """

    repository = get_repository()

    file_path = repository.get_by_id(id)["file_path"]
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

    repository = get_repository()

    return repository.create(file_name, user_id, file_path, content_total)


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
    repository = get_repository()

    response = repository.write(file_id, content_range, content_total, content)

    response.raise_for_status()

    return response.json()["file_size"]


def delete_file(id):
    """ Deletes a file from storage. """
    repository = get_repository()

    return repository.delete(id)
