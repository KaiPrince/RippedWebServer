"""
* Project Name: RippedWebServer
* File Name: url.py
* Programmer: Kai Prince
* Date: Sun, Feb 28, 2021
* Description: This file contains the Url entity and logic.
"""
import uuid
from urllib.parse import urlparse, urlunparse
from typing import NewType


Url = NewType("Url", str)
ShortUrl = NewType("ShortUrl", str)


def shorten_url(url: Url) -> ShortUrl:
    rand_id = uuid.uuid4()
    parsed_url = urlparse(url)
    short_url = urlunparse(
        (parsed_url.scheme, parsed_url.netloc, str(rand_id), "", "", "")
    )

    short_url = ShortUrl(short_url)

    return short_url
