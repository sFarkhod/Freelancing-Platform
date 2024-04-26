from django.db.models.signals import post_save
from django.dispatch import receiver
from payment.models import CreditCard
from user.models import User


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        CreditCard.objects.create(user=instance)