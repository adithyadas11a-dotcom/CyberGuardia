from django.urls import path
from .views import register, user_login, user_logout, forgot_password, verify_otp, reset_password, user_profile, edit_profile


urlpatterns = [
    path('register/', register, name='register'),
    path('', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path("forgot-password/", forgot_password, name="forgot_password"),
    path("verify-otp/", verify_otp, name="verify_otp"),
    path("reset-password/", reset_password, name="reset_password"),
    path("profile/<str:username>/", user_profile, name="user_profile"),
    path('edit/', edit_profile, name='edit_profile'),
]
