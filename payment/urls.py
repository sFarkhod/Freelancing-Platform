from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, CreditCardViewSet, SubscriptionViewSet, WithdrawViewSet

# Ruterni yaratamiz va uni foydalanuvchilar bilan ro'yxatga olamiz.
router = DefaultRouter()
router.register(r'payments', PaymentViewSet)
router.register(r'credit-cards', CreditCardViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'withdraws', WithdrawViewSet)

# API URLlari avtomatik ravishda router tomonidan aniqlanadi.
# Qo'shimcha ravishda, ko'rinuvchi API uchun kirish URLlarini qo'shib chiqamiz.
urlpatterns = [
    path('api/', include(router.urls)),
]
