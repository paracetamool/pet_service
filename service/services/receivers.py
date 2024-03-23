from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.core.cache import cache

@receiver(post_delete, sender=None)
def delete_cach_total_sum(*args, **kwargs):
    cache.delete('price_cache')