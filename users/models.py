from django.utils.timezone import now
from rest_framework.authtoken.models import Token
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomToken(Token):
    expires_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = now() + timedelta(days=30)
        return super().save(*args, **kwargs)

    def is_expired(self):
        return self.expires_at and now() > self.expires_at



