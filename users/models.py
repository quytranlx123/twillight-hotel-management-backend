# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords


class CustomUser(AbstractUser):
    is_superuser = models.BooleanField(default=False, verbose_name='is_superuser')
    email = models.EmailField(unique=True)
    last_login = models.DateTimeField(auto_now=True)
    is_customer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    account_updated = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True, editable=False)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.username}"
