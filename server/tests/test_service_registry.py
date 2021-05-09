"""
 * Project Name: RippedWebServer
 * File Name: test_service_registry.py
 * Programmer: Kai Prince
 * Date: Sun, Jan 24, 2021
 * Description: This file contains tests for the service registry functions.
"""
from flask import Flask
from pytest_mock import MockerFixture

from common import get_service_url


def test_get_service_url(mocker: MockerFixture, app: Flask):
    """ Call the get_service_url function. """
    # Arrange
    # ..Mock network call
    mock_func = mocker.patch("common.requests").get

    service_name = "AUTH_SERVICE"
    service_url = "abc"

    mock_func.return_value = service_url

    # Act
    with app.app_context():
        return_value = get_service_url(service_name)

    # Assert
    assert return_value == service_url
    mock_func.assert_called_once_with(
        app.config["SERVICE_REGISTRY_URL"] + f"/find/{service_name}/1.0")
