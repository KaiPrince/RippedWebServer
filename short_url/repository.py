"""
* Project Name: RippedWebServer
* File Name: repository.py
* Programmer: Kai Prince
* Date: Sun, Feb 28, 2021
* Description: This file contains repositories.
"""

from abc import ABC, abstractmethod
from typing import Dict
from pymongo import MongoClient

from url import Url, ShortUrl


class BaseUrlRepository(ABC):
    @abstractmethod
    def add(self, short_url: ShortUrl, url: Url):
        pass

    @abstractmethod
    def get_by_short_url(self, short_url: ShortUrl) -> Url:
        pass


class InMemRepository(BaseUrlRepository):

    store: Dict[ShortUrl, Url]

    def __init__(self):
        self.store = dict()

    def add(self, short_url: ShortUrl, url: Url):
        self.store[short_url] = url

    def get_by_short_url(self, short_url: ShortUrl) -> Url:
        return self.store.get(short_url)


class MongoRepository(BaseUrlRepository):
    """
    * Class Name: MongoRepository
    * Purpose: This purpose of this class is to implement the repository pattern
    *   with a MongoDB client.
    """
    db_name = "urls"
    collection_name = "urls"

    def __init__(self, db: MongoClient):
        self.db_client = db
        self.db = db.get_database(self.db_name)
        self.collection = self.db.get_collection(self.collection_name)

    def add(self, short_url: ShortUrl, url: Url):
        self.collection.insert_one({"short_url": short_url, "full_url": url})

    def get_by_short_url(self, short_url: ShortUrl) -> Url:
        record = self.collection.find_one({"short_url": short_url})

        return record.get("full_url") if record is not None else None
