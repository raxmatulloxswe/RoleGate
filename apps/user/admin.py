from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, RefreshToken, BlackListedToken

# SendOPT your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    readonly_fields = ('date_joined',)
    list_display = ('id', 'email',  'phone_number', 'role')
    list_display_links = ('id', 'email')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('id', 'email',)


@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'used_at')
    list_display_links = ('id', 'user')
    search_fields = ('token', )


@admin.register(BlackListedToken)
class BlackListedTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'token_type', 'created_at')
    list_display_links = ('id', 'user')
    search_fields = ('token', 'user__email')
