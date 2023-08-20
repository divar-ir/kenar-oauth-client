import random
import re

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from oauthlib.oauth2.rfc6749.clients import WebApplicationClient

from handler import oauth_client
from handler.forms import OAuthLoginForm, OAuthGetPhoneForm, OAuthCreateApprovedAddonForm
from handler.models import Oauth, Scope

client = WebApplicationClient(client_id=settings.OAUTH_CLIENT_ID)

scope_regex = re.compile(r"^(?P<permission_type>([A-Z]+_)*([A-Z]+))(__(?P<resource_id>.+))?$")


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
    scopes = [f'ADDON_USER_APPROVED__{resource_id}', 'USER_PHONE']
    state = random.randint(1000, 9999)

    oauth_url = client.prepare_request_uri(
        settings.OAUTH_AUTHORIZATION_URL,
        redirect_uri=settings.OAUTH_REDIRECT_URI,
        scope=scopes,
        state=state
    )

    request.session[settings.OAUTH_INFO_SESSION_KEY] = {"state": str(state), "scopes": scopes}
    return redirect(oauth_url)


def oauth_callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")
    state_in_session, scopes = request.session.get(settings.OAUTH_INFO_SESSION_KEY)["state"], \
        request.session.get(settings.OAUTH_INFO_SESSION_KEY)["scopes"]
    if not code or state != state_in_session:
        return JsonResponse({"status": "access denied"})

    if Oauth.objects.filter(session_id=request.session.session_key).exists():
        Oauth.objects.get(session_id=request.session.session_key).delete()

    oauth = oauth_client.create(code=code, session_id=request.session.session_key)
    oauth.save()

    scopes_permissions = []
    for s in scopes:
        scope_match_groups = scope_regex.search(s).groupdict()
        scopes_permissions.append(scope_match_groups['permission_type'])

        Scope.objects.create(
            permission_type=scope_match_groups['permission_type'],
            resource_id=scope_match_groups.setdefault('resource_id', None),
            oauth=oauth
        )

    return render(
        request,
        'access_success.html',
        {
            'permissions': scopes_permissions,
            'get_phone_form': OAuthGetPhoneForm(),
            'create_approved_addon_form': OAuthCreateApprovedAddonForm()
        }
    )


def oauth_get_phone(request):
    form = OAuthGetPhoneForm(request.POST)
    if not form.is_valid():
        raise Exception("invalid input")

    oauth = Oauth.objects.get(session_id=request.session.session_key)
    oauth.has_phone_number_scope()
    phone = oauth_client.get_phone_numbers(oauth.access_token)

    return render(
        request,
        'phone_number.html',
        {
            'phone_number': phone[0]
        }
    )


def oauth_approved_addon(request, token):
    return render(
        request,
        'approved_addon.html',
        {
            'token': token,
        }
    )


def oauth_create_approved_addon_form(request):
    if request.method == "POST":
        form = OAuthCreateApprovedAddonForm(request.POST)
        if form.is_valid():
            widgets = form.cleaned_data["widgets"]
        else:
            raise Exception("invalid input")

        oauth = Oauth.objects.get(session_id=request.session.session_key)
        token = oauth.approved_addon_token()
        oauth_client.create_approved_addon(oauth.access_token, widgets, token)

        return redirect('oauth_approved_addon', token=token)
    else:
        return render(
            request,
            'approved_addon_form.html',
            {
                'form': OAuthCreateApprovedAddonForm(),
            }
        )

