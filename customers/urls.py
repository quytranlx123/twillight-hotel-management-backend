from django.urls import path
from .views import CustomerProfileViewSet, UpdateCustomerProfileViewSet
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'api/customer/profile', CustomerProfileViewSet, basename='customer-profile')
router.register(r'api/customer/update-profile', UpdateCustomerProfileViewSet, basename='update-customer-profile')
urlpatterns = router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
