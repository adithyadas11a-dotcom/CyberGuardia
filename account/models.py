from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('normal', 'Normal User'),
        ('advertiser', 'Advertiser'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='normal')
