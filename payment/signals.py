from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User
from .models import CreditCard


@receiver(post_save, sender=User)
def clear_credit_card_info(sender, instance, created, **kwargs):
    if created:
        try:
            credit_card = instance.credit_card
            credit_card.credit_card_name = None
            credit_card.credit_card_number = None
            credit_card.credit_card_date = None
            credit_card.save()
        except CreditCard.DoesNotExist:
            pass
