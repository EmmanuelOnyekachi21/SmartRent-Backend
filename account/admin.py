from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account

@admin.register(Account)
class AccountAdmin(UserAdmin):
    ordering = ('email',)
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
    # Fields that should not be manually changed
    readonly_fields = ('date_joined', 'date_updated', 'last_login',)
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password'),
        }),
        ('Personal Information', {
            'fields': (
                'first_name', 'last_name', 'sex', 'phone_number', 
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
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        ('Personal Information', {
            'fields': (
                'first_name', 'last_name', 'sex', 'phone_number',
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
