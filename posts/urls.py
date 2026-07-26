from django.urls import path
from .views import create_post, post_list, like_post, comment_on_post, report_comment, my_posts, toggle_safe_mode, post_details, delete_post, edit_post

urlpatterns = [
    path("", post_list, name="home"),
    path("create/", create_post, name="create_post"),
    path("like/<int:post_id>/", like_post, name="like_post"),
    path("comment/<int:post_id>/", comment_on_post, name="comment_post"),
    path('report_comment/<int:comment_id>/', report_comment, name='report_comment'),
    path('my-posts/<int:user_id>/', my_posts, name='my_posts'),
    path('delete-post/<int:post_id>/', delete_post, name='delete_my_post'),
    path('toggle-safe-mode/', toggle_safe_mode, name='toggle_safe_mode'),
    path('post/<int:post_id>/', post_details, name='post_details'),
    path('post/<int:post_id>/edit/', edit_post, name='edit_post'),
]   
