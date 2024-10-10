# users/views.py
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from Hotel_Management import settings
from rest_framework import viewsets
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import Permission
from rest_framework import generics


class UsersViewSet(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)


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
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        return response


class Login(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = CustomUser.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'id': user.id,
            'jwt': token,
            'role': user.role
        }
        return response


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


class PermissionViewSet(RoomAuthenticationMixin,viewsets.ViewSet):
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
