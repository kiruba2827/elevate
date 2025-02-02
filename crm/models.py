from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)  # Approval status
    is_rejected = models.BooleanField(default=False)  # Rejection status
    created_at = models.DateTimeField(default=now)  # Track creation time
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Profile Picture

    def __str__(self):
        return self.user.username


class ImportantEvent(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=now)  # Track creation time
    is_featured = models.BooleanField(default=False)  # Feature flag for important events

    def __str__(self):
        return f"{self.title} - {self.date}"
