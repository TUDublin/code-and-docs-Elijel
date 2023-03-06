from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm, FavoriteStopForm
from .models import CustomUser, FavoriteStop

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'age', 'is_staff',]

admin.site.register(CustomUser, CustomUserAdmin)

class FavoriteStopAdmin(admin.ModelAdmin):
    model = FavoriteStop
    list_display = ('user', 'stop')

admin.site.register(FavoriteStop, FavoriteStopAdmin)