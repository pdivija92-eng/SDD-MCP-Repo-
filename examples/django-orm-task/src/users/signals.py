"""
Signal handlers for User model.

Spec: FEAT-002 — Auto-create Profile, invalidate cache

Register in apps.py:
    def ready(self):
        from . import signals
"""

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import User, Profile


@receiver(post_save, sender=User)
def auto_create_profile(sender, instance: User, created: bool, **kwargs):
    """
    Auto-create Profile when User is created.

    Spec: FR-2 — Profile auto-created on user creation
    """
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=Profile)
def invalidate_profile_cache(sender, instance: Profile, **kwargs):
    """
    Invalidate cached Profile data when Profile is updated.

    Spec: FR-6, FR-7 — Cache invalidation on Profile save
    """
    cache_key = f"profile:{instance.user_id}"
    cache.delete(cache_key)


def get_profile_cached(user_id: int, ttl: int = 3600) -> Profile | None:
    """
    Get Profile from cache or database.

    Args:
        user_id: User ID
        ttl: Cache TTL in seconds (default 1 hour)

    Returns:
        Profile or None if user not found

    Spec: FR-6 — Cache Profile with 1-hour TTL
    """
    cache_key = f"profile:{user_id}"

    # Try cache first
    profile = cache.get(cache_key)
    if profile:
        return profile

    # Fall back to database
    try:
        profile = Profile.objects.get(user_id=user_id)
        cache.set(cache_key, profile, ttl)
        return profile
    except Profile.DoesNotExist:
        return None
