from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from rest_framework_simplejwt.token_blacklist import admin as jwt_admin
from rest_framework_simplejwt.token_blacklist import models as jwt_models

from apps.users.models import User


class UserAdmin(BaseUserAdmin):
    model = User

    list_display = (
        'email', 'first_name', 'last_name', 'dob', 'is_staff', 'is_active', 'is_superuser', 'auth_provider',
        'created_at'
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    change_password_form = auth_admin.AdminPasswordChangeForm

    fieldsets = (
        ('User Info',
         {'fields': ('email', 'password', 'first_name', 'last_name', 'dob', 'is_staff', 'is_active', 'is_superuser',
                     'auth_provider', 'user_permissions', 'groups')}),
        ('Other info', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'auth_provider')


class OutstandingTokenAdmin(jwt_admin.OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True


class PermissionAdmin(admin.ModelAdmin):
    model = Permission
    fields = ['name']


class GroupAdmin(admin.ModelAdmin):
    model = Group
    fields = ['name', 'permissions']


# admin.site.register(Group, GroupAdmin)
admin.site.register(Permission, PermissionAdmin)


admin.site.unregister(jwt_models.OutstandingToken)
admin.site.register(jwt_models.OutstandingToken, OutstandingTokenAdmin)

admin.site.register(User, UserAdmin)
