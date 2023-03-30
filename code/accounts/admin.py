from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Favorite

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'age', 'is_staff',]

class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite
    list_display = ['user', 'stop']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Favorite, FavoriteAdmin)
