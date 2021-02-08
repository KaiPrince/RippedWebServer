"""
 * Project Name: RippedWebServer
 * File Name: permissions.py
 * Programmer: Kai Prince
 * Date: Mon, Dec 07, 2020
 * Description: This file contains a module which knows which permissions the
 *  user currently has.
"""

from auth.application.interfaces.permissions_reader import IPermissionsReader
from auth.domain.auth_ticket import AuthTicket


class JWTPermissionsReader(IPermissionsReader):
    """
    * Class Name: JWTPermissionsReader
    * Purpose: This purpose of this class is to determine effective
    *  permissions using a JSON Web Token.
    """

    def __init__(self, auth_ticket: AuthTicket):
        self._auth_ticket = auth_ticket
        self._permissions = self._get_permissions(auth_ticket)

    def may_delete(self, resource):
        has_write_files_permission = any(
            x.operation == "write" and x.scope == "files" for x in self._permissions
        )
        has_write_disk_storage_permission = any(
            x.operation == "write" and x.scope == "disk_storage"
            for x in self._permissions
        )

        is_user_token = self._auth_ticket.audience != "public"
        is_resource_in_scope = is_user_token or self._auth_ticket.subject == resource

        return (
            has_write_files_permission
            and has_write_disk_storage_permission
            and is_resource_in_scope
        )

    def may_share(self, resource):
        is_user_token = self._auth_ticket.audience != "public"
        has_read_files_permission = any(
            x.operation == "read" and x.scope == "files" for x in self._permissions
        )

        return is_user_token and has_read_files_permission

    def _get_permissions(self, auth_ticket: AuthTicket):
        return auth_ticket.permissions


def make_jwt_permissions_reader(claims: dict):
    auth_ticket = AuthTicket.from_claims(claims)

    return JWTPermissionsReader(auth_ticket)
