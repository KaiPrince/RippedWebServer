"""
 * Project Name: RippedWebServer
 * File Name: repository.py
 * Programmer: Kai Prince
 * Date: Sat, Nov 21, 2020
 * Description: This file contains functions that call the disk_storage service API.
"""

from abc import ABC, abstractmethod

import requests

from auth.middleware import get_auth_middleware


class IDiskStorageRepository(ABC):
    """
    * Class Name: IDiskStorageRepository
    * Purpose: This purpose of this class is to provide an interface for disk storage
    *   repositories.
    """

    @abstractmethod
    def __init__(self, base_url, auth_middleware=None):
        pass

    @abstractmethod
    def index(self):
        pass

    @abstractmethod
    def search(self, predicate: callable([..., bool])):
        pass

    @abstractmethod
    def create(self, file_name, file_size) -> int:
        pass

    @abstractmethod
    def write(self, file_path, content_range, file_size, data) -> int:
        """Consumes a file path, content, and content metadata,
        and produces a file size."""
        pass

    @abstractmethod
    def download(file_path):
        pass

    @abstractmethod
    def delete(self, file_id) -> None:
        pass


class DiskStorageAPIRepository(IDiskStorageRepository):
    """
    * Class Name: DiskStorageRepository
    * Purpose: This purpose of this class is to make requests to the files service.
    """

    def __init__(self, base_url, auth_middleware):
        self.base_url = base_url

        self.auth_middleware = auth_middleware

    def index(self):
        index_url = self.base_url + "/storage/"

        response = requests.get(index_url, auth=self.auth_middleware)

        response.raise_for_status()

        return response.json()["files"]

    def search(self, predicate):
        raise NotImplementedError

    def create(self, file_path, file_size):
        """ Consumes a file path and size and returns json. """
        create_url = self.base_url + "/storage/create"

        response = requests.post(
            create_url,
            auth=self.auth_middleware,
            json={
                "file_path": file_path,
                "content_total": str(file_size),
            },
        )

        response.raise_for_status()

        return response.json()

    def write(self, file_path, content_range, content_total, content):
        """Consumes a file path, content, and content data,
        and produces a file size."""
        upload_url = self._get_upload_url(file_path)

        response = requests.put(
            upload_url,
            auth=self.auth_middleware,
            headers={
                "Content-Range": f"bytes {content_range}/{content_total}",
            },
            data=content,
        )

        response.raise_for_status()

        return response.json()["file_size"]

    def download(self, file_path):
        """ Consumes a file path and returns an Http Response. """

        download_url = self._get_download_url(file_path)

        return requests.get(download_url, auth=self.auth_middleware)

    def delete(self, file_path):
        """ Delete a file at the given file path. """
        delete_url = self.base_url + "/storage/delete/" + file_path

        response = requests.post(
            delete_url,
            auth=self.auth_middleware,
        )

        response.raise_for_status()

    def _get_upload_url(self, file_path):
        return self.base_url + "/storage/create/" + file_path

    def _get_download_url(self, file_path):
        return self.base_url + "/storage/download/" + file_path


def make_repository(base_url: str, auth_token: str) -> IDiskStorageRepository:

    if auth_token:
        auth_middleware = get_auth_middleware(auth_token)
    else:
        auth_middleware = None
    return DiskStorageAPIRepository(base_url, auth_middleware)
