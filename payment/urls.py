from django.urls import path
from .views import (
    PaymentListAPIView, PaymentDetailAPIView, PaymentCreateAPIView, PaymentUpdateAPIView, PaymentDeleteAPIView,
    CreditCardListAPIView, CreditCardDetailAPIView, CreditCardCreateAPIView, CreditCardUpdateAPIView, CreditCardDeleteAPIView,
    SubscriptionListAPIView, SubscriptionDetailAPIView, SubscriptionCreateAPIView, SubscriptionUpdateAPIView, SubscriptionDeleteAPIView,
    WithdrawListAPIView, WithdrawDetailAPIView,  WithdrawCreateAPIView, WithdrawUpdateAPIView, WithdrawDeleteAPIView,
)

urlpatterns = [
    # payment
    path('payment/api/', PaymentListAPIView.as_view()),
    path('payment/detail/<int:pk>/', PaymentDetailAPIView.as_view()),
    path('payment/create/', PaymentCreateAPIView.as_view()),
    path('payment/update/<int:pk>/', PaymentUpdateAPIView.as_view()),
    path('payment/delete/<int:pk>/', PaymentDeleteAPIView.as_view()),
    # credit card
    path('credit-cards/api/', CreditCardListAPIView.as_view()),
    path('credit-cards/detail/<int:pk>/', CreditCardDetailAPIView.as_view()),
    path('credit-cards/create/', CreditCardCreateAPIView.as_view()),
    path('credit-cards/update/<int:pk>/', CreditCardUpdateAPIView.as_view()),
    path('credit-cards/delete/<int:pk>/', CreditCardDeleteAPIView.as_view()),
    # subscription
    path('subscriptions/api/', SubscriptionListAPIView.as_view()),
    path('subscriptions/detail/<int:pk>/', SubscriptionDetailAPIView.as_view()),
    path('subscriptions/create/', SubscriptionCreateAPIView.as_view()),
    path('subscriptions/update/<int:pk>', SubscriptionUpdateAPIView.as_view()),
    path('subscriptions/delete/<int:pk>/', SubscriptionDeleteAPIView.as_view()),
    # withdraw
    path('withdraw/api/', WithdrawListAPIView.as_view()),
    path('withdraw/detail/<int:pk>/', WithdrawDetailAPIView.as_view()),
    path('withdraw/create/', WithdrawCreateAPIView.as_view()),
    path('withdraw/update/<int:pk>/', WithdrawUpdateAPIView.as_view()),
    path('withdraw/delete/<int:pk>/', WithdrawDeleteAPIView.as_view()),
]
