from requests.auth import AuthBase


class JWTAuth(AuthBase):
    """
    * Class Name: JWTAuth
    * Purpose: This purpose of this class is to inject an auth token into request
    *   headers.
    """

    def __init__(self, auth_token):
        # setup any auth-related data here
        self._auth_token = auth_token

    def __call__(self, r):
        # modify and return the request
        r.headers["Authorization"] = self._auth_token
        return r


def get_auth_middleware(auth_token: str) -> AuthBase:
    return JWTAuth(auth_token)
