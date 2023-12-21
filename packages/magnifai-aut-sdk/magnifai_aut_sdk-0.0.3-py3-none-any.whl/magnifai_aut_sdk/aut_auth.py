import time
from datetime import datetime

import requests

from magnifai_aut_sdk.aut_properties import AutProperties, Property


class AutAuth:
    accessTokenExpirationTimestamp = 0
    refreshTokenExpirationTimestamp = 0
    accessToken = None
    tokenUser = ""
    refreshToken = None
    ENDPOINT = "/realms/aut/protocol/openid-connect/token"
    CLIENT_ID = "aut-magnifai-aut-magnifai_aut_sdk-python"
    PASSWORD_GRANT_TYPE = "password"
    REFRESH_TOKEN_GRANT_TYPE = "refresh_token"

    def __init__(self):
        raise ValueError("Utility class")

    @classmethod
    def is_token_expired(cls, expiration_time):
        now = int(time.mktime(datetime.now().timetuple()) * 1000)
        return now > expiration_time - cls.get_threshold_millis()

    @classmethod
    def get_threshold_millis(cls):
        return int(AutProperties.get_property(Property.AUTH_TOKEN_THRESHOLD_SECONDS)) * 1000

    @classmethod
    def get_token(cls):
        if cls.tokenUser != AutProperties.get_property(Property.AUTH_USER):
            return cls.req_token()
        elif not cls.is_token_expired(cls.accessTokenExpirationTimestamp):
            return cls.accessToken
        elif not cls.is_token_expired(cls.refreshTokenExpirationTimestamp):
            return cls.refreshToken()
        else:
            return cls.req_token()

    @classmethod
    def req_token(cls):
        response = requests.post(
            f"{AutProperties.get_property(Property.MAGNIFAI_AUTH_HOST)}{cls.ENDPOINT}",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_id": cls.CLIENT_ID,
                "username": AutProperties.get_property(Property.AUTH_USER),
                "password": AutProperties.get_property(Property.AUTH_PASSWORD),
                "grant_type": cls.PASSWORD_GRANT_TYPE
            }
        )
        cls.assign_values(response)
        cls.tokenUser = AutProperties.get_property(Property.AUTH_USER)
        return cls.accessToken

    @classmethod
    def refresh_token(cls):
        response = cls.token_endpoint_specification().post(
            data={
                "refresh_token": cls.refreshToken,
                "grant_type": cls.REFRESH_TOKEN_GRANT_TYPE
            }
        )
        cls.assign_values(response)
        return cls.accessToken

    @classmethod
    def token_endpoint_specification(cls):
        port = int(AutProperties.get_property(Property.AUTH_PORT) if AutProperties.get_property(
            Property.AUTH_PORT) else AutProperties.get_property(
            Property.MAGNIFAI_PORT))
        return requests.Session().post(
            f"{AutProperties.get_property(Property.MAGNIFAI_HOST)}{cls.ENDPOINT}",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_id": cls.CLIENT_ID
            }
        )

    @classmethod
    def assign_values(cls, response):
        now = int(time.mktime(datetime.now().timetuple()) * 1000)
        data = response.json()
        cls.accessToken = data["access_token"]
        cls.refreshToken = data["refresh_token"]
        cls.accessTokenExpirationTimestamp = now + data["expires_in"] * 1000
        cls.refreshTokenExpirationTimestamp = now + data["refresh_expires_in"] * 1000
