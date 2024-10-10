from django.urls import path
from .views import Login, Register, UserView, Logout, PermissionViewSet, UserAppsPermissionsView, UsersViewSet

urlpatterns = [
    path('api/users/register/', Register.as_view(), name='register'),
    path('api/users/login/', Login.as_view(), name='login'),
    path('api/users/user/', UserView.as_view(),name='userview'),
    path('api/users/logout/', Logout.as_view(), name='logout'),
    path('api/users/', UsersViewSet.as_view(), name='usersview'),
    path('api/users/<int:user_id>/assign_permission/<str:permission_codename>/',
         PermissionViewSet.as_view({'post': 'assign_permission'})),
    path('api/users/<int:user_id>/revoke_permission/<str:permission_codename>/',
         PermissionViewSet.as_view({'post': 'revoke_permission'})),
    path('api/users/<int:user_id>/permissions/', PermissionViewSet.as_view({'get': 'list_user_permissions'})),
    path('api/users/user-apps-permissions/', UserAppsPermissionsView.as_view(), name='user-apps-permissions'),
]
