import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
import logging
from django.conf import LazySettings
settings = LazySettings()
logger = logging.getLogger(__name__)



class NotificationConsumer(AsyncWebsocketConsumer):

    def _is_authenticated(self):
        if hasattr(self.scope, 'auth_error'):
            return False
        if not self.scope['user'] or self.scope['user'] is AnonymousUser:
            return False
        return True

    async def connect(self):
        self.group_name = 'public_room'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        
        if self._is_authenticated():
            pass

        else:
            logger.error("ws client auth error")
            self.close(code=4003)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({ 'description': event['description'] }))


# def _is_authenticated(self):
#     if hasattr(self.scope, 'auth_error'):
#         return False
#     if not self.scope['user'] or self.scope['user'] is AnonymousUser:
#         return False
#     return True