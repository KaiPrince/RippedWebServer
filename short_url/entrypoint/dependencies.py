"""
* Project Name: Short_Url
* File Name: dependencies.py
* Programmer: Kai Prince
* Date: Sun, Feb 28, 2021
* Description: This file contains factory functions for adapter and application
*   layer objects.
"""

from fastapi import Depends
from pymongo import MongoClient

import config
from repository import BaseUrlRepository, MongoRepository
from service import ShortUrlService


def make_repo():
    db = MongoClient(config.mongo_url)
    return MongoRepository(db)


def make_service(repo: BaseUrlRepository = Depends(make_repo)):
    return ShortUrlService(repo)
