from django.shortcuts import render
from django.views.decorators.cache import never_cache

@never_cache
def landing_page(request):
    return render(request, "home/landing_page.html")
