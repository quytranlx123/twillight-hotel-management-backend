# external_integrations/models.py

from django.db import models

class ExternalIntegration(models.Model):
    name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
