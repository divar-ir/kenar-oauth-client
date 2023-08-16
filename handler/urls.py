from django.urls import path

from handler.views import oauth_callback, oauth_login_form, oauth_login

urlpatterns = [
    path("form/", oauth_login_form, name="oauth_login_form"),
    path("login/<str:resource_id>", oauth_login, name="oauth_login"),
    path("callback", oauth_callback, name="oauth_callback"),
]
