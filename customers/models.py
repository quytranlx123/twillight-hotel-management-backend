# customers/models.py
import hashlib
from django.db import models
from users.models import CustomUser


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='uploads/%Y/%m/%d', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    identity_card_number = models.CharField(max_length=64, unique=True, editable=True)

    def set_identity_card_number(self, identity_card_number):
        # Băm CCCD bằng SHA-256
        self.identity_card_number = hashlib.sha256(identity_card_number.encode('utf-8')).hexdigest()

    def save(self, *args, **kwargs):
        # Kiểm tra nếu không có identity_card_number thì mới lưu
        if not self.identity_card_number or self.identity_card_number == 'UNKNOWN':
            raise ValueError("Bạn phải cung cấp số CCCD thông qua phương thức set_identity_card_number() trước khi lưu.")
        super(Customer, self).save(*args, **kwargs)


class Guest(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{CustomUser.username}"

