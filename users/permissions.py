from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsEmployeeOrManagerOrAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.role in ['admin', 'manager', 'employee']
        return False


class IsAdminOrManager(BasePermission):


    def has_permission(self, request, view):
        # Kiểm tra xem người dùng đã xác thực hay chưa
        if request.user.is_authenticated:
            return request.user.role in ['admin', 'manager']
        return False
