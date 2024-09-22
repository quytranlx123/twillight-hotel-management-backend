# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    last_login = models.DateTimeField(auto_now=True, editable=False)
    is_customer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    account_updated = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True, editable=False)
    def __str__(self):
        return f"Account: {self.username}"
