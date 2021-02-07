"""
 * Project Name: RippedWebServer
 * File Name: permission.py
 * Programmer: Kai Prince
 * Date: Fri, Feb 05, 2021
 * Description: This file contains the Permission model.
"""


class Permission:
    """
    * Class Name: Permission
    * Purpose: This purpose of this class is to define the properties
    *  of the Permission entity.
    *  A permission is used authorize certain actions.
    """

    # operation: Literal["read", "write"]
    # scope: Literal["files", "disk_storage"]

    def __init__(self, operation, scope):
        self.operation = operation
        self.scope = scope

    @staticmethod
    def from_string(string: str):
        # Example: "write: disk_storage"

        operation, scope = [x.strip() for x in string.split(":")]

        instance = Permission(operation, scope)

        # TODO add validation

        return instance

    def __eq__(self, other):
        is_equal = self.operation == other.operation and self.scope == other.scope

        return is_equal

    def __str__(self) -> str:
        return f"{self.operation}: {self.scope}"
