from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'avatar': {'required': False},
            'phone_number': {'required': False},
            'address': {'required': False},
            'date_of_birth': {'required': False, 'allow_null': True},
            'identity_card_number': {'required': False},
        }

    def update(self, instance, validated_data):
        # Lưu avatar nếu có sự thay đổi
        avatar = validated_data.get('avatar', None)

        # Nếu không có avatar mới, loại bỏ avatar khỏi validated_data
        if avatar is None:
            validated_data.pop('avatar', None)

        # Cập nhật các trường khác
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Lưu đối tượng
        instance.save()
        return instance
