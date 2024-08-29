# assets/models.py

from django.db import models

class Asset(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    purchase_date = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Maintenance(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    description = models.TextField()
    maintenance_date = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Maintenance {self.id} for Asset {self.asset.name}"
