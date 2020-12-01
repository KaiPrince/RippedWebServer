"""
 * Project Name: RippedWebServer
 * File Name: repository.py
 * Programmer: Kai Prince
 * Date: Sat, Nov 21, 2020
 * Description: This file contains functions that call the files service API.
"""

import requests
from auth.middleware import get_auth_middleware
from abc import ABC, abstractmethod


class IFilesRepository(ABC):
    """
    * Class Name: IRepository
    * Purpose: This purpose of this class is to provide an interface for all
    *   repositories.
    """

    @abstractmethod
    def __init__(self, base_url, auth_middleware=None):
        pass

    @abstractmethod
    def index(self):
        pass

    @abstractmethod
    def get_by_id(self, id: int):
        pass

    @abstractmethod
    def search(self, predicate: callable([..., bool])):
        pass

    @abstractmethod
    def create(self, file_name, user_id, file_path, content_total) -> int:
        pass

    @abstractmethod
    def edit(self, file_id, file_name, user_id, file_path, content_total) -> None:
        pass

    @abstractmethod
    def delete(self, file_id) -> None:
        pass


class FilesAPIRepository(IFilesRepository):
    """
    * Class Name: FilesServiceRepository
    * Purpose: This purpose of this class is to make requests to the files service.
    """

    def __init__(self, base_url, auth_middleware):
        self.base_url = base_url

        self.auth_middleware = auth_middleware

    def index(self):
        """ Get all files from files service. """

        response = requests.get(self.base_url + "/", auth=self.auth_middleware)

        response.raise_for_status()

        return response.json()["files"]

    def get_by_id(self, id):
        """ Get a file with the matching id. """

        response = requests.get(
            f"{self.base_url}/files/{id}", auth=self.auth_middleware
        )

        response.raise_for_status()

        return response.json()

    def search(self, predicate):
        raise NotImplementedError

    def create(self, file_name, user_id, file_path, content_total):
        """ Consumes file details and returns a file id. """

        response = requests.post(
            self.base_url + "/files/create",
            json={
                "file_name": file_name,
                "user_id": user_id,
                "file_path": file_path,
                "content_total": str(content_total),
            },
            auth=self.auth_middleware,
        )
        return response.json()["file_id"]

    def edit(self, file_id, file_name, user_id, file_path, content_total):
        raise NotImplementedError

    def delete(self, id):
        """ Delete a file with the matching id. """
        response = requests.post(
            f"{self.base_url}/files/delete/{id}", auth=self.auth_middleware
        )

        return response


def make_repository(base_url: str, auth_token: str) -> IFilesRepository:

    if auth_token:
        auth_middleware = get_auth_middleware(auth_token)
    else:
        auth_middleware = None
    return FilesAPIRepository(base_url, auth_middleware)
