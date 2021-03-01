"""
* Project Name: Short_Url
* File Name: views.py
* Programmer: Kai Prince
* Date: Sun, Feb 28, 2021
* Description: This file contains the blueprint routes.
"""

from fastapi import APIRouter, status, Depends

from entrypoint.dependencies import make_service
from orm import UrlDTO, ShortUrlDTO
from service import ShortUrlService

router = APIRouter(prefix="/url")


@router.post(
    "/make-short-url/",
    response_model=ShortUrlDTO,
    status_code=status.HTTP_201_CREATED,
)
def make_short_url(url: UrlDTO, url_service: ShortUrlService = Depends(make_service)):
    raw_short_url = url_service.make_short_url(url.url)

    return ShortUrlDTO(short_url=raw_short_url)


@router.post(
    "/get-full-url/",
    response_model=UrlDTO,
)
def get_full_url(short_url: ShortUrlDTO, url_service: ShortUrlService = Depends(make_service)):
    raw_url = url_service.get_full_url(short_url.short_url)

    return UrlDTO(url=raw_url)
