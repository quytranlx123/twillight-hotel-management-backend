# admin.py
from django.contrib import admin
from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'phone_number', 'address']
    search_fields = ['user__username', 'phone']

    def save_model(self, request, obj, form, change):
        # Mã hóa số CCCD trước khi lưu
        identity_card_number = form.cleaned_data.get('identity_card_number')
        if identity_card_number:
            obj.set_identity_card_number(identity_card_number)
        # Lưu đối tượng
        super().save_model(request, obj, form, change)


admin.site.register(Customer, CustomerAdmin)
