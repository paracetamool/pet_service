from django.shortcuts import render
from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Subscription
from clients.models import Client
from .serializers import SubscriprionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client', queryset=Client.objects.all().select_related('user').only(
                                                            "company_name",
                                                            "user__email")))
    serializer_class = SubscriprionSerializer