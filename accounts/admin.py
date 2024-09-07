# # admin.py trong app accounts
# from django.contrib import admin
# from django import forms
# from .models import CustomUser
# from customers.models import Customer
# from employees.models import Employee
#
#
# class CustomerInline(admin.StackedInline):
#     model = Customer
#     max_num = 10
#     pk_name = 'user'
#     extra = 1
#
#
# class EmployeeInline(admin.StackedInline):
#     model = Employee
#     max_num = 10
#     pk_name = 'user'
#     extra = 1
#
#
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ['username', 'email', 'is_customer', 'is_employee']
#     search_fields = ['username', 'email']
#
#     inlines = []  # Bắt đầu không có inlines
#
#     class Media:
#         js = 'accounts/static/custom_user_admin.js'  # Đường dẫn đến file JavaScript
#
#     def get_inlines(self, request, obj=None):
#         inlines = []
#         if obj:  # Kiểm tra nếu có đối tượng
#             if obj.is_customer:  # Nếu là customer
#                 inlines.append(CustomerInline)
#             if obj.is_employee:  # Nếu là employee
#                 inlines.append(EmployeeInline)
#         return inlines
#
#
# # Đăng ký CustomUserAdmin
# admin.site.register(CustomUser, CustomUserAdmin)
#
#
#
# admin.py trong app accounts
# admin.py trong app accounts

from django.contrib import admin
from .models import CustomUser
from customers.models import Customer
from employees.models import Employee

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
        js = ('custom_user_admin.js',)  # Đảm bảo đường dẫn đúng


admin.site.register(CustomUser, CustomUserAdmin)

