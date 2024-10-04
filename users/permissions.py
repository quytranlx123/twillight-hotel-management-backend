from rest_framework import permissions


class IsEmployeeOrManagerOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.role in ['admin', 'manager', 'employee']
        return False
