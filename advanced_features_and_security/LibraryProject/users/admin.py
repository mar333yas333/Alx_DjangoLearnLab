from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


class CustomUserAdmin(BaseUserAdmin):
    """
    Custom ModelAdmin for managing CustomUser in the Django admin interface.
    """
    model = CustomUser
    
    # Display fields in list view
    list_display = ("email", "username", "first_name", "last_name", "date_of_birth", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "date_joined")
    
    # Define fieldsets for form display
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "date_of_birth", "profile_photo")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    
    # Fieldsets for adding new users
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "date_of_birth", "profile_photo"),
        }),
    )
    
    # Allow searching by email and username
    search_fields = ("email", "username", "first_name", "last_name")
    
    # Default ordering
    ordering = ("-date_joined",)


admin.site.register(CustomUser, CustomUserAdmin)
