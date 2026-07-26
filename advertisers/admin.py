from django.contrib import admin
from .models import Advertiser, Advertisements, MaliciousClick
# Register your models here.

admin.site.register(Advertiser)
admin.site.register(Advertisements)
admin.site.register(MaliciousClick)