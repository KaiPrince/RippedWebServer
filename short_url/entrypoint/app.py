"""
* Project Name: Short-Url
* File Name: entrypoint.py
* Programmer: Kai Prince
* Date: Sun, Feb 28, 2021
* Description: This file contains the FastAPI entrypoint.
"""

from fastapi import FastAPI
from .views import router


def create_app():
    app = FastAPI()

    app.include_router(router)

    return app
