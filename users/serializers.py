from django.db import transaction
from rest_framework import serializers

from customers.models import Customer
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'role', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])  # Mã hóa mật khẩu
        Customer.objects.create(user=user)
        user.save()
        return user  # Đảm bảo trả về đối tượng người dùng đã tạo


class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'role', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}


    @transaction.atomic  # Đảm bảo rằng tất cả các thao tác đều thành công hoặc không có gì được lưu
    def create(self, validated_data):
        # Tạo đối tượng user
        user = CustomUser.objects.create(**validated_data)

        # Kiểm tra xem customer đã tồn tại hay chưa
        customer, created = Customer.objects.get_or_create(user=user)

        # Cập nhật trường customer_id trong user
        user.customer = customer
        user.save()  # Lưu lại user với customer_id

        return user