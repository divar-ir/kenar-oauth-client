from django.db import models


class Oauth(models.Model):
    access_token = models.CharField(max_length=128)
    refresh_token = models.CharField(max_length=256)
    expires = models.DateTimeField()
    phone = models.CharField(max_length=11)


class Scope(models.Model):
    PERMISSION_CHOICES = [
        ('ADDON_USER_APPROVED', 'ADDON_USER_APPROVED'),
        ('USER_PHONE', 'USER_PHONE'),
    ]
    permission_type = models.CharField(max_length=100, choices=PERMISSION_CHOICES)
    resource_id = models.CharField(max_length=100, null=True)
    oauth = models.ForeignKey(Oauth, on_delete=models.CASCADE)
