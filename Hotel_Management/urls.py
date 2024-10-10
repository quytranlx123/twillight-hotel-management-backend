from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static

from Hotel_Management import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Hotel Management API",
        default_version='v1',
        description="APIs for Hotel Management", contact=openapi.Contact(email="ngqui.official@gmail.com"),
        license=openapi.License(name="Trần Ngọc Quí@2024"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('rooms.urls')),
                  path('', include('users.urls')),
                  # path('', include('payments.urls')),
                  path('api/', include('bookings.urls')),

                  re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                          name='schema-json'),
                  re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
