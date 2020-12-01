"""
 * Project Name: RippedWebServer
 * File Name: logging.py
 * Programmer: Kai Prince
 * Date: Tue, Dec 01, 2020
 * Description: This file contains a common logging handler.
"""

from logging import Handler, LogRecord
import requests
from requests.auth import AuthBase
from datetime import datetime
import os


class LogServiceHandler(Handler):
    """
    * Class Name: LogServiceHandler
    * Purpose: This purpose of this class is to send log messages to
    *  the logging service.
    """

    def __init__(self, url, auth_middleware, app_name, *args, **kwargs):
        self.url = url
        self.auth_middleware = auth_middleware
        self.app_name = app_name

        super().__init__(*args, **kwargs)

    def emit(self, record: LogRecord):
        message = self.format(record)
        level = record.levelname
        date_time = datetime.now().isoformat()
        application_name = self.app_name
        process_id = os.getpid()
        process_name = "python.exe"

        json = {
            "message": message,
            "logLevel": level,
            "applicationName": application_name,
            "dateTime": date_time,
            "processName": process_name,
            "processId": process_id,
        }

        requests.post(self.url, json=json, auth=self.auth_middleware)


class LoggerAuth(AuthBase):
    """
    * Class Name: LoggerAuth
    * Purpose: This purpose of this class is to inject an auth token into requests.
    """

    def __init__(self, auth_token):
        # setup any auth-related data here
        self.auth_token = auth_token

    def __call__(self, req: requests.PreparedRequest):
        # modify and return the request

        req.headers["x-access-token"] = self.auth_token

        return req


def get_auth_middleware(auth_token: str) -> AuthBase:
    return LoggerAuth(auth_token)


def make_log_handler(url, auth_token, app_name) -> Handler:
    auth_middleware = get_auth_middleware(auth_token)
    handler = LogServiceHandler(url, auth_middleware, app_name)
    return handler
