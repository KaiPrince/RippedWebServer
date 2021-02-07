"""
 * Project Name: RippedWebServer
 * File Name: permissions_reader.py
 * Programmer: Kai Prince
 * Date: Sat, Feb 06, 2021
 * Description: This file contains the interface for the PermissionsReader.
"""

from abc import ABC, abstractmethod
from auth.domain.auth_ticket import AuthTicket


class IPermissionsReader(ABC):
    """
    * Class Name: IPermissionsReader
    * Purpose: This purpose of this class is to define an interface for the
    *  PermissionsReader classes.
    """

    @abstractmethod
    def __init__(self, auth_ticket: AuthTicket):
        pass

    @abstractmethod
    def may_delete(self, resource):
        """ Consumes a resource, such as a file id, and produces a boolean. """
        pass

    @abstractmethod
    def may_share(resource):
        """ Consumes a resource, such as a file id, and produces a boolean. """
        pass
