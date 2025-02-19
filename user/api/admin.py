from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from api.forms import CustomUserCreationForm, CustomUserChangeForm
from api.models import User

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['username', 'owner_uuid']

admin.site.register(User, CustomUserAdmin)