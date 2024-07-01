from django.urls import path, include
from rest_framework import routers
from .views import (
    PaymentViewSet, CreditCardViewSet, 
    SubscriptionViewSet, WithdrawViewSet,
    )

router = routers.DefaultRouter()
router.register(r'payments', PaymentViewSet)
router.register(r'creditcards', CreditCardViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'withdraws', WithdrawViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    # path('transfer/',TransferMoneyView.as_view(),name='transfer')
]
