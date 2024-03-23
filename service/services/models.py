from typing import Any, Iterable
from django.db import models
from django.core.validators import MaxValueValidator
from clients.models import Client
from .tasks import set_price

class Service(models.Model):
    name = models.CharField(max_length=50)
    full_price = models.PositiveIntegerField()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price

    def save(self, *args, **kwargs) -> None:

        if self.full_price != self.__full_price:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)

        return super().save(*args, **kwargs)


class Plan(models.Model):
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount')
    )

    plan_type = models.CharField(choices=PLAN_TYPES, max_length=10)
    discount_persent = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])


    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__discount_persent = self.discount_persent

    def save(self, *args, **kwargs) -> None:

        if self.discount_persent != self.__discount_persent:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)

        return super().save(*args, **kwargs)


class Subscription(models.Model):
    client = models.ForeignKey(Client, related_name='subscriptions', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, related_name='subscriptions', on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, related_name='subscriptions', on_delete=models.PROTECT)
    price = models.PositiveIntegerField(default=0)