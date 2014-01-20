from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import admin_forms
from .models import User


class UserAdmin(BaseUserAdmin):
    form = admin_forms.UserChangeForm
    add_form = admin_forms.UserCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )
    list_display = ('email',)
    list_filter = ('is_active',)
    search_fields = ('name', 'email')
    ordering = ('name',)

admin.site.register(User, UserAdmin)
