from django.urls import path

from handler.views import oauth_callback, oauth_login_form, oauth_login, oauth_get_phone, oauth_approved_addon, \
    oauth_create_approved_addon_form

urlpatterns = [
    path("form/", oauth_login_form, name="oauth_login_form"),
    path("login/<str:resource_id>", oauth_login, name="oauth_login"),
    path("callback", oauth_callback, name="oauth_callback"),
    path("get-phone", oauth_get_phone, name="oauth_get_phone"),
    path("approved-addon/<str:token>", oauth_approved_addon, name="oauth_approved_addon"),
    path("approved-addon-form", oauth_create_approved_addon_form, name="oauth_approved_addon_form"),
]
