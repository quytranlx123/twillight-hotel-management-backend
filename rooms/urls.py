# urls.py
from django.urls import path
from .views import RoomTypeListView, RoomTypeDetailView, RoomTypeCreateView, RoomTypeUpdateView, RoomTypeDeleteView, \
    RoomListView, RoomDetailView, RoomCreateView, RoomUpdateView, RoomDeleteView, RoomListViewWithRoomType

urlpatterns = [
    path('api/roomtypes/', RoomTypeListView.as_view(), name='room-list'),  # Để xem tất cả các phòng
    path('api/roomtype/<int:pk>/', RoomTypeDetailView.as_view(), name='room-detail'),  # Để xem một phòng cụ thể
    path('api/roomtype/create/', RoomTypeCreateView.as_view(), name='room-create'),  # Để tạo phòng mới
    path('api/roomtype/update/<int:pk>/', RoomTypeUpdateView.as_view(), name='room-update'),  # Để cập nhật phòng
    path('api/roomtype/delete/<int:pk>/', RoomTypeDeleteView.as_view(), name='room-delete'),  # Để xóa phòng
    path('api/rooms/', RoomListView.as_view(), name='room-list'),  # Để xem tất cả các phòng
    path('api/rooms_with_roomtype/', RoomListViewWithRoomType.as_view(), name='rooms-roomtype'),
    path('api/room/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),  # Để xem một phòng cụ thể
    path('api/room/create/', RoomCreateView.as_view(), name='room-create'),  # Để tạo phòng mới
    path('api/room/update/<int:pk>/', RoomUpdateView.as_view(), name='room-update'),  # Để cập nhật phòng
    path('api/room/delete/<int:pk>/', RoomDeleteView.as_view(), name='room-delete'),  # Để xóa phòng
]
