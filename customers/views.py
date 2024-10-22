from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError

from .models import Customer
from .serializers import CustomerSerializer


class CustomerProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Trả về đối tượng Customer gắn với người dùng hiện tại
        return Customer.objects.filter(user=self.request.user)

    def get_object(self):
        # Lấy đối tượng Customer gắn với người dùng hiện tại
        return self.request.user.customer


class UpdateCustomerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        customer = getattr(self.request.user, 'customer', None)
        if customer is None:
            raise PermissionDenied("User does not have an associated customer.")
        return Customer.objects.filter(id=customer.id)

    def perform_update(self, serializer):
        try:
            customer = serializer.save()

            # Xử lý avatar
            avatar_file = self.request.FILES.get('avatar')
            if avatar_file:
                customer.avatar.save(avatar_file.name, avatar_file)
                customer.save()

            # Tạo URL cho avatar
            avatar_url = customer.avatar.url if customer.avatar else None

            return Response({
                'detail': 'Cập nhật dữ liệu thành công!',
                'customer': CustomerSerializer(customer).data,
                'avatar': avatar_url  # Trả về URL của avatar
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def handle_exception(self, exc):

        return super().handle_exception(exc)
