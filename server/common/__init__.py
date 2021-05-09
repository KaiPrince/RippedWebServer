"""
 * Project Name: RippedWebServer
 * File Name: __init__.py
 * Programmer: Kai Prince
 * Date: Sun, Nov 22, 2020
 * Description: This file contains shared functions.
"""
import re
from threading import Timer
from typing import Callable

import requests

from flask import current_app


def get_content_metadata(header_string):
    """ Consumes a Content-Range header and produces (range, total). """

    # e.g. 'bytes 0-9999999/14364672'
    m = re.match(
        r"bytes (?P<range>\d+\-\d+)/(?P<total>\d+)",
        header_string,
    )
    content_range = m.group("range")
    content_total = m.group("total")

    return (content_range, content_total)


def periodically_do(func: Callable, interval_in_seconds: float):
    def _do():
        func()
        Timer(interval_in_seconds, _do).start()

    Timer(interval_in_seconds, _do).start()
