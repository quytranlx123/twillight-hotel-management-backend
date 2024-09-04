# notifications/models.py

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('email', 'Email'),
        ('SMS', 'SMS'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    sent_date = models.DateField()

    def __str__(self):
        return f"Notification {self.id} to {self.user}"
