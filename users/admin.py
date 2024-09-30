# # admin.py trong app users
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import CustomUser
from customers.models import Customer
from employees.models import Employee
from django.contrib.auth.models import Permission


class CustomerInline(admin.StackedInline):
    model = Customer
    max_num = 10
    extra = 1


class EmployeeInline(admin.StackedInline):
    model = Employee
    max_num = 10
    extra = 1


class CustomUserAdmin(SimpleHistoryAdmin):
    is_superuser = 'is_superuser'
    list_display = ['username', 'is_superuser', 'is_customer', 'is_employee', 'last_login', 'date_joined',]
    search_fields = ['username', 'email']
    inlines = (CustomerInline, EmployeeInline)
    ordering = ['-last_login',]

    class Media:
        js = ('custom_user_admin.js',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Permission)