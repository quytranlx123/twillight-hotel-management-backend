# middleware.py
import jwt
from django.conf import settings
from users.models import CustomUser  # Đảm bảo import CustomUser
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Bỏ qua middleware cho admin
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        token = request.COOKIES.get('jwt')
        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user = CustomUser.objects.get(id=payload['id'])
                request.user = user
            except (jwt.ExpiredSignatureError, jwt.DecodeError, CustomUser.DoesNotExist):
                request.user = None
        else:
            request.user = None

        return self.get_response(request)

