"""
 * Project Name: RippedWebServer
 * File Name: _session_controller.py
 * Programmer: Kai Prince
 * Date: Mon, Feb 08, 2021
 * Description: This file contains operations on the session.
"""
from typing import Optional

from auth.application.models.auth_ticket_jwt import AuthTicketJwt
from auth.application.port.outbound.session import Session
from auth.domain.auth_ticket import AuthTicket
from auth.domain.user_profile import UserProfile


class SessionController:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_auth_ticket(self) -> Optional[AuthTicket]:
        auth_ticket = self.session.get("auth_token_data")  # auth_ticket
        return AuthTicket.from_claims(auth_ticket) if auth_ticket else None

    def get_auth_token(self) -> Optional[AuthTicketJwt]:
        auth_token = self.session.get("auth_token")
        return AuthTicketJwt(auth_token) if auth_token else None

    def get_user_profile(self) -> Optional[UserProfile]:
        user_profile = self.session.get("user")
        return UserProfile.from_dict(user_profile) if user_profile else None

    def clear(self):
        self.session.clear()

    def save_auth_ticket(self, auth_ticket: Optional[AuthTicket]):
        serialized: dict = auth_ticket.to_jwt() if auth_ticket else None

        self.session.set("auth_token_data", serialized)  # auth_ticket

    def save_auth_token(self, auth_token: Optional[AuthTicketJwt]):
        serialized: str = auth_token.get_encoded_jwt() if auth_token else None
        self.session.set("auth_token", serialized)

    def save_user_profile(self, user_profile: Optional[UserProfile]):
        serialized: dict = user_profile.to_dict() if user_profile else None
        self.session.set("user", serialized)
