# roles/models.py

from django.db import models

class Role(models.Model):
    role_name = models.CharField(max_length=50)

    def __str__(self):
        return self.role_name

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission_name = models.CharField(max_length=50)

    def __str__(self):
        return f"Permission {self.permission_name} for Role {self.role.role_name}"
