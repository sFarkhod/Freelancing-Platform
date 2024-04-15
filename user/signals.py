from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User, Freelancer, Client


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type=='client':
            Client.objects.create(user=instance)
        if instance.user_type=='freelancer':
            Freelancer.objects.create(user=instance)