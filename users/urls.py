from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import Login, Register, UserView, Logout, PermissionViewSet, UserAppsPermissionsView, UsersViewSet, \
    VerifyOTP, CheckSession, CustomUserListCreateView, CustomUserRetrieveUpdateDestroyView, ForgotPassword, \
    ResetPassword

urlpatterns = [
    path('session/', CheckSession.as_view(), name='session'),
    path('api/users/register/', Register.as_view(), name='register'),
    path('api/users/verify-otp/', VerifyOTP.as_view(), name='verify_otp'),
    path('api/users/login/', Login.as_view(), name='login'),
    path('api/users/user/', UserView.as_view(),name='userview'),
    path('api/users/logout/', Logout.as_view(), name='logout'),
    path('api/users/<int:user_id>/assign_permission/<str:permission_codename>/',
         PermissionViewSet.as_view({'post': 'assign_permission'})),
    path('api/users/<int:user_id>/revoke_permission/<str:permission_codename>/',
         PermissionViewSet.as_view({'post': 'revoke_permission'})),
    path('api/users/<int:user_id>/permissions/', PermissionViewSet.as_view({'get': 'list_user_permissions'})),
    path('api/users/user-apps-permissions/', UserAppsPermissionsView.as_view(), name='user-apps-permissions'),
    path('api/users/', CustomUserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<int:pk>/', CustomUserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('api/users/forgot-password/', ForgotPassword.as_view(), name='forgot-password'),
    path('api/users/reset-password/', ResetPassword.as_view(), name='reset-password'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# GET /users/: Lấy danh sách tất cả người dùng.
# POST /users/: Thêm một người dùng mới.
# GET /users/<id>/: Xem thông tin của người dùng với ID tương ứng.
# PUT/PATCH /users/<id>/: Cập nhật thông tin của người dùng với ID tương ứng.
# DELETE /users/<id>/: Xóa người dùng với ID tương ứng.
