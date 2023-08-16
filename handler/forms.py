from django import forms


class OAuthLoginForm(forms.Form):
    resource_id = forms.CharField(label="Divar Post Token To", max_length=100)
