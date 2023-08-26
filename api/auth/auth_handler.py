import time

import jwt

from data.config import JWT_SECRET, JWT_ALGORITHM


def sign_jwt(team_id: int, admin: bool = False) -> str:
    payload = {
        "team_id": team_id,
        "expires": time.time() + 86400
    }
    if admin:
        payload["admin"] = admin
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token


def decode_jwt(token: str):
    """
    :param token: jwt token
    :return:
    :rtype: None | dict
    """
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except:
        return None
    return decoded_token if decoded_token["expires"] >= time.time() else None
