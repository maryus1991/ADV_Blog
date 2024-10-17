from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    for set user admin options 
    """
    model = User
    list_display = [
        'email',
        'is_staff'
        ,'is_superuser'
        ,'is_active'
        ,'is_verified'
    ]
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "email",
        "is_verified",
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = [
        'email'
        ,'is_staff'
        ,'is_superuser'
        ,'is_active'
        ,'is_verified'
        ,'verified_date'
        ,'created_at'
        ,'updated_at'
        ,'first_name'
        ,'last_name'
    ]
    fieldsets = (
        ('Authentication',{
            'fields':(
                'email',
                'password',
                'first_name'
                ,'last_name',
                'verified_code',
                'avatar',
        )
        })
        ,('Permissions', {
            "fields":(
                'is_active',
                'is_superuser',
                'is_staff',
                'is_verified'
            )
        }),
        ("Group&Permissions", {"fields": ("groups", "user_permissions")}),
        ("Important Date", {"fields": ("last_login", "verified_date")}),
    )
    add_fieldsets = (
        ("Authentication", {"fields": ("email", "password1", "password2" ,
                'first_name'
                ,'last_name')}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", 'is_verified')},
        ),
        ("Group&Permissions", {"fields": ("groups", "user_permissions")}),
    )
    