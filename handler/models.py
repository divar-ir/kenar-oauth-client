from django.db import models

class Oauth(models.Model):
    access_token = models.CharField(max_length=128)
    refresh_token = models.CharField(max_length=256)
    expires = models.DateTimeField()
    phone = models.CharField(max_length=11)
    session_id = models.CharField(max_length=128, unique=True)

    def approved_addon_token(self) -> str:
        try:
            scope = self.scope_set.get(permission_type='ADDON_USER_APPROVED')
        except self.DoesNotExist:
            raise Exception("oauth does not have user approved scope")

        return scope.resource_id

    def has_phone_number_scope(self):
        if not self.scope_set.filter(permission_type='USER_PHONE').exists():
            raise Exception("oauth does not have user phone scope")


class Scope(models.Model):
    PERMISSION_CHOICES = [
        ('ADDON_USER_APPROVED', 'ADDON_USER_APPROVED'),
        ('USER_PHONE', 'USER_PHONE'),
    ]
    permission_type = models.CharField(max_length=100, choices=PERMISSION_CHOICES)
    resource_id = models.CharField(max_length=100, null=True)
    oauth = models.ForeignKey(Oauth, on_delete=models.CASCADE)
