from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)

# -------------------
# Account Manager
# -------------------
class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)
        account = self.model(email=email, **extra_fields)
        account.set_password(password)
        account.save(using=self._db)
        return account
    
    def get_by_natural_key(self, email):
        """
        Override this method to normalize email input
        before attempting to find the user in the database
        """
        email = self.normalize_email(email)
        return super().get_by_natural_key(email)
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self.create_user(email, password, **extra_fields)



# ---------------------------
# ACCOUNT MODEL
# ---------------------------
class Account(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("tenant", "Tenant"),
        ("landlord", "Landlord"),
        ("agent", "Agent"),
        ("admin", "Admin"),
    )

    SEX_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(null=False, blank=False, max_length=50)
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=20, unique=True)
    sex = models.CharField(choices=SEX_CHOICES, max_length=10)
    role = models.CharField(
        choices=ROLE_CHOICES,
        max_length=8,
        default='tenant'
    )
    age = models.PositiveIntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    profile_photo = models.ImageField(
        upload_to='images',
        null=True,
        blank=True
    )

    # System fields
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = AccountManager()
    
    USERNAME_FIELD = 'email'
    
    # Required fields only apply when creating superuser
    REQUIRED_FIELDS = [
        'first_name',
    ]
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return f"{self.email} ({self.role})"
    
    
