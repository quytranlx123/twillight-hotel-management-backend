from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('id','username', 'email', 'first_name', 'last_name', 'account_updated','role')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('email',)

    # Cấu hình các trường trong giao diện chỉnh sửa
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('date_joined', 'account_updated')}),  # Bao gồm account_updated
    )

    # Đánh dấu các trường không thể chỉnh sửa
    readonly_fields = ('date_joined', 'account_updated')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
