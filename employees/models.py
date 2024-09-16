import hashlib
from django.db import models
from users.models import CustomUser


class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee_profile')
    avatar = models.ImageField(upload_to='uploads/%Y/%m/%d', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    hire_date = models.DateField(null=True, blank=True)
    identity_card_number = models.CharField(max_length=64, unique=True, editable=True)

    def set_identity_card_number(self, identity_card_number):
        # Băm CCCD bằng SHA-256
        self.identity_card_number = hashlib.sha256(identity_card_number.encode('utf-8')).hexdigest()

    def save(self, *args, **kwargs):
        # Kiểm tra nếu không có identity_card_number thì mới lưu
        if not self.identity_card_number or self.identity_card_number == 'UNKNOWN':
            raise ValueError("Bạn phải cung cấp số CCCD thông qua phương thức set_identity_card_number() trước khi lưu.")
        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return f"Employee: {CustomUser.username}"
