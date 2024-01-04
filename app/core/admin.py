"""
Django Admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core import models


class UserAdmin(BaseUserAdmin):
    """Defin the admin pages for users"""

    ordering = ['id']
    list_display = ['name', 'email']

    fieldsets = (
        (None, {'fields': ('name', 'email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_superuser',
                    'is_staff',
                    )
            }
        ),

        (_('Important Dates'), {'fields': ('last_login',)})
    )

    readonly_fields = ['last_login']

    add_fieldsets = (
        (None,
            {
                'fields': (
                    'name',
                    'email',
                    'password1',
                    'password2',
                    'is_active',
                    'is_superuser',
                    'is_staff'
                )
            }),
    )


admin.site.register(models.User, UserAdmin)
