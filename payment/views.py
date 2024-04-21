from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView
from rest_framework.viewsets import ModelViewSet
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


class PaymentViewSet(ModelViewSet):
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


class CreditCardViewSet(ModelViewSet):
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


class SubscriptionViewSet(ModelViewSet):
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


class WithdrawViewSet(ModelViewSet):
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


class FreelancerBillingUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'payment_update/update_payment.html'
    model = CreditCard
    fields = ['card_holder_name', 'card_number', 'card_expiration_date']
