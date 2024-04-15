from django.contrib import admin
from .models import Payment, CreditCard, Subscription, Withdraw, SubscriptionType


admin.site.register(Payment)
admin.site.register(CreditCard)
admin.site.register(Subscription)
admin.site.register(Withdraw)
admin.site.register(SubscriptionType)
