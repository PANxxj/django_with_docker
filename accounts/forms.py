from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """Custom form for creating a new user."""
    
    class Meta:
        model = CustomUser
        fields = ('phone_no', 'email', 'is_active', 'is_staff', 'is_superuser')

class CustomUserChangeForm(UserChangeForm):
    """Custom form for changing user data."""
    
    class Meta:
        model = CustomUser
        fields = ('phone_no', 'email', 'is_active', 'is_staff', 'is_superuser')
