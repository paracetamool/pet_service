from django.shortcuts import render
from django.db.models import Prefetch, F, Sum
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.core.cache import cache

from .models import Subscription
from clients.models import Client
from .serializers import SubscriprionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client', queryset=Client.objects.all().select_related('user').only(
                                                            "company_name",
                                                            "user__email"))
        )
    serializer_class = SubscriprionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        price_cache = cache.get('price_cache')

        if price_cache:
            total_price = price_cache
        else:
            total_price = queryset.aggregate(total=Sum('price')).get('total')
            cache.set('price_cache', total_price, 30)

        response_data = {'result': response.data}
        response_data['total_amount'] = total_price
        response.data = response_data
        return response