from django.db import models
from customers.models import Customer
from employees.models import Employee


class CustomerInteraction(models.Model):
    interaction_id = models.AutoField(primary_key=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='interactions')
    interaction_date = models.DateField()
    interaction_type = models.CharField(max_length=50, choices=[
        ('phone_call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('chat', 'Chat'),
        ('other', 'Other')
    ])
    notes = models.TextField(blank=True, null=True)
    created_by = models.OneToOneField(Employee, on_delete=models.SET_NULL, null=True, related_name='created_interactions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Interaction {self.interaction_id} - {self.Customer.user}"
