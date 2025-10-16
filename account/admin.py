"""
==================
account/admin.py
==================

This module registers the custom Account model in the Django admin interface.

It provides a tailored admin panel for managing user accounts with
role-based access, detailed filtering, search capabilities, and
well-structured field layouts. This customization extends Django’s
built-in `UserAdmin` to fit the custom Account model defined in
`account/models.py`.

"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account


@admin.register(Account)
class AccountAdmin(UserAdmin):
    """
    Custom Django admin configuration for the Account model.

    This class extends Django’s built-in `UserAdmin` to:
      - Display and filter users based on key attributes.
      - Make audit fields (e.g., `date_joined`, `date_updated`) read-only.
      - Provide logical grouping of user details, permissions, and dates.
      - Support an improved UI for managing ManyToMany permission fields.
    """
    ordering = ('-date_updated',)
    list_display = [
        'first_name', 'last_name', 'email', 'sex',
        'phone_number', 'role', 'is_active', 'is_verified',
        'date_joined', 'date_updated'
    ]
    search_fields = (
        'email', 'first_name'
    )
    list_filter = (
        'is_active',
        'is_verified',
        'is_staff',
        'role',
        'date_joined',
    )
    #: Fields that cannot be edited directly in the admin
    readonly_fields = ('date_joined', 'date_updated', 'last_login',)

    #: Field organization for the change (edit) form
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password'),
        }),
        ('Personal Information', {
            'fields': (
                'first_name', 'last_name', 'sex', 'age', 'phone_number',
                'role', 'address', 'profile_photo'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_verified', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'  # Essential permissions fields
            )
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined', 'date_updated')
        }),
    )

    # Better interface for Many-to-Many fields
    filter_horizontal = (
        'groups',
        'user_permissions',
    )

    #: Field organization for the add-user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        ('Personal Information', {
            'fields': (
                'first_name', 'last_name', 'sex', 'phone_number', 'age',
                'role', 'address', 'profile_photo'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_verified', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
    )
