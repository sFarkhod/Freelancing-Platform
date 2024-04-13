from rest_framework import permissions
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Payment, Subscription, CreditCard, Withdraw
from .serializer import (
    PaymentSerializer, PaymentDetailSerializer, CreatePaymentSerializer, UpdatePaymentSerializer,
    DeletePaymentSerializer,
    SubscriptionSerializer, SubscriptionDetailSerializer, CreateSubscriptionSerializer, UpdateSubscriptionSerializer,
    DeleteSubscriptionSerializer,
    CreditCardSerializer, CreditCardDetailSerializer, CreateCreditCardSerializer, UpdateCreditCardSerializer,
    DeleteCreditCardSerializer,
    WithdrawSerializer, WithdrawDetailSerializer, CreateWithdrawSerializer, UpdateWithdrawSerializer,
    DeleteWithdrawSerializer
)


class IsVacationOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return view.get_object().members_user == request.user


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDetailAPIView(RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentDetailSerializer


class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = CreatePaymentSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]


class PaymentUpdateAPIView(UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = UpdatePaymentSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]


class PaymentDeleteAPIView(DestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = DeletePaymentSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]


# Subcription
class SubscriptionListAPIView(ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class SubscriptionDetailAPIView(RetrieveAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionDetailSerializer


class SubscriptionCreateAPIView(CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = CreateSubscriptionSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]


class SubscriptionUpdateAPIView(UpdateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = UpdateSubscriptionSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]


class SubscriptionDeleteAPIView(DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = DeleteSubscriptionSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]


# CreditCard
class CreditCardListAPIView(ListAPIView):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer


class CreditCardDetailAPIView(RetrieveAPIView):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardDetailSerializer


class CreditCardCreateAPIView(CreateAPIView):
    queryset = CreditCard.objects.all()
    serializer_class = CreateCreditCardSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]


class CreditCardUpdateAPIView(UpdateAPIView):
    queryset = CreditCard.objects.all()
    serializer_class = UpdateCreditCardSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]


class CreditCardDeleteAPIView(DestroyAPIView):
    queryset = CreditCard.objects.all()
    serializer_class = DeleteCreditCardSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]


# Withdraw
class WithdrawListAPIView(ListAPIView):
    queryset = Withdraw.objects.all()
    serializer_class = WithdrawSerializer


class WithdrawDetailAPIView(RetrieveAPIView):
    queryset = Withdraw.objects.all()
    serializer_class = WithdrawDetailSerializer


class WithdrawCreateAPIView(CreateAPIView):
    queryset = Withdraw.objects.all()
    serializer_class = CreateWithdrawSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]


class WithdrawUpdateAPIView(UpdateAPIView):
    queryset = Withdraw.objects.all()
    serializer_class = UpdateWithdrawSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]


class WithdrawDeleteAPIView(DestroyAPIView):
    queryset = Withdraw.objects.all()
    serializer_class = DeleteWithdrawSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]
