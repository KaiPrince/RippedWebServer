"""
* Project Name: RippedWebServer
* File Name: test_shorten_url.py
* Programmer: Kai Prince
* Date: Sun, Feb 28, 2021
* Description: This file contains tests for the url-shortener feature.
"""
import pytest
from pytest_mock import MockFixture
from fastapi.testclient import TestClient

from repository import InMemRepository
from service import ShortUrlService
from url import shorten_url, Url, ShortUrl


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ["http://example.com/this-is-a-long-url", "http://example.com/ABCDEF"],
        ["http://example.com/this-is-another-long-url", "http://example.com/123456"],
    ],
)
def test_make_short_url(url: str, expected: str, mocker: MockFixture):
    """ Converts a Url to a short url. """
    # Arrange
    url: Url = Url(url)
    mocker.patch("url.uuid.uuid4").return_value = expected.split("/")[-1]

    # Act
    short_url = shorten_url(url)

    # Assert
    assert short_url == expected


def test_repo_store_url():
    """ Stores a url. """
    # Arrange
    url = Url("http://example.com/this-is-a-long-url")
    short_url = ShortUrl("http://example.com/ABCDEF")
    url_repo = InMemRepository()

    # Act
    url_repo.add(short_url, url)

    # Assert
    assert url_repo.get_by_short_url(short_url) == url


def test_service_level_store_url(mocker, mock_url_service):
    """ Stores the url from the service level. """
    # Arrange
    url = "http://example.com/this-is-a-long-url"
    short_url = "http://example.com/ABCDEF"
    mocker.patch("url.uuid.uuid4").return_value = short_url.split("/")[-1]

    # Act
    result = mock_url_service.make_short_url(url)

    # Assert
    assert result == short_url
    assert mock_url_service.get_full_url(short_url) == url


def test_store_short_url_collision(
    mocker: MockFixture, mock_url_service: ShortUrlService
):
    """ Recreates short url if it's already taken. """
    # Arrange
    url = "http://example.com/this-is-a-long-url"
    short_url = "http://example.com/ABCDEF"
    url_hash = short_url.split("/")[-1]
    new_hash = "new-hash"
    new_url = "http://example.com/new-hash"
    old_url = "http://example.com/this-is-another-long-url"
    mocker.patch("url.uuid.uuid4").side_effect = [url_hash, url_hash, new_hash]

    mock_url_service.make_short_url(old_url)

    # Act
    result = mock_url_service.make_short_url(url)

    # Assert
    assert result == new_url
    assert mock_url_service.get_full_url(short_url) == old_url
    assert mock_url_service.get_full_url(result) == url


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ["http://example.com/this-is-a-long-url", "http://example.com/ABCDEF"],
        ["http://example.com/this-is-another-long-url", "http://example.com/123456"],
    ],
)
def test_get_short_url_route(client: TestClient, url, expected, mocker):
    """ Calls the get short url route. """
    # Arrange
    route_url = "/url/make-short-url/"
    mocker.patch("url.uuid.uuid4").return_value = expected.split("/")[-1]

    # Act
    response = client.post(route_url, json={"url": url})

    # Assert
    assert response.status_code == 201

    response_data = response.json()
    assert "short_url" in response_data
    assert response_data["short_url"] == expected
