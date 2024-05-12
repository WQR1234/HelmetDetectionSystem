from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    gender = models.CharField(max_length=5, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)


    class Meta:
        db_table = 'user_profile'