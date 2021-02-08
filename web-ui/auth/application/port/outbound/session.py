"""
 * Project Name: RippedWebServer
 * File Name: session.py
 * Programmer: Kai Prince
 * Date: Mon, Feb 08, 2021
 * Description: This file contains the interface for sessions.
"""

from abc import ABC, abstractmethod
from typing import Optional, Any


class Session(ABC):
    """
    * Class Name: Session
    * Purpose: This purpose of this class is to define the port interface for
    *   session-based storage between the controller and adapters.
    """

    @abstractmethod
    def set(self, key: str, data: object, ) -> Optional[Any]:
        pass

    @abstractmethod
    def get(self, key: str) -> Any:
        pass

    def clear(self) -> None:
        pass
