"""
 * Project Name: RippedWebServer
 * File Name: response.py
 * Programmer: Kai Prince
 * Date: Sun, Feb 07, 2021
 * Description: This file contains a response humble object for use as a DTO.
"""

from typing import Any


class Response:
    """
    * Class Name: Response
    * Purpose: This purpose of this class is to preserve the boundary between
    *   the use case and the implementation.
    """

    data: Any
