from django.core.validators import RegexValidator
from django.db import models
from config import settings


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    client = models.ForeignKey('user.Client', on_delete=models.DO_NOTHING, related_name='payments_made',
                               null=True, blank=True)
    freelancer = models.ForeignKey('user.Freelancer', on_delete=models.DO_NOTHING, related_name='payments_received',
                                   null=True, blank=True)

    def __str__(self):
        return f'{self.client} - {self.freelancer}'

    class Meta:
        db_table = 'payment'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        


class StripeCustomer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.user.username
    

    class Meta:
        db_table = 'stripe_customer'
        verbose_name = 'StripeCustomer'
        verbose_name_plural = 'StripeCustomer'


class CreditCard(models.Model):
    credit_card_user = models.ForeignKey('user.User', models.DO_NOTHING, related_name='user_credit_card',
                                         null=True, blank=True)
    card_holder_name = models.CharField(max_length=255, null=True)
    card_number = models.CharField(
        max_length=16,
        validators=[
            RegexValidator(regex=r'^\d{16}$', message='Card number must be 16 digits')
        ],
        null=True
    )
    card_expiration_date = models.CharField(
        max_length=5,
        validators=[
            RegexValidator(regex=r'^(0[1-9]|1[0-2])\/?([0-9]{2})$', message='Expiration date must be in MM/YY format')
        ],
        null=True
    )

    class Meta:
        db_table = 'credit_card'
        verbose_name = 'Credit Card'
        verbose_name_plural = 'Credit Cards'


class SubscriptionType(models.Model):
    subscription_type = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.subscription_type

    class Meta:
        db_table = 'subscription_type'
        verbose_name = 'Subscription Type'
        verbose_name_plural = 'Subscription Types'


class Subscription(models.Model):
    subscription_type = models.ForeignKey(SubscriptionType, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    freelancer = models.ForeignKey('user.Freelancer', on_delete=models.DO_NOTHING, related_name='subscriptions')

    def __str__(self):
        return str(self.subscription_type)

    class Meta:
        db_table = 'subscription'
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'


class Withdraw(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    withdraw_date = models.DateField(null=True, blank=True, auto_now_add=True)
    freelancer = models.ForeignKey('user.Freelancer', on_delete=models.DO_NOTHING, related_name='withdrawals',
                                   null=True, blank=True)

    def __str__(self):
        return str(self.withdraw_date)

    class Meta:
        db_table = 'withdraw'
        verbose_name = 'Withdraw'
        verbose_name_plural = 'Withdrawals'
