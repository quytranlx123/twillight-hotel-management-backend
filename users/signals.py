from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver
from .models import CustomUser
from django.db.models.signals import pre_save


@receiver(pre_save, sender=CustomUser)
def hash_user_password(sender, instance, **kwargs):
    # Băm mật khẩu trước khi lưu
    if instance.password and not instance.password.startswith('pbkdf2_sha256$'):
        instance.password = make_password(instance.password)


@receiver(user_logged_in)
def update_last_login(sender, request, user, **kwargs):
    user.last_login = timezone.now()
    user.save()
