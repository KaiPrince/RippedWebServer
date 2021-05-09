"""
* Project Name: RippedWebServer
* File Name: service_registry.py
* Programmer: Kai Prince
* Date: Sat, May 08, 2021
* Description: This file contains api calls to the service registry.
"""
from ipaddress import ip_address
from typing import Callable

import requests


class ServicesRepository:
    """
    * Class Name: ServicesRepository
    * Purpose: This purpose of this class is to make calls to the service
       registration service.
    """

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def make_ping_func(
        self,
        service_name: str,
        service_version: str,
        service_port=80,
    ) -> Callable:
        def func():
            url = f"{self.base_url}/register/{service_name}/{service_version}/{service_port}"

            requests.put(url)

        return func

    def get_auth_url(self) -> str:
        service_name = "auth"
        version = "1.0.0"
        return self._get_service_url(service_name, version)

    def get_files_url(self) -> str:
        service_name = "files"
        version = "1.0.0"
        return self._get_service_url(service_name, version)

    def get_disk_storage_url(self) -> str:
        service_name = "disk_storage"
        version = "1.0.0"
        return self._get_service_url(service_name, version)

    def _get_service_url(self, service_name, version) -> str:
        url = f"{self.base_url}/find/{service_name}/{version}"

        response = requests.get(url)
        if response.status_code == 404:
            raise Exception("Auth service not found in service registry.")

        # TODO handle service registry offline

        data = response.json()

        # e.g. "10.31.64.150"
        ip = ip_address(data["ip"])

        return str(ip)
