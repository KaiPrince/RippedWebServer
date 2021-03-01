"""
* Project Name: RippedWebServer
* File Name: test_factory.py
* Programmer: Kai Prince
* Date: Sun, Feb 28, 2021
* Description: This file contains factory tests for building the app.
"""
from entrypoint.app import create_app


def test_create_app():
    create_app()
