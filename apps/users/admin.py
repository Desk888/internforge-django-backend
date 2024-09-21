from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email_address', 'first_name', 'last_name', 'is_staff', 'user_type')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'email_verified', 'email_verification_token')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email_address', 'user_type')}),
    )

admin.site.register(User, CustomUserAdmin)