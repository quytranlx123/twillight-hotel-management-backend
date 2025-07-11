from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import BaseUserManager

from customers.models import Customer


class CustomUserManager(BaseUserManager):
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  # Đặt role mặc định là admin

        return self._create_user(username, email, password, **extra_fields)

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        # Giữ giá trị role không đổi nếu không được truyền vào
        return self._create_user(username, email, password, **extra_fields)

    def _create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('customer', 'Customer'),
        ('employee', 'Employee'),
    ]
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    last_login = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    account_updated = models.DateTimeField(auto_now_add=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='customer', null=True, blank=True)
    objects = CustomUserManager()

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Thay đổi tên này cho phù hợp
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Thay đổi tên này cho phù hợp
        blank=True,
    )

    def __str__(self):
        return self.username


class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Kiểm tra xem OTP có còn hợp lệ không (ví dụ: trong 5 phút)
        return (timezone.now() - self.created_at).total_seconds() < 300  # 5 phút
