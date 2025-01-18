from django.contrib.auth.models import User
from django.db import models

from django.db import models
from django.utils.timezone import now

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)  # Approval status
    is_approved = models.BooleanField(default=False)  # Track approval status
    is_rejected = models.BooleanField(default=False)  # Add this field
    created_at = models.DateTimeField(default=now)  # New field to track creation time

    def __str__(self):
        return self.user.username
    
# models.py
from django.db import models

class ImportantEvent(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
