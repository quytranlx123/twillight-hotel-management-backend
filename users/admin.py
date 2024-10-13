from django.contrib import admin
from .models import CustomUser
from .serializers import CustomUserSerializer


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    # Lấy các trường từ serializer
    serializer = CustomUserSerializer()
    serializer_fields = [field for field in serializer.fields]  # Lấy danh sách tên các trường

    # Sử dụng các trường này cho list_display
    list_display = serializer_fields  # Sử dụng các trường từ serializer cho list_display

    # Nếu bạn muốn sử dụng cho fieldsets hoặc readonly_fields, bạn có thể làm tương tự:
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Thông tin cá nhân', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Quyền hạn', {'fields': ('is_active',)}),
    )
