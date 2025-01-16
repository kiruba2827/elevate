from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)  # Approval status
    is_approved = models.BooleanField(default=False)  # Track approval status
    is_rejected = models.BooleanField(default=False)  # Add this field


    def __str__(self):
        return self.user.username