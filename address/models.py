from django.db import models
from user_profile.models import UserProfile


class Address(models.Model):
    user_address = models.ForeignKey(
        UserProfile, related_name='profile_address', on_delete=models.CASCADE)
    address_name = models.CharField(max_length=255)
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.address_name}'