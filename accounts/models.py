from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string

class UserManager(BaseUserManager):
    """
    Custom user manager for user
    """
    def create_user(self, email, password, **extra_fields):
        """
        for Create a simple user
        """
        if not email:
            raise ValueError(_('email not valid'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        for Creating admin user that haa full control
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))            
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))                
        if extra_fields.get('is_active') is not True:
            raise ValueError(_('Superuser must have is_active=True'))            
        if extra_fields.get('is_verified') is not True:
            raise ValueError(_('Superuser must have is_verified=True'))                

        return self.create_user(email, password, **extra_fields)




class User(AbstractBaseUser, PermissionsMixin):
    """
    Create Custom User Model
    """
    email = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    verified_code = models.CharField(max_length=255, default=get_random_string(255))
    verified_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    first_name = models.CharField(null=True, blank=True, max_length=255)
    last_name = models.CharField(null=True, blank=True, max_length=255)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        for getting the full name if exist or get email
        """
        if self.first_name is not None and self.last_name is not None:
            return self.first_name + ' ' + self.last_name 
        else:
            return self.email


    
