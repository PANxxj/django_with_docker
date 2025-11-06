from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm

class CustomUserAdmin(UserAdmin):
    # Display fields in the admin list view
    list_display = ('phone_no', 'email', 'is_staff', 'is_active', 'is_superuser')
    
    # Add filters for the admin list view
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    
    # Search by phone number and email
    search_fields = ('phone_no', 'email')
    
    # Fields displayed in the edit view for a user
    fieldsets = (
        (None, {'fields': ('phone_no', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Dates', {'fields': ('created', 'modified')}),
    )
    
    # Fields to include in the "add user" form (when creating a user)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_no', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')
        }),
    )
    
    # Use custom forms for creating and updating users
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # Making the model active in the admin interface
    model = CustomUser
    ordering = ('phone_no',)
# Register the CustomUser model with the admin interface
admin.site.register(CustomUser, CustomUserAdmin)
