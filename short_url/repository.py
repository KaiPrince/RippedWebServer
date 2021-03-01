"""
* Project Name: RippedWebServer
* File Name: repository.py
* Programmer: Kai Prince
* Date: Sun, Feb 28, 2021
* Description: This file contains repositories.
"""

from abc import ABC, abstractmethod
from typing import Dict

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
