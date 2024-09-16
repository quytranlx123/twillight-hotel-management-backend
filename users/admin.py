# # admin.py trong app users
from django.contrib import admin
from employees.admin import EmployeeAdmin
from .models import CustomUser
from customers.models import Customer
from employees.models import Employee
from django.contrib.auth.models import Permission, Group


class CustomerInline(admin.StackedInline):
    model = Customer
    max_num = 10
    extra = 1


class EmployeeInline(admin.StackedInline):
    model = Employee
    max_num = 10
    extra = 1


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_customer', 'is_employee']
    search_fields = ['username', 'email']
    inlines = (CustomerInline, EmployeeInline)

    class Media:
        js = ('custom_user_admin.js',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Permission)