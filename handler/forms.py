import json

from django import forms


class OAuthLoginForm(forms.Form):
    resource_id = forms.CharField(label="Divar Post Token To", max_length=100)


class OAuthGetPhoneForm(forms.Form):
    pass


class OAuthCreateApprovedAddonForm(forms.Form):
    widgets = forms.JSONField(label="addon widgets to use for approved token", encoder=json.JSONEncoder,
                              decoder=json.JSONDecoder)
