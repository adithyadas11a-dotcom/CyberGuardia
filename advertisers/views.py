from django.shortcuts import get_object_or_404, render, redirect
from .forms import AdvertiserRegistrationForm, EditAdvertiserForm
from account.models import User
from .models import Advertiser, Advertisements
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .utils import check_malicious_url
from accounts.models import Profile
from .models import MaliciousClick
# Create your views here.

def resister(request):
    if request.method == 'POST':
        form = AdvertiserRegistrationForm(request.POST, request.FILES)
        profile_image = request.FILES.get('profile_image')
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = request.POST.get('confirm_password')
            business_name = form.cleaned_data['business_name']
            business_type = form.cleaned_data['business_type']
            contact_number = form.cleaned_data['contact_number']
            address = form.cleaned_data['address']
            profile_image=profile_image

            user = User.objects.create_user(username=username, email=email, password=password, user_type='advertiser', is_active=False)
            Advertiser.objects.create(user=user, business_name=business_name, business_type=business_type, contact_number=contact_number, address=address, profile_image=profile_image)
            messages.success(request, 'Registration Successfull! please login')
            return redirect('login')
    else:
        form = AdvertiserRegistrationForm()
    return render(request, 'advertisers/register.html', {'form': form})

@never_cache
@login_required
def add_advertisement(request):
    advertiser = Advertiser.objects.get(user=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        link = request.POST.get('link')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')
        advertisement_type = request.POST.get('advertisement_type')
        image = request.FILES.get('image')

        if title and link and start_date and end_date and description and advertisement_type and image:
            Advertisements.objects.create(
                advertiser=advertiser, 
                title=title,
                link=link,
                start_date=start_date,
                end_date=end_date,
                description=description,
                advertisement_type=advertisement_type,
                image=image
            )
            messages.success(request, "Advertisement added successfully!")
            return redirect('advertisers:add_advertisement')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'advertisers/add_advertisement.html')

@login_required
def edit_advertiser_profile(request):
    user = request.user
    advertiser = user.advertiser
    if request.method == 'POST':
        form = EditAdvertiserForm(request.POST, request.FILES, user=request.user)
        
        if form.is_valid():
            request.user.username = form.cleaned_data['username']
            request.user.email = form.cleaned_data['email']
            request.user.save()

            # Update Profile Model
            advertiser, created = Advertiser.objects.get_or_create(user=request.user)
            advertiser.business_name = form.cleaned_data['business_name']
            advertiser.business_type = form.cleaned_data['business_type']
            advertiser.contact_number = form.cleaned_data['contact_number']
            advertiser.address = form.cleaned_data['address']
            advertiser.profile_image = form.cleaned_data['profile_image']
            
            if 'profile_image' in request.FILES:  
                advertiser.profile_image = request.FILES['profile_image']

            advertiser.save()
            user.save()

            messages.success(request, "Your profile has been updated successfully!")
            return redirect('advertisers:adver_profile', username=request.user.username)
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = EditAdvertiserForm(user=request.user)

    return render(request, 'advertisers/adver_edit_profile.html', {'form': form})


def adver_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Advertiser, user=user)

    return render(request, 'advertisers/adver_profile.html', {'user': user, 'profile': profile})



@never_cache
@login_required 
def view_advertisements(request):
    advertisements = Advertisements.objects.filter(advertiser=request.user.advertiser)
    return render(request, 'advertisers/view_advertisements.html', {'advertisements': advertisements})

@never_cache
@login_required
def ad_click(request, ad_id):
    """
    Handles ad clicks, checks if the URL is malicious, and redirects the user accordingly.

    Args:
        request: The HTTP request object.
        ad_id (int): The ID of the clicked advertisement.

    Returns:
        Redirects to the ad URL or displays a warning.
    """
    ad = get_object_or_404(Advertisements, id=ad_id)
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    # Run ML model to check if the ad URL is malicious
    result = check_malicious_url(ad.link)  # Always run ML, even if Safe Mode is OFF

    if profile.safe_mode:
        if result == "Benign":
            return redirect(ad.link)  # Safe, allow direct access
        else:
            return render(request, "posts/ad_warning.html", {"ad": ad, "result": result})
    # Safe Mode OFF: Allow all links, but log if malicious
    if result != "Benign":
        MaliciousClick.objects.get_or_create(user=user, ad=ad)  # Log unsafe clicks
    return redirect(ad.link)  # Always allow access
    

@login_required
def visit_anyway(request, ad_id):
    """
    Logs user details when they click 'Visit Anyway' and redirects them to the malicious site.
    """
    ad = get_object_or_404(Advertisements, id=ad_id)
    
    # Log the click (store user details and ad info)
    MaliciousClick.objects.get_or_create(user=request.user, ad=ad)

    # Redirect the user to the actual ad link
    return redirect(ad.link)

@login_required
def user_details(request):
    advertiser = Advertiser.objects.get(user=request.user)
    clicked_users = MaliciousClick.objects.filter(ad__advertiser=advertiser)
    return render(request, "advertisers/user_details.html", {"clicked_users": clicked_users})

def toggle_safe_mode(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile.safe_mode = not profile.safe_mode
    profile.save()
    return redirect('dashboard') 