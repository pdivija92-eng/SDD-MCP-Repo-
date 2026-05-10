"""
Django User and Profile models with signals.

Spec: FEAT-002 (docs/specs/FEAT-002-user-model.md)
Status: Implemented 2024-01-15
"""

from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


class User(models.Model):
    """
    Custom User model with email as unique identifier.

    Spec: FR-1 — User with email, password, timestamps
    """
    email = models.EmailField(unique=True, max_length=254)
    password_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users_user'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.email

    def set_password(self, raw_password: str) -> None:
        """Hash and set password. Spec: FR-1."""
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        """Verify password against hash. Spec: FR-1."""
        return check_password(raw_password, self.password_hash)


class Profile(models.Model):
    """
    User profile auto-created on user creation.

    Spec: FR-2, FR-3 — Auto-created Profile with bio, avatar, last_login
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, default='')
    avatar_url = models.URLField(blank=True, default='')
    last_login = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users_profile'
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['last_login']),
        ]

    def __str__(self):
        return f"Profile({self.user.email})"

    def update_last_login(self) -> None:
        """Update last_login timestamp. Spec: FR-5."""
        self.last_login = timezone.now()
        self.save(update_fields=['last_login', 'updated_at'])
