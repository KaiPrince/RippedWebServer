"""
 * Project Name: RippedWebServer
 * File Name: user_profile.py
 * Programmer: Kai Prince
 * Date: Sat, Feb 06, 2021
 * Description: This file contains the UserProfile entity.
"""


class UserProfile:
    id: str
    username: str

    def __init__(self, id, username) -> None:
        self.id = id
        self.username = username

    @staticmethod
    def from_jwt(dict: dict):

        (id, username,) = [
            dict.get(x)
            for x in [
                "sub",
                "name",
            ]
        ]

        return UserProfile(id, username)

    @staticmethod
    def from_dict(dict: dict):

        (id, username,) = [
            dict.get(x)
            for x in [
                "id",
                "username",
            ]
        ]

        return UserProfile(id, username)

    def to_dict(self):
        return {"username": self.username, "id": self.id}
