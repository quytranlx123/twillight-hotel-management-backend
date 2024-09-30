from django.contrib import admin
from activity_logs.models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'os', 'path', 'ip', 'timestamp')
    readonly_fields = ('user', 'os', 'path', 'ip', 'timestamp')
    list_filter = ('user', 'os', 'timestamp')
    list_per_page = 20