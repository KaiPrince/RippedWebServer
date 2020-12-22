"""
 * Project Name: RippedWebServer
 * File Name: __init__.py
 * Programmer: Kai Prince
 * Date: Sun, Dec 13, 2020
 * Description: This file contains an interface for the FilesRepository.
 *  This module implements the repository pattern.
"""
from abc import ABC, abstractmethod


class IFilesRepository(ABC):
    """
    * Class Name: IRepository
    * Purpose: This purpose of this class is to provide an interface for all
    *   repositories.
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
    def create(self, file_name, user_id, file_path) -> str:
        pass

    @abstractmethod
    def edit(self, file_id, file_name, user_id, file_path) -> None:
        pass

    @abstractmethod
    def delete(self, file_id) -> None:
        pass
