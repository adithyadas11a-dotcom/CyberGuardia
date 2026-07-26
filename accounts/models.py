from django.db import models
from account.models import User 
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    area_of_interest = models.CharField(max_length=255, blank=True)
    age = models.IntegerField(null=True)
    country = models.CharField(max_length=20, null=True)
    state = models.CharField(max_length=20, null=True)
    safe_mode = models.BooleanField(default=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)


    def __str__(self):
        return f"{self.user.username}'s Profile"
    

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.otp}"