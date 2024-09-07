# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    account_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Account: {self.username}"
