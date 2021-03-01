"""
* Project Name: SET-Capstone
* File Name: service.py
* Programmer: Kai Prince
* Date: Sun, Feb 28, 2021
* Description: This file contains the ShortUrlService class.
"""
from repository import BaseUrlRepository
from url import shorten_url, Url, ShortUrl


class ShortUrlService:
    """
    * Class Name: ShortUrlService
    * Purpose: This purpose of this class is to present a facade for the service
    *   layer.
    """

    def __init__(self, url_repo: BaseUrlRepository):
        self.url_repo = url_repo

    def make_short_url(self, url: str) -> str:
        return make_short_url(url, self.url_repo)

    def get_full_url(self, short_url: str) -> str:
        return get_full_url(short_url, self.url_repo)


def make_short_url(url: str, url_repo: BaseUrlRepository) -> str:
    url = Url(url)

    short_url = shorten_url(url)

    found_url = False
    max_retries = 5
    for _ in range(max_retries):
        if url_repo.get_by_short_url(short_url) is None:
            found_url = True
            break
        short_url = shorten_url(url)

    if not found_url:
        raise Exception(
            f"Couldn't find an available URL uuid within {max_retries} attempts."
        )

    url_repo.add(short_url, url)
    return short_url


def get_full_url(short_url: str, url_repo: BaseUrlRepository) -> str:
    short_url = ShortUrl(short_url)
    full_url = url_repo.get_by_short_url(short_url)
    return full_url
