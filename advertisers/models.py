from django.db import models
from account.models import User 

# Create your models here.
class Advertiser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='advertiser_profiles/', null=True, blank=True)

    def __str__(self):
        return self.business_name
    
class Advertisements(models.Model):
    ADVERTISEMENT_TYPE_CHOICES = [
        ('lifestyle', 'Life Style'),
        ('food_cooking', 'Food and Cooking'),
        ('electronics_appliances', 'Electronics and Home Appliances'),
        ('movie', 'Movie'),
        ('music', 'Music'),
        ('photography', 'Photography'),
        ('gaming', 'Gaming'),
        ('travel', 'Travel'),

    ]
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    link = models.URLField()
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='advertisements/')
    advertisement_type = models.CharField(max_length=30, choices=ADVERTISEMENT_TYPE_CHOICES, default='lifestyle')

    def __str__(self):
        return self.title
    
class MaliciousClick(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Advertisements, on_delete=models.CASCADE)
    clicked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} clicked on {self.ad.title}"