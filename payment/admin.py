from django.contrib import admin
from .models import (
    Payment, CreditCard, 
    Subscription, Withdraw, 
    SubscriptionType, StripeCustomer
                     )

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'payment_date')
    search_fields = ('payment_date', 'client', 'freelancer')
    list_filter = ('amount', 'payment_date', 'client', 'freelancer')


class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'credit_card_user', 'card_holder_name')
    search_fields = ('credit_card_user', 'card_holder_name')
    list_filter = ('card_holder_name',)


class SubscriptionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'subscription_type', 'price')
    


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'subscription_type', 'start_date', 'end_date')
    search_fields = ('subscription_type', 'freelancer', 'start_date', 'end_date')
    list_filter = ('subscription_type', 'start_date', 'end_date')

class WithdrawAdmin(admin.ModelAdmin):
    list_display = ('id', 'freelancer', 'amount')
    search_fields = ('withdraw_date', 'freelancer', 'amount')
    list_filter = ('freelancer', 'amount', 'withdraw_date')
    

class StripeCustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'stripe_customer_id')
    search_fields = ('user',)
    list_filter = ('user',)

admin.site.register(Payment, PaymentAdmin)
admin.site.register(CreditCard, CreditCardAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Withdraw, WithdrawAdmin)
admin.site.register(SubscriptionType, SubscriptionTypeAdmin)
admin.site.register(StripeCustomer, StripeCustomerAdmin)
