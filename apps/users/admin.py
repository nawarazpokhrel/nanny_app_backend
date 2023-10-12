from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.users.forms import UserChangeForm, UserCreationForm
from apps.users.models import User


# Register your models here.

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # add_form_template = 'admin/auth/user/add_form.html'
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('fullname', 'phone_number', 'role')
    list_filter = ('is_superuser', 'is_active', 'groups', 'role')
    search_fields = ('fullname', 'phone_number', 'role')
    ordering = ('fullname',)
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('Personal info'), {'fields': ('fullname', 'role')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'role', 'fullname'),
        }),
    )


admin.site.register(User, UserAdmin)
