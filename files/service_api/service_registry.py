"""
* Project Name: RippedWebServer
* File Name: service_registry.py
* Programmer: Kai Prince
* Date: Sat, May 08, 2021
* Description: This file contains api calls to the service registry.
"""

import requests


def ping_service_registry(base_url):
    # TODO move to config.
    service_name = "files"
    service_version = "1.0.0"
    service_port = 80
    url = f"{base_url}/register/{service_name}/{service_version}/{service_port}"

    requests.put(url)
