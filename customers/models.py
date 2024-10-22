# customers/models.py
import hashlib
import os

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models


def avatar_upload_to(instance, filename):
    # Lấy tên người dùng từ instance.user
    username = instance.user.username
    # Tạo tên tệp mới với tên người dùng và giữ lại phần mở rộng
    base, extension = os.path.splitext(filename)
    new_filename = f"{username}{extension}"
    return f'uploads/avatars/customer/{new_filename}'


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_profile')
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(
        upload_to=avatar_upload_to,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'svg'])]
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    identity_card_number = models.CharField(max_length=64, unique=True, editable=True, blank=True, null=True)

    def set_identity_card_number(self, identity_card_number):
        self.identity_card_number = hashlib.sha256(identity_card_number.encode('utf-8')).hexdigest()

    def save(self, *args, **kwargs):
        # Nếu không có tệp mới thì không thay đổi avatar
        if not self.pk or (self.avatar and self.avatar.name != self.__class__.objects.get(pk=self.pk).avatar.name):
            super(Customer, self).save(*args, **kwargs)
        elif not self.avatar:  # Nếu avatar không có thì cũng cập nhật
            super(Customer, self).save(*args, **kwargs)


class Guest(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

