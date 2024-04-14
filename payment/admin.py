from django.contrib import admin
from .models import Payment, Subscription, CreditCard, Withdraw, SubscriptionType


admin.site.register(Payment)
admin.site.register(Subscription)
admin.site.register(CreditCard)
admin.site.register(Withdraw)
admin.site.register(SubscriptionType)
