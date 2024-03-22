from django.contrib import admin
from .models import Service, Subscription, Plan

admin.site.register(Plan)
admin.site.register(Service)
admin.site.register(Subscription)