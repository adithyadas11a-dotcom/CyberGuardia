from django.urls import path
from . import views

app_name = 'advertisers'

urlpatterns = [
    path('register/', views.resister, name='register'),
    path('add-advertisement/', views.add_advertisement, name='add_advertisement'),
    path('view-advertisements/', views.view_advertisements, name='view_advertisements'),
    path('ad-click/<int:ad_id>/', views.ad_click, name='ad_click'),
    path('ad/<int:ad_id>/visit/', views.visit_anyway, name='visit_anyway'),
    path("user-details/", views.user_details, name="user_details"),
    path("profile/<str:username>/", views.adver_profile, name="adver_profile"),
    path('edit/', views.edit_advertiser_profile, name='adver_edit_profile'),
    

]
