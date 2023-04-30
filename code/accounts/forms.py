"""
Forms for accounts app.
"""
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    A form that extends UserCreationForm to include age and email fields.
    """
    class Meta(UserCreationForm.Meta):
        """
        Meta Field For UserCreationForm
        """
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('age', 'email',)

class CustomUserChangeForm(UserChangeForm):
    """
    A form that extends UserChangeForm to include all fields.
    """
    class Meta:
        """
        Meta Field For UserChangeForm
        """
        model = CustomUser
        fields = UserChangeForm.Meta.fields
