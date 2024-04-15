from rest_framework import viewsets
from .models import Payment, CreditCard, Subscription, Withdraw
from .serializers import (
    PaymentSerializer, PaymentDetailSerializer, CreatePaymentSerializer, UpdatePaymentSerializer,
    DeletePaymentSerializer,
    CreditCardSerializer, CreditCardDetailSerializer, CreateCreditCardSerializer, UpdateCreditCardSerializer,
    DeleteCreditCardSerializer,
    SubscriptionSerializer, SubscriptionDetailSerializer, CreateSubscriptionSerializer, UpdateSubscriptionSerializer,
    DeleteSubscriptionSerializer,
    WithdrawSerializer, WithdrawDetailSerializer, CreateWithdrawSerializer, UpdateWithdrawSerializer,
    DeleteWithdrawSerializer,
)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return PaymentSerializer
        elif self.action == 'retrieve':
            return PaymentDetailSerializer
        elif self.action == 'create':
            return CreatePaymentSerializer
        elif self.action == 'update':
            return UpdatePaymentSerializer
        elif self.action == 'destroy':
            return DeletePaymentSerializer


class CreditCardViewSet(viewsets.ModelViewSet):
    queryset = CreditCard.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CreditCardSerializer
        elif self.action == 'retrieve':
            return CreditCardDetailSerializer
        elif self.action == 'create':
            return CreateCreditCardSerializer
        elif self.action == 'update':
            return UpdateCreditCardSerializer
        elif self.action == 'destroy':
            return DeleteCreditCardSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SubscriptionSerializer
        elif self.action == 'retrieve':
            return SubscriptionDetailSerializer
        elif self.action == 'create':
            return CreateSubscriptionSerializer
        elif self.action == 'update':
            return UpdateSubscriptionSerializer
        elif self.action == 'destroy':
            return DeleteSubscriptionSerializer


class WithdrawViewSet(viewsets.ModelViewSet):
    queryset = Withdraw.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return WithdrawSerializer
        elif self.action == 'retrieve':
            return WithdrawDetailSerializer
        elif self.action == 'create':
            return CreateWithdrawSerializer
        elif self.action == 'update':
            return UpdateWithdrawSerializer
        elif self.action == 'destroy':
            return DeleteWithdrawSerializer
