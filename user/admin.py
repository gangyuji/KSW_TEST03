from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.forms import UserCreationForm, UserChangeForm


# Register your models here.
# Now register the new UserAdmin...


class MyUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id", "account", "email", "username",
                     "age", "gender","is_active", "is_admin", "created_at",]
    list_filter = ["is_active", "is_admin"]
    fieldsets = [
        ("User Information", {"fields": ["account", "username", "age", "gender", "password", "followings", ]}),
        ("Permissions", {"fields": ["is_active", "is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["account", "email", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["account"]
    ordering = ["account"]
    filter_horizontal = []

admin.site.register(User, MyUserAdmin)
