# customer_interactions/models.py

from django.db import models
from customers.models import Customer

class CustomerInteraction(models.Model):
    INTERACTION_TYPE_CHOICES = [
        ('email', 'Email'),
        ('phone call', 'Phone Call'),
        # Thêm các loại tương tác khác nếu cần
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    interaction_date = models.DateField()
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPE_CHOICES)
    notes = models.TextField()

    def __str__(self):
        return f"Interaction {self.id} with {self.customer}"
