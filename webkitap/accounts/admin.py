from django.contrib import admin
from .models import UserProfile, Notification

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'theme_preference')
    search_fields = ('user__username', 'bio')
    list_filter = ('theme_preference',)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read')
    search_fields = ('user__username', 'title', 'message')
    date_hierarchy = 'created_at'

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Notification, NotificationAdmin) 