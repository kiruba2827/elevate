from django.contrib import admin
from .models import UserProfile
from .models import ImportantEvent

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'gender', 'date_of_birth']



@admin.register(ImportantEvent)
class ImportantEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'description']  # Fields to display in the admin list view
    search_fields = ['title', 'description']  # Make the fields searchable
    list_filter = ['date']  # Add a filter by date
