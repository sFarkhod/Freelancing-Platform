from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User, Freelancer, Client,Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type=='client':
            Client.objects.create(user=instance)
        if instance.user_type=='freelancer':
            Freelancer.objects.create(user=instance)


@receiver(post_save, sender=Notification)
def notification_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'public_room',
            {
                "type": "send_notification",
                "title": instance.title,
                "description": instance.description,
                "created_time": instance.created_time
            }
        )