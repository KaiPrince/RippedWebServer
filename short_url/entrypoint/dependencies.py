"""
* Project Name: Short_Url
* File Name: dependencies.py
* Programmer: Kai Prince
* Date: Sun, Feb 28, 2021
* Description: This file contains factory functions for adapter and application
*   layer objects.
"""

from fastapi import Depends

from repository import InMemRepository, BaseUrlRepository
from service import ShortUrlService


def make_repo():
    return InMemRepository()


def make_service(repo: BaseUrlRepository = Depends(make_repo)):
    return ShortUrlService(repo)
