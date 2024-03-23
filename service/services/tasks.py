from celery import shared_task
from celery_singleton import Singleton
from django.db.models import F
from django.db import transaction
from django.core.cache import cache



@shared_task(base=Singleton)
def set_price(subscription_id):
    from services.models import Subscription

    with transaction.atomic():

        subscription = Subscription.objects.select_for_update().filter(id=subscription_id).annotate(
                        annotated_price=F('service__full_price')-F('service__full_price')*F('plan__discount_persent')/100.00
                        ).first()
        subscription.price = subscription.annotated_price
        subscription.save()
    
    cache.delete('price_cache')
    