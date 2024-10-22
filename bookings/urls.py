from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, DailyRevenueView, MonthlyRevenueView, AnnualRevenueView, RevenueSummaryView

# Tạo một router
router = DefaultRouter()
booking_list = BookingViewSet.as_view({
    'post': 'create',
    'get': 'list',
    'update': 'update',
})

booking_detail = BookingViewSet.as_view({
    'get': 'retrieve',  # Lấy chi tiết một booking
    'put': 'update',    # Cập nhật một booking
    'patch': 'partial_update',  # Cập nhật một phần
    'delete': 'destroy',  # Xóa một booking
})

# Định nghĩa urlpatterns
urlpatterns = [
    path('api/daily/', DailyRevenueView.as_view(), name='daily-revenue'),  # Endpoint cho doanh thu hàng ngày
    path('api/monthly/', MonthlyRevenueView.as_view(), name='monthly-revenue'),  # Endpoint cho doanh thu hàng tháng
    path('api/annual/', AnnualRevenueView.as_view(), name='annual-revenue'),  # Endpoint cho doanh thu hàng năm
    path('api/summary/', RevenueSummaryView.as_view(), name='revenue-summary'),  # Endpoint cho tóm tắt doanh thu
    path('api/bookings/', booking_list, name='booking-list'),
    path('api/bookings/complete/', BookingViewSet.as_view({'post': 'complete_booking'}), name='booking-complete'),
    path('api/bookings/<int:pk>/', booking_detail, name='booking-detail'),
]

# Endpoints của BookingViewSet:
#
# /bookings/complete/
# POST /api/bookings/: Tạo một đặt phòng và gửi OTP.
# GET /api/bookings/: Lấy danh sách tất cả các đặt phòng.
# GET /api/bookings/{id}/: Lấy thông tin đặt phòng cụ thể.
# PUT /api/bookings/{id}/: Cập nhật thông tin đặt phòng.
# DELETE /api/bookings/{id}/: Hủy đặt phòng.
# Endpoints cho Doanh Thu:
#
# GET /api/daily/: Nhận báo cáo doanh thu hàng ngày.
# GET /api/monthly/: Nhận báo cáo doanh thu hàng tháng.
# GET /api/annual/: Nhận báo cáo doanh thu hàng năm.
# GET /api/summary/: Nhận tóm tắt doanh thu.
