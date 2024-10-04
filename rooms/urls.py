# urls.py
from django.urls import path
from .views import RoomListView, RoomDetailView, RoomCreateView, RoomUpdateView, RoomDeleteView

urlpatterns = [
    path('api/rooms/', RoomListView.as_view(), name='room-list'),  # Để xem tất cả các phòng
    path('api/rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),  # Để xem một phòng cụ thể
    path('api/rooms/create/', RoomCreateView.as_view(), name='room-create'),  # Để tạo phòng mới
    path('api/rooms/update/<int:pk>/', RoomUpdateView.as_view(), name='room-update'),  # Để cập nhật phòng
    path('api/rooms/delete/<int:pk>/', RoomDeleteView.as_view(), name='room-delete'),  # Để xóa phòng
]
