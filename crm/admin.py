from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile, ImportantEvent

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['profile_pic_display', 'user', 'age', 'gender', 'date_of_birth', 'is_approved', 'is_rejected', 'created_at']
    list_editable = ['is_approved', 'is_rejected']
    search_fields = ['user__username', 'user__email', 'gender']
    list_filter = ['is_approved', 'is_rejected', 'created_at', 'gender']
    ordering = ['-created_at']
    readonly_fields = ['profile_pic_display']

    def profile_pic_display(self, obj):
        """Display profile picture in admin panel."""
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;"/>', obj.profile_picture.url)
        return "No Image"
    
    profile_pic_display.short_description = "Profile Picture"

@admin.register(ImportantEvent)
class ImportantEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'is_featured', 'created_at']
    search_fields = ['title', 'description']
    list_filter = ['date', 'is_featured']
    list_editable = ['is_featured']
    ordering = ['-date']