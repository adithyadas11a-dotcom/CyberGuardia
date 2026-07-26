from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from account.models import User
from posts.models import Post, Comment
from accounts.models import Profile
from advertisers.models import Advertisements
# Create your views here.

def is_admin(user):
    return user.is_superuser

@never_cache
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    advertisers = User.objects.filter(is_active=False, user_type='advertiser')
    recent_posts = Post.objects.order_by('-created_at')[:3]
    return render(request, 'admin_panel/admin_dashboard.html', {'advertisers': advertisers, 'recent_posts': recent_posts})

@never_cache
@user_passes_test(is_admin)
@login_required
def all_advertisers_view(request):
    advertisers = User.objects.filter(user_type='advertiser')
    return render(request, 'admin_panel/advertiser_requests.html', {'advertisers': advertisers})

@never_cache
@user_passes_test(is_admin)
@login_required
def all_posts_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/recent_posts.html', {'posts': posts})

@never_cache
@user_passes_test(is_admin)
@login_required
def approve_advertiser(request, id):
    advertiser = User.objects.get(id=id)
    advertiser.is_active = True
    advertiser.save()
    messages.success(request, "The advertiser has been approved successfully.")
    return redirect('all_advertisers')

@never_cache
@user_passes_test(is_admin)
@login_required
def reject_advertiser(request, id):
    advertiser = get_object_or_404(User, id=id)
    advertiser.is_active = False
    advertiser.save()
    messages.error(request, "The advertiser has been rejected.")
    return redirect('all_advertisers')

@never_cache
@login_required
@user_passes_test(is_admin)
def all_users(request):
    users = User.objects.filter(user_type='normal', is_superuser=False)
    return render(request, 'admin_panel/all_users.html', {'users':users})

@never_cache
@login_required
@user_passes_test(is_admin)
def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'admin_panel/all_posts.html', {'posts': posts})

def all_advertisements(request):
    advertisements = Advertisements.objects.all()
    return render(request, 'admin_panel/all_advertisements.html', {'advertisements': advertisements})

@never_cache
@user_passes_test(is_admin)
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user.is_superuser:
        post.delete()
        messages.success(request, "Post deleted successfully.")
    return redirect('all_posts')

@never_cache
@user_passes_test(is_admin)
@login_required
def abusive_comments(request):
    flagged_comments = Comment.objects.filter(flagged=True)
    reported_comments = Comment.objects.filter(reported=True)
    return render(request, 'admin_panel/abusive_comments.html', {'flagged_comments': flagged_comments, 'reported_comments': reported_comments})

@never_cache
@user_passes_test(is_admin)
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('abusive_comments')

@never_cache
@user_passes_test(is_admin)
@login_required
def user_profile_admin(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    return render(request, 'admin_panel/user_profile_admin.html', {'user': user, 'profile': profile})

@never_cache
@user_passes_test(is_admin)
@login_required
def suspend_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    return redirect('all_users')


def total_count(request):
    users_count = User.objects.all()

    return render(request, 'admin_panel/admin_dashboard.htm', {'users_count':users_count})