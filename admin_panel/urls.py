from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.all_users, name='all_users'),
    path('posts/', views.all_posts, name='all_posts'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('abusive_comments/', views.abusive_comments, name='abusive_comments'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('suspend-user/<int:user_id>/', views.suspend_user, name='suspend_user'),
    path('user-profile-admin<str:username>/', views.user_profile_admin, name='user_profile_admin'),

    path('admin/advertisers/', views.all_advertisers_view, name='all_advertisers'),
    path('advertisements/', views.all_advertisements, name='all_advertisements'),
    path('admin/posts/', views.all_posts_view, name='all_posts'),
    path('admin/advertiser/approve/<int:id>/', views.approve_advertiser, name='approve_advertiser'),
    path('admin/advertiser/reject/<int:id>/', views.reject_advertiser, name='reject_advertiser'),
]
