# activity_logs/models.py
from django.db import models
from users.models import CustomUser


class ActivityLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    os = models.CharField(max_length=100)
    path = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
