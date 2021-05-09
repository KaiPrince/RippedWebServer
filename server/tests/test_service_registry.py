"""
 * Project Name: RippedWebServer
 * File Name: test_service_registry.py
 * Programmer: Kai Prince
 * Date: Sun, Jan 24, 2021
 * Description: This file contains tests for the service registry functions.
"""

from flask import Flask

# from pytest_mock import MockerFixture
import responses

from service_api.service_registry import ServicesRepository


@responses.activate
def test_get_service_url(app: Flask):
    """ Call the _get_service_url function. """
    # Arrange
    service_registry_url = app.config["SERVICE_REGISTRY_URL"]
    service_name = "auth"
    service_url = "10.10.10.10"

    expected_url = service_registry_url + f"/find/{service_name}/1.0.0"

    # ..Mock network call
    responses.add(responses.GET, expected_url, json={"ip": service_url})

    service_repo = ServicesRepository(service_registry_url)

    # Act
    with app.app_context():
        return_value = service_repo.get_auth_url()

    # Assert
    assert return_value == service_url

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == expected_url
