# bookings/urls.py
from rest_framework.routers import DefaultRouter
from .views import (
    BookingViewSet,
    DailyRevenueView,
    MonthlyRevenueView,
    AnnualRevenueView,
    RevenueSummaryView,
)
from django.urls import path

router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('daily/', DailyRevenueView.as_view(), name='daily-revenue'),
    path('monthly/', MonthlyRevenueView.as_view(), name='monthly-revenue'),
    path('annual/', AnnualRevenueView.as_view(), name='annual-revenue'),
    path('summary/', RevenueSummaryView.as_view(), name='revenue-summary'),
]

# Thêm router.urls vào urlpatterns
urlpatterns += router.urls
