from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import CreditCard


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_credit_card_for_new_user(sender, instance, created, **kwargs):
    if created:
        CreditCard.objects.create(credit_card_user=instance)
