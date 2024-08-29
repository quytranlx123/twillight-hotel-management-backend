# customer_support/models.py

from django.db import models
from customers.models import Customer

class SupportTicket(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Ticket {self.id} by {self.customer}"
