"""
* Project Name: RippedWebServer
* File Name: conftest.py
* Programmer: Kai Prince
* Date: Sun, Feb 28, 2021
* Description: This file contains test configuration.
"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from entrypoint.app import create_app
from repository import InMemRepository
from service import ShortUrlService


@pytest.fixture
def app() -> FastAPI:
    return create_app()


@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app)


@pytest.fixture
def mock_repo() -> InMemRepository:
    url_repo = InMemRepository()
    return url_repo


@pytest.fixture
def mock_url_service(mock_repo) -> ShortUrlService:
    service = ShortUrlService(mock_repo)
    return service
