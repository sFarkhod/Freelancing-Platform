from rest_framework import serializers
from .models import Payment, CreditCard, Subscription, Withdraw
from user.models import Client, Freelancer

class PaymentSerializer(serializers.ModelSerializer):
    
        class Meta:
            model = Payment
            fields = '__all__'
            extra_kwargs = {
                'payment_date' : {'read_only':True}
                }

class GetPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'client', 'freelancer', 'amount']



class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = '__all__'

class GetCreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ['id', 'credit_card_user', 'card_holder_name']



class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class GetSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'subscription_type', 'freelancer']



class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = '__all__'

class GetWithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = ['id', 'amount', 'freelancer']