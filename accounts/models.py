from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    trial_started_at = models.DateTimeField(null=True, blank=True)
    trial_end = models.BooleanField(default=False)
