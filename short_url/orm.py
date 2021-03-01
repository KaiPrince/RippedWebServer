"""
* Project Name: Short_Url
* File Name: orm.py
* Programmer: Kai Prince
* Date: Sun, Feb 28, 2021
* Description: This file contains pydantic models for easy JSON mapping.
*   This model lives in the adapter layer.
"""
from pydantic import HttpUrl, BaseModel


class UrlDTO(BaseModel):
    url: HttpUrl


class ShortUrlDTO(BaseModel):
    short_url: HttpUrl
