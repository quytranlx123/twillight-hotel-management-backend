# customer_accounts/models.py

from django.db import models
from customers.models import Customer

class CustomerAccount(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    account_created = models.DateTimeField(auto_now_add=True)
    account_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Account for {self.customer}"
