"""
 * Project Name: RippedWebServer
 * File Name: __init__.py
 * Programmer: Kai Prince
 * Date: Sun, Dec 13, 2020
 * Description: This file contains an interface for the FilesRepository.
 *  This module implements the repository pattern.
"""
from abc import ABC, abstractmethod


class IUsersRepository(ABC):
    """
    * Class Name: IUsersRepository
    * Purpose: This purpose of this class is to provide an interface for all
    *   User repositories.
    """

    @abstractmethod
    def __init__(self, db):
        pass

    @abstractmethod
    def index(self) -> list:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> dict:
        pass

    @abstractmethod
    def search(self, predicate: callable([..., bool])) -> list:
        pass

    @abstractmethod
    def create(self, username, password, permissions) -> int:
        pass

    @abstractmethod
    def edit(self, user_id, password, permissions) -> None:
        pass

    @abstractmethod
    def delete(self, user_id) -> None:
        pass
