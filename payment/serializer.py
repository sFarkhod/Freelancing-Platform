from rest_framework import serializers
from .models import Payment, CreditCard, Subscription, Withdraw


# payment
class PaymentSerializer(serializers.ModelSerializer):
    payment_detail = serializers.SerializerMethodField('get_payment_detail')

    def get_payment_detail(self, instance):
        return f'http://127.0.0.1:8000/payment/api/payments/detail/{instance.pk}/'

    class Meta:
        model = Payment
        fields = ['id', 'amount', 'payment_date', 'payment_detail']


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class CreatePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_date', 'client_id', 'freelancer_id']


class UpdatePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_date', 'client_id', 'freelancer_id']


class DeletePaymentSerializer(serializers.ModelSerializer):
    def delete(self, instance):
        instance.delete()

    class Meta:
        model = Payment
        fields = ['id', ]


# Credit Card
class CreditCardSerializer(serializers.ModelSerializer):
    credit_card_detail = serializers.SerializerMethodField('get_creditcard_detail')

    def get_creditcard_detail(self, instance):
        return f'http://127.0.0.1:8000/payment/api/credit-card/detail/{instance.pk}/'

    class Meta:
        model = CreditCard
        fields = ['id', 'card_holder_name', 'card_number', 'credit_card_detail']


class CreditCardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = '__all__'


class CreateCreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ['card_holder_name', 'card_number', 'card_expiration_date']


class UpdateCreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ['card_holder_name', 'card_number', 'card_expiration_date']


class DeleteCreditCardSerializer(serializers.ModelSerializer):
    def delete(self, instance):
        instance.delete()

    class Meta:
        model = CreditCard
        fields = ['id', ]


# Subscription
class SubscriptionSerializer(serializers.ModelSerializer):
    subscription_detail = serializers.SerializerMethodField('get_subscription_detail')

    def get_subscription_detail(self, instance):
        return f'http://127.0.0.1:8000/payment/api/subscriptions/detail/{instance.pk}/'

    class Meta:
        model = Subscription
        fields = ['id', 'start_date', 'freelancer', 'end_date', 'subscription_detail']


class SubscriptionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class CreateSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['subscription_type', 'start_date', 'end_date', 'freelancer']


class UpdateSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['subscription_type', 'start_date', 'end_date', 'freelancer']


class DeleteSubscriptionSerializer(serializers.ModelSerializer):
    def delete(self, instance):
        instance.delete()

    class Meta:
        model = Subscription
        fields = ['id', ]


# withdraw
class WithdrawSerializer(serializers.ModelSerializer):
    withdraw_detail = serializers.SerializerMethodField('get_withdraw_detail')

    def get_withdraw_detail(self, instance):
        return f'http://127.0.0.1:8000/payment/api/withdraw/detail/{instance.pk}/'

    class Meta:
        model = Withdraw
        fields = ['id', 'amount', 'withdraw_date', 'withdraw_detail']


class WithdrawDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = '__all__'


class CreateWithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = ['amount', 'withdraw_date', 'freelancer']


class UpdateWithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = ['amount', 'withdraw_date', 'freelancer']


class DeleteWithdrawSerializer(serializers.ModelSerializer):
    def delete(self, instance):
        instance.delete()

    class Meta:
        model = Withdraw
        fields = ['id', ]
