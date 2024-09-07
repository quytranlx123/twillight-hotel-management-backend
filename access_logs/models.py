# access_logs/models.py
from django.db import models
from accounts.models import CustomUser


class AccessLog(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    access_time = models.DateTimeField(auto_now_add=True)
    action = models.TextField()

    def __str__(self):
        return f"AccessLog {self.id} by {self.user}"