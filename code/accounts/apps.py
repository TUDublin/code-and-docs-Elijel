"""
Accounts app configuration module.
"""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    AppConfig for accounts app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
