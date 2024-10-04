from django.urls import path
from .views import Login, Register, UserView, Logout

urlpatterns = [
    path('api/register/', Register.as_view(), name='register'),
    path('api/login/', Login.as_view(), name='login'),
    path('api/user/', UserView.as_view(),name='userview'),
    path('api/logout/', Logout.as_view(), name='logout'),
]
