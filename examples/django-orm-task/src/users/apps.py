"""
Django app config. Registers signals.

Usage in settings.py:
    INSTALLED_APPS = [
        ...
        'users.apps.UsersConfig',
    ]
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'User Management'

    def ready(self):
        """Register signals when app is ready. Spec: FEAT-002."""
        # Import signals to register them
        from . import signals  # noqa: F401
