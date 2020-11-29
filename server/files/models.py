"""
 * Project Name: RippedWebServer
 * File Name: models.py
 * Programmer: Kai Prince
 * Date: Sun, Nov 29, 2020
 * Description: This file contains models definitions for the files app.
"""

from typing_extensions import Protocol


class File(Protocol):
    file_id: int
    file_name: str
    file_path: str
    file_size: str
    user_id: int
