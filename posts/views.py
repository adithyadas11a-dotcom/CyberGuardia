from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Comment
from .forms import PostForm, CommentForm
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
import json
from accounts.models import Profile
from advertisers.models import Advertisements
from django.contrib import messages
@never_cache
@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "posts/create_post.html", {"form": form})

@never_cache
@login_required
def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    user_profile = Profile.objects.filter(user=request.user).first()
    user_interests = [interest.strip().lower().replace(" ", "") for interest in user_profile.area_of_interest.split(",")]
    # user_interests = user_profile.area_of_interest.split(",")
    # ads = Advertisements.objects.filter(advertisement_type__in=user_interests).first()
    # adss = Advertisements.objects.values_list("advertisement_type", flat=True)
    ads = Advertisements.objects.filter(advertisement_type__in=user_interests)

    # print('advertismetns ',ads)
    # print(adss)
    # print('user interests',user_interests)
    for post in posts:
        post.is_liked_by_user = post.likes.filter(user=request.user).exists()

    return render(request, "posts/post_list.html", {"posts": posts, "ads": ads})

@never_cache
@login_required
def post_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "posts/post_details.html", {"post": post})

@never_cache
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True
   
    return JsonResponse({"liked": liked, "likes_count": post.likes.count()})


@never_cache
@login_required
def comment_on_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        text = request.POST.get("text")

        if text:
            comment = Comment.objects.create(user=request.user, post=post, text=text)
            return JsonResponse({
                "success": True,
                "comment_id": comment.id,
                "username": comment.user.username,
                "text": comment.text,
                "timestamp": comment.created_at, 
                "profile_image": comment.user.profile.profile_image.url, 
            })

    return JsonResponse({"success": False}, status=400)

@csrf_exempt
@login_required
def report_comment(request, comment_id):
    if request.method == "POST":
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user == request.user:
                return JsonResponse({"success": False, "error": "You cannot report your own comment"}, status=403)
        comment.reported = True
        comment.save()
        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False}, status=400)

@login_required
def my_posts(request, user_id):
    my_posts = Post.objects.filter(user_id=user_id)
    return render(request, 'posts/my_posts.html', {'my_posts':my_posts})

@login_required
def delete_post(request, post_id):
    print(f"User: {request.user}, Post ID: {post_id}")
    post = Post.objects.filter(id=post_id, user=request.user).first()
    
    if post:
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('my_posts', user_id=request.user.id)
    else:
        return redirect('home')

    
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('my_posts', user_id=request.user.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})
@login_required
def toggle_safe_mode(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile.safe_mode = not profile.safe_mode
    profile.save()
    return redirect('home')