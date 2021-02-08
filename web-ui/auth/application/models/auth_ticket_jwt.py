"""
 * Project Name: RippedWebServer
 * File Name: auth_ticket_jwt.py
 * Programmer: Kai Prince
 * Date: Sun, Feb 07, 2021
 * Description: This file contains the DTO for an Auth Token with a JWT.
"""

from typing import Union
from authlib.jose import JsonWebToken
from auth.domain.auth_ticket import AuthTicket
from auth.adapter.inbound.jwt.decode import get_payload_from_auth_token


class AuthTicketJwt(AuthTicket):
    ticket: AuthTicket
    encoded_jwt: JsonWebToken

    # TODO: call super init
    def __init__(self, encoded_jwt: Union[JsonWebToken, str]) -> None:
        self.encoded_jwt = encoded_jwt

        decoded_jwt = get_payload_from_auth_token(encoded_jwt)
        self.ticket = AuthTicket.from_jwt(decoded_jwt)

    def to_jwt(self):
        return self.ticket.to_jwt()

    def get_encoded_jwt(self):
        return str(self.encoded_jwt)
