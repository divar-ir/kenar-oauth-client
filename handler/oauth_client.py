from datetime import datetime
from typing import List

from django.conf import settings
from django.utils import timezone
from oauthlib.oauth2 import WebApplicationClient

from handler import requests
from handler.models import Oauth

client = WebApplicationClient(client_id=settings.OAUTH_CLIENT_ID)


def create(code, session_id, *args, **kwargs) -> Oauth:
    data = dict(
        code=code,
        client_id=settings.OAUTH_CLIENT_ID,
        client_secret=settings.OAUTH_CLIENT_SECRET,
        grant_type='authorization_code',
    )
    response = requests.post(
        settings.OAUTH_TOKEN_URL,
        json=data,
    )
    token = client.parse_request_body_response(response.text)

    access_token, refresh_token = token['access_token'], token['refresh_token']
    expires = datetime.fromtimestamp(int(token['expires']), timezone.utc)

    return Oauth(access_token=access_token, refresh_token=refresh_token,
                 expires=expires, session_id=session_id, *args, **kwargs)


def create_approved_addon(access_token, widgets, token):
    resp = requests.post(
        settings.CREATE_ADDON_ENDPOINT.format(token=token),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            'x-api-key': settings.OAUTH_CLIENT_SECRET,
            'x-access-token': access_token
        },
        json=widgets,
    )

    if resp.status_code != 200:
        raise Exception("could not create approved addon", resp.status_code, resp.content)


def get_phone_numbers(access_token) -> List[str]:
    resp = requests.post(
        settings.GET_USER_ENDPOINT,
        json={},
        headers={
            "Content-Type": "application/json; charset=utf-8",
            'x-api-key': settings.OAUTH_CLIENT_SECRET,
            'x-access-token': access_token
        }
    )
    if resp.status_code != 200:
        raise Exception("could not get phone number", resp.status_code, resp.content)

    return resp.json().get("phone_numbers")
