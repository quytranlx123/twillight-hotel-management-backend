# users/views.py
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from Hotel_Management import settings
from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Permission
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client
import random
import string

from customers.models import Customer
from customers.serializers import CustomerSerializer
from .models import CustomUser, OTP
from .serializers import CustomUserSerializer, CustomerRegisterSerializer
from django.conf import settings


class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class UsersViewSet(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class RoomAuthenticationMixin:
    def authenticate(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            role = payload.get('role')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.DecodeError:
            raise AuthenticationFailed('Invalid token')

        return role


class Register(APIView):
    def generate_otp(self, length=6):
        return ''.join(random.choices(string.digits, k=length))

    def send_sms(self, to_phone_number, message):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            to=to_phone_number,
            from_=settings.TWILIO_PHONE_NUMBER,
            body=message
        )

    @csrf_exempt
    def post(self, request):
        phone_number = request.data.get('phone_number')

        # Kiểm tra xem số điện thoại đã tồn tại chưa
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            return Response({'error': 'Phone number already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo OTP và lưu vào cơ sở dữ liệu
        otp = self.generate_otp()
        OTP.objects.create(phone_number=phone_number, otp=otp)

        message = f'Your OTP code is: {otp}'
        # Gửi OTP qua SMS
        self.send_sms(phone_number, message)

        return Response({'message': 'OTP has been sent to your phone.'}, status=status.HTTP_200_OK)


class VerifyOTP(APIView):
    def post(self, request):
        otp = request.data.get('otp')
        phone_number = request.data.get('phone_number')

        try:
            otp_record = OTP.objects.get(phone_number=phone_number, otp=otp)
            if (timezone.now() - otp_record.created_at).total_seconds() > 300:  # OTP hợp lệ trong 5 phút
                return Response({'error': 'OTP has expired.'}, status=status.HTTP_400_BAD_REQUEST)

            # Nếu OTP hợp lệ, tạo user
            user_data = {
                'username': request.data.get('username'),
                'phone_number': phone_number,
                'password': request.data.get('password'),
                'email': request.data.get('email'),
                'role': request.data.get('role')
            }
            user_serializer = CustomerRegisterSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()  # Tạo user và tự động tạo customer nếu cần

            # Xóa OTP sau khi xác thực thành công
            otp_record.delete()

            return Response({
                'user': user_serializer.data,
                'customer': {'user': user.customer.id}  # Hoặc lấy thông tin customer nếu cần
            }, status=status.HTTP_201_CREATED)

        except OTP.DoesNotExist:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ForgotPassword(APIView):
    def generate_otp(self, length=6):
        return ''.join(random.choices(string.digits, k=length))

    def send_sms(self, to_phone_number, message):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            to=to_phone_number,
            from_=settings.TWILIO_PHONE_NUMBER,
            body=message
        )

    @csrf_exempt
    def post(self, request):
        phone_number = request.data.get('phone_number')

        # Kiểm tra xem số điện thoại có tồn tại không
        if not CustomUser.objects.filter(phone_number=phone_number).exists():
            return Response({'error': 'Phone number does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo OTP và lưu vào cơ sở dữ liệu
        otp = self.generate_otp()
        OTP.objects.create(phone_number=phone_number, otp=otp)

        message = f'Your OTP code is: {otp}'
        # Gửi OTP qua SMS
        self.send_sms(phone_number, message)

        return Response({'message': 'OTP has been sent to your phone.'}, status=status.HTTP_200_OK)


class ResetPassword(APIView):
    def post(self, request):
        otp = request.data.get('otp')
        phone_number = request.data.get('phone_number')
        new_password = request.data.get('new_password')

        try:
            # Kiểm tra OTP có tồn tại không
            otp_record = OTP.objects.get(phone_number=phone_number, otp=otp)
            if (timezone.now() - otp_record.created_at).total_seconds() > 300:  # OTP hợp lệ trong 5 phút
                return Response({'error': 'OTP has expired.'}, status=status.HTTP_400_BAD_REQUEST)

            # Lấy người dùng bằng số điện thoại
            user = CustomUser.objects.get(phone_number=phone_number)
            # Đặt lại mật khẩu
            user.set_password(new_password)
            user.save()

            # Xóa bản ghi OTP sau khi xác thực thành công (tuỳ chọn)
            otp_record.delete()

            return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
        except OTP.DoesNotExist:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)


# xem session
class CheckSession(APIView):
    def get(self, request):
        otp = request.session.get('otp')
        phone_number = request.session.get('phone_number')
        return Response({'otp': otp, 'phone_number': phone_number}, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Lấy thông tin token
        tokens = serializer.validated_data
        user = CustomUser.objects.get(username=request.data['username'])

        # Thêm role vào phản hồi
        tokens['role'] = user.role

        return Response(tokens, status=status.HTTP_200_OK)


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')
        if token is None:
            return AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.ExpiredSignatureError:
            return AuthenticationFailed('Unauthenticated')

        user = CustomUser.objects.filter(id=payload['id']).first()
        serializer = CustomUserSerializer(user)

        return Response(serializer.data)


class Logout(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Successfully logged out'
        }
        return response


class CustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]


class PermissionViewSet(RoomAuthenticationMixin, viewsets.ViewSet):
    def assign_permission(self, request, user_id, permission_codename):
        # Kiểm tra người dùng
        user = get_object_or_404(CustomUser, id=user_id)
        role = self.authenticate(self.request)
        if role not in ['admin', 'manager']:
            raise AuthenticationFailed('Permission denied')
        # Kiểm tra quyền
        try:
            permission = Permission.objects.get(codename=permission_codename)
        except Permission.DoesNotExist:
            return Response({'error': 'Permission not found'}, status=status.HTTP_404_NOT_FOUND)

        user.user_permissions.add(permission)
        return Response({'status': 'permission assigned'}, status=status.HTTP_200_OK)

    def revoke_permission(self, request, user_id, permission_codename):
        # Kiểm tra người dùng
        user = get_object_or_404(CustomUser, id=user_id)

        # Kiểm tra quyền
        try:
            permission = Permission.objects.get(codename=permission_codename)
        except Permission.DoesNotExist:
            return Response({'error': 'Permission not found'}, status=status.HTTP_404_NOT_FOUND)

        user.user_permissions.remove(permission)
        return Response({'status': 'permission revoked'}, status=status.HTTP_200_OK)

    def list_user_permissions(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        role = self.authenticate(self.request)
        if role not in ['admin', 'manager']:
            raise AuthenticationFailed('Permission denied')
        # Kiểm tra người dùng
        permissions = user.user_permissions.all()
        return Response({'permissions': [perm.codename for perm in permissions]}, status=status.HTTP_200_OK)


class UserAppsPermissionsView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_permissions = user.user_permissions.all()

        # Tạo danh sách các ứng dụng và quyền
        apps_permissions = {}

        for permission in user_permissions:
            app_label = permission.content_type.app_label

            # Khởi tạo danh sách quyền cho từng ứng dụng
            if app_label not in apps_permissions:
                apps_permissions[app_label] = []

            apps_permissions[app_label].append(permission.codename)

        return Response(apps_permissions)
