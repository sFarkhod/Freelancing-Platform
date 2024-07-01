from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Payment, CreditCard, Subscription, Withdraw, StripeCustomer
import stripe
from decimal import Decimal
from config import settings
from .serializers import (
    PaymentSerializer, GetPaymentSerializer,
    SubscriptionSerializer, GetSubscriptionSerializer,
    WithdrawSerializer, GetWithdrawSerializer,
    CreditCardSerializer, GetCreditCardSerializer
)

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetPaymentSerializer
        return PaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            client = serializer.validated_data['client']
            freelancer = serializer.validated_data['freelancer']
            amount = serializer.validated_data['amount']
            print("Test:", client, freelancer, amount)

            try:
                client_user = client.user
                freelancer_user = freelancer.user
                print("Test1:", client_user, freelancer_user)
                
                client_stripe_customer = StripeCustomer.objects.get(user=client_user)
                print("Test2:", client_stripe_customer)

                freelancer_stripe_customer = StripeCustomer.objects.get(user=freelancer_user)
                print("Test3:", freelancer_stripe_customer)
                
                client_balance = Decimal(client.balance)

                if client_balance < amount:
                    return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

                payment_intent = stripe.PaymentIntent.create(
                    amount=int(amount * 100),
                    currency='usd',
                    customer=client_stripe_customer.stripe_customer_id,
                    payment_method_types=['card'],
                    capture_method='automatic',
                )
                
                print(payment_intent)

                transfer = stripe.Transfer.create(
                    amount=int(amount * 100),
                    currency='usd',
                    destination=freelancer_stripe_customer.stripe_customer_id,
                    source_transaction=payment_intent.id,
                )

                print(transfer)

                client.balance -= amount
                freelancer.balance += amount
                client.save()
                freelancer.save()
                
                payment = Payment.objects.create(
                    client=client,
                    freelancer=freelancer,
                    amount=amount
                )

                return Response({"success": True, "payment": self.get_serializer(payment).data}, status=status.HTTP_200_OK)

            except StripeCustomer.DoesNotExist:
                return Response({"error": "Stripe customer not found"}, status=status.HTTP_404_NOT_FOUND)
            except stripe.error.StripeError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CreditCardViewSet(ModelViewSet):
    queryset = CreditCard.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetCreditCardSerializer
        return CreditCardSerializer

class SubscriptionViewSet(ModelViewSet):
    queryset = Subscription.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetSubscriptionSerializer
        return SubscriptionSerializer

class WithdrawViewSet(ModelViewSet):
    queryset = Withdraw.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetWithdrawSerializer
        return WithdrawSerializer

class FreelancerBillingUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'payment_update/update_payment.html'
    model = CreditCard
    fields = ['card_holder_name', 'card_number', 'card_expiration_date']
    
    def test_func(self):
        return self.request.user.is_freelancer
