"""
===========================
account/models.py
===========================

This module defines the custom Account model and its corresponding
AccountManager for handling user creation and retrieval logic.

It replaces Django’s default User model to use email as the unique
identifier instead of a username. It also supports role-based access
(e.g., tenant, landlord, agent, admin) and includes helper methods
for user management and authentication.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
import uuid
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

# -------------------
# Account Manager
# -------------------
class AccountManager(BaseUserManager):
    """
    Custom manager for the Account model.
    
    Provides helper methods for creating standard users,
    superusers, and retrieving Account objects safely.
    """
    def get_object_by_id(self, id):
        """
        Retrieve an Account instance by its UUID-based ID.
        
        Args:
            id (UUID): The UUID of the Account instance.
        
        Returns:
            Account or None: The Account instance if found,
            otherwise None if found or invalid ID.

        Notes:
            This method avoids raising exceptions like
            ObjectDoesNotExist or ValueError, returning None instead.
        """
        try:
            instance = self.get(id=id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return None

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a new user account.

        Args:
            email (str): User’s email address (must be unique).
            password (str): Raw password to be hashed and stored.
            **extra_fields: Additional keyword fields for Account.

        Raises:
            ValueError: If email or password is not provided.

        Returns:
            Account: The created Account instance.
        """
        if not email:
            raise ValueError("Email is required")
        
        if password is None:
            raise ValueError("User must have password")
        
        email = self.normalize_email(email)
        account = self.model(email=email, **extra_fields)
        account.set_password(password)
        account.save(using=self._db)
        return account
    
    def get_by_natural_key(self, email):
        """
        Override this method to normalize email input
        before attempting to find the user in the database.

        Args:
            email (str): Email address to look up.

        Returns:
            Account: Matching user instance if found.
        """
        email = self.normalize_email(email)
        return super().get_by_natural_key(email)
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a new superuser (admin).

        Args:
            email (str): Superuser’s email address.
            password (str): Password for the account.
            **extra_fields: Extra attributes for the superuser.

        Raises:
            TypeError: If email or password is missing.
            ValueError: If required superuser flags are not True.

        Returns:
            Account: The created superuser Account instance.
        """
        if email is None:
            raise TypeError("Superusers must have an email.")
        if password is None:
            raise TypeError("Superusers must have an password.")
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
    """
    Custom user model that supports authentication via email instead of username.

    Attributes:
        id (UUID): Primary key, auto-generated UUID.
        first_name (str): User’s first name.
        last_name (str): User’s last name.
        email (str): Unique email used as the login credential.
        phone_number (str): Unique contact number.
        sex (str): Gender, one of 'male', 'female', or 'other'.
        role (str): Role type such as tenant, landlord, agent, or admin.
        age (int): Optional age field.
        address (str): User’s address information.
        profile_photo (ImageField): Optional user profile image.
        is_active (bool): Indicates whether the account is active.
        is_verified (bool): Whether the user’s email or account is verified.
        is_staff (bool): Grants staff access to admin interface.
        date_joined (datetime): Timestamp when user joined.
        date_updated (datetime): Auto-updated timestamp when modified.
    """
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
    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        primary_key=True
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
    # age = models.PositiveIntegerField(blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
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
        """
        Return the user’s full name by concatenating first and last names.

        Returns:
            str: The user’s full name in "First Last" format.
        """
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        """Returns user's age.
        Returns:
            int: The user's age.
        """
        if self.dob is None:
            return None
        today = datetime.now()
        age = (today.year - self.dob.year) - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age
  
    def __str__(self):
        """
        Return a human-readable string representation of the user.

        Returns:
            str: User’s email and role (e.g., "user@example.com (tenant)").
        """
        return f"{self.email} ({self.role})\nID: {self.id}"
    
    
