from django import forms
from account.models import User
from django.core.exceptions import ValidationError
import re
from .models import Advertiser
from django import forms
from django.core.exceptions import ValidationError
import re

class AdvertiserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    business_name = forms.CharField(max_length=255, required=True)
    business_type = forms.CharField(max_length=255, required=True)
    contact_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(max_length=500, required=True)
    profile_image = forms.ImageField(required=True)  # Uncomment if needed

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username.isdigit():
            raise ValidationError("Username must contain at least one letter.")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already registered.")
        return email

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get("contact_number")
        if not contact_number.isdigit():
            raise ValidationError("Contact number must contain digits only.")
        if len(contact_number) != 10:
            raise ValidationError("Contact number must be 10 digits long.")
        return contact_number

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Za-z]', password):
            raise ValidationError("Password must contain at least one letter.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain at least one number.")
        return password

    def clean_business_name(self):
        business_name = self.cleaned_data.get("business_name")
        if business_name.isdigit():
            raise ValidationError("Business name must contain at least one letter.")
        return business_name

    def clean_business_type(self):
        business_type = self.cleaned_data.get("business_type")
        if business_type.isdigit():
            raise ValidationError("Business type must contain at least one letter.")
        return business_type

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        return cleaned_data

    

class EditAdvertiserForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'text-black p-2 w-full'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'text-black p-2 w-full'}))
    business_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'text-black p-2 w-full'}))
    business_type = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'text-black p-2 w-full'}))
    contact_number = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'text-black p-2 w-full'}))
    address = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'text-black p-2 w-full'}))
    profile_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'text-black p-2 w-full'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

       
        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email
            advertiser = getattr(self.user, 'advertiser', None)
            if advertiser:
                self.fields['business_name'].initial = advertiser.business_name
                self.fields['business_type'].initial = advertiser.business_type
                self.fields['contact_number'].initial = advertiser.contact_number
                self.fields['address'].initial = advertiser.address
                self.fields['profile_image'].initial = advertiser.profile_image
