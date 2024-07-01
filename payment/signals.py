from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import CreditCard, StripeCustomer
import stripe


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_credit_card_for_new_user(sender, instance, created, **kwargs):
    if created:
        CreditCard.objects.create(
            credit_card_user=instance,
            card_holder_name=None,
            card_number=None,
            card_expiration_date=None
        )
        
stripe.api_key = settings.STRIPE_SECRET_KEY

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_stripe_customer(sender, instance, created, **kwargs):
    if created:
        customer = stripe.Customer.create(
            email=instance.email
        )
        StripeCustomer.objects.create(user=instance, stripe_customer_id=customer.id)
