import json
import random
from datetime import datetime

import pytz
import requests
from django.http import JsonResponse
from django.shortcuts import redirect, render
from oauthlib.oauth2.rfc6749.clients import WebApplicationClient

from handler.forms import OAuthLoginForm
from handler.models import Oauth, Scope
from handler.oauth_configs import OAUTH_CLIENT_ID, OAUTH_AUTHORIZATION_URL, OAUTH_REDIRECT_URI, OAUTH_CLIENT_SECRET, \
    OAUTH_TOKEN_URL, OAUTH_INFO_SESSION_KEY, GET_USER_URL

client = WebApplicationClient(client_id=OAUTH_CLIENT_ID)


def oauth_login_form(request):
    if request.method == "POST":
        form = OAuthLoginForm(request.POST)
        if form.is_valid():
            resource_id = form.cleaned_data["resource_id"]
            return redirect("oauth_login", resource_id=resource_id)
    else:
        form = OAuthLoginForm()

    return render(request, "get_token_form.html", {"form": form})


def oauth_login(request, resource_id):
    scope = [f'ADDON_USER_APPROVED__{resource_id}', 'USER_PHONE']
    state = random.randint(1000, 9999)
    url = client.prepare_request_uri(
        OAUTH_AUTHORIZATION_URL,
        redirect_uri=OAUTH_REDIRECT_URI,
        scope=scope,
        state=state
    )
    request.session[OAUTH_INFO_SESSION_KEY] = {"state": str(state), "scope": scope}
    return redirect(url)


def oauth_callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")
    state_in_session, scope = request.session.get(OAUTH_INFO_SESSION_KEY)["state"], \
                              request.session.get(OAUTH_INFO_SESSION_KEY)["scope"]
    if not code or state != state_in_session:
        return JsonResponse({"status": "access denied"})
    data = dict(
        code=code,
        redirect_uri=OAUTH_REDIRECT_URI,
        client_id=OAUTH_CLIENT_ID,
        client_secret=OAUTH_CLIENT_SECRET,
        grant_type='authorization_code',
    )
    response = requests.post(
        OAUTH_TOKEN_URL,
        json=data,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )
    token = client.parse_request_body_response(response.text)
    access_token, refresh_token, expires = token['access_token'], token['refresh_token'], token['expires']
    oauth = Oauth.objects.create(
        access_token=access_token,
        refresh_token=refresh_token,
        expires=datetime.fromtimestamp(int(expires)).replace(tzinfo=pytz.utc)
    )
    for s in scope:
        permission_resource_tup = s.split('__')
        Scope.objects.create(
            permission_type=permission_resource_tup[0],
            resource_id=permission_resource_tup[1] if len(permission_resource_tup) > 1 else None,
            oauth=oauth
        )
    response = requests.post(
        GET_USER_URL,
        json={},
        headers={
            "Content-Type": "application/json; charset=utf-8",
            'x-api-key': OAUTH_CLIENT_SECRET,
            'x-access-token': access_token
        }
    )
    return render(request, 'access_success.html', {'user_phone': json.loads(response.content)["phone_numbers"]})
