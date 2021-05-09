"""
* Project Name: RippedWebServer
* File Name: service_registry.py
* Programmer: Kai Prince
* Date: Sat, May 08, 2021
* Description: This file contains api calls to the service registry.
"""

import requests


class ServicesRepository:
    """
    * Class Name: ServicesRepository
    * Purpose: This purpose of this class is to make calls to the service
       registration service.
    """

    def __init__(
        self,
        base_url: str,
        service_name="files",
        service_version="1.0.0",
        service_port=80,
    ) -> None:
        self.base_url = base_url
        self.service_name = service_name
        self.service_version = service_version
        self.service_port = service_port

    def ping_service_registry(self):
        url = f"{self.base_url}/register/{self.service_name}/{self.service_version}/{self.service_port}"

        requests.put(url)

    def get_disk_storage_url(self):
        service_name = "disk_storage"
        version = "1.0.0"
        url = f"{self.base_url}/find/{service_name}/{version}"

        response = requests.get(url)
        if response.status_code == 404:
            raise Exception("Service not found.")

        data = response.json()

        # e.g. "[::ffff:10.31.64.150]"
        ip = data["ip"]

        return ip
