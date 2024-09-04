# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='uploads/%Y/%m/%d', blank=True, null=True)
    is_customer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    account_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Account: {self.username}"
