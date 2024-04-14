from django.db import models
from user.models import Client, Freelancer


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='payments_made')
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name='payments_received')

    class Meta:
        db_table = 'payment'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'


class CreditCard(models.Model):
    card_holder_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16)
    card_expiration_date = models.CharField(max_length=5)

    def __str__(self):
        return self.card_holder_name

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
    start_date = models.DateField()
    end_date = models.DateField()
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name='subscriptions')

    def __str__(self):
        return str(self.subscription_type)

    class Meta:
        db_table = 'subscription'
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'


class Withdraw(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    withdraw_date = models.DateField()
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name='withdrawals')

    def __str__(self):
        return str(self.withdraw_date)

    class Meta:
        db_table = 'withdraw'
        verbose_name = 'Withdraw'
        verbose_name_plural = 'Withdrawals'
