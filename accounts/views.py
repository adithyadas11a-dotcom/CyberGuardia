from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from account.models import User
from .forms import RegistrationForm
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
import random
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from .models import OTP
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = request.POST.get('confirm_password')
            area_of_interest = form.cleaned_data['area_of_interest']
            age = form.cleaned_data['age']
            country = form.cleaned_data['country']
            state = form.cleaned_data['state']
            profile_image = form.cleaned_data['profile_image']
            
            user = User.objects.create_user(username=username, email=email, password=password, user_type='normal')
            Profile.objects.create(user=user, area_of_interest=area_of_interest, age=age, country=country, state=state, profile_image=profile_image)

            messages.success(request, 'Registration Successfull! please login')
            return redirect('login')  
        
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif user.user_type == 'normal':
                return redirect("home")
            elif user.user_type == 'advertiser':
                return redirect("advertisers:add_advertisement")
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, "accounts/login.html")

@csrf_exempt
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            otp_code = str(random.randint(100000, 999999))  
            OTP.objects.create(user=user, otp=otp_code)

            # Send email
            send_mail(
                "Password Reset OTP",
                f"Your OTP for password reset is: {otp_code}",
                "your_email@example.com",
                [email],
                fail_silently=False,
            )
            request.session["reset_email"] = email
            return redirect("verify_otp")
        except User.DoesNotExist:
            messages.error(request, "Email not found")

    return render(request, "accounts/forgot_password.html")

@csrf_exempt
def verify_otp(request):
    if request.method == "POST":
        email = request.session.get("reset_email")
        entered_otp = request.POST.get("otp")

        try:
            user = User.objects.get(email=email)
            otp_entry = OTP.objects.filter(user=user).order_by("-created_at").first()

            if otp_entry and otp_entry.otp == entered_otp:
                request.session["otp_verified"] = True
                return redirect("reset_password")
            else:
                messages.error(request, "Invalid OTP")
        except User.DoesNotExist:
            messages.error(request, "User not found")

    return render(request, "accounts/verify_otp.html")

@csrf_exempt
def reset_password(request):
    if not request.session.get("otp_verified"):
        return redirect("forgot_password")

    if request.method == "POST":
        email = request.session.get("reset_email")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password == confirm_password:
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password reset successful! Please login.")
                del request.session["reset_email"]
                del request.session["otp_verified"]
                return redirect("login")
            except User.DoesNotExist:
                messages.error(request, "User not found")
        else:
            messages.error(request, "Passwords do not match")

    return render(request, "accounts/reset_password.html")

@never_cache
@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    return render(request, 'accounts/user_profile.html', {'user': user, 'profile': profile})


@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, user=request.user)
        
        if form.is_valid():
            request.user.username = form.cleaned_data['username']
            request.user.email = form.cleaned_data['email']
            request.user.save()

            # Update Profile Model
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.age = form.cleaned_data['age']
            profile.country = form.cleaned_data['country']
            profile.state = form.cleaned_data['state']
            profile.area_of_interest = form.cleaned_data['area_of_interest']
            profile.profile_image = form.cleaned_data['profile_image']
            
            if 'profile_image' in request.FILES:  
                profile.profile_image = request.FILES['profile_image']

            profile.save()
            user.save()

            messages.success(request, "Your profile has been updated successfully!")
            return redirect('user_profile', username=request.user.username)
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = EditProfileForm(user=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})

def user_logout(request):
    logout(request)
    request.session.flush() 
    request.session.modified = True 
    response = redirect('login')  
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    return redirect("login")
